/**
 * Read the full content of a single 3MS document (blog/doc).
 *
 * Input: a full 3MS detail URL (the `detail_url` from a `search` result), e.g.
 * `https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113`. A bare
 * numeric docId is not accepted — 3MS detail URLs require the group id, which
 * a bare id doesn't carry.
 * Output: the complete document — title, author, date, views/likes/comments,
 * and the full body text.
 *
 * This complements `search`, which returns summaries + metadata for many
 * documents. `read` fetches one document's full body.
 *
 * Strategy: COOKIE — the detail page is SSO-gated, so the adapter drives the
 * logged-in Chrome tab to the detail URL and scrapes the rendered `#content-body`
 * (or `.content`).
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - body:     #content-body  (cleanest; fallback .content). Contains breadcrumb
 *               + meta (作者/日期/浏览/回复) + the article body; the meta is
 *               parsed out separately and the body is the text after it.
 *   - title:    document.title (format: "<title> - <community> - 3MS知识管理社区")
 *   - author:   the "楼主<name>等级" token in .content, or a[Uuf]field link
 *   - date:     "日期：YYYY-MM-DD" inline
 *   - views:    "浏览：N" inline  ·  replies: "回复：N" inline
 *
 * Comments: 3MS blog detail pages lazy-load the comment thread (via a widget/
 * iframe that only renders on interaction), so `comments_thread` is best-effort
 * and often empty. The body is the primary content on 3MS (unlike 稼先社区,
 * where the discussion thread carried much of the value).
 *
 * NOTE: hand-mirrored from read.ts (no build step). Keep the two in sync.
 */

import { cli, Strategy } from "@jackwener/opencli/registry";
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from "@jackwener/opencli/errors";

const BASE_URL = "https://3ms.huawei.com";
const DOMAIN = "3ms.huawei.com";

// Detail route. The docId is the trailing /details/<docId> segment. The
// /km/groups/<gid>/ prefix is optional — /km/blogs/details/<docId> also works.
const DETAIL_PATH = "/km/blogs/details/";

// How long (seconds) to wait for the body to render after navigation.
const RENDER_WAIT_S = 5;

cli({
    site: "huawei-3ms",
    name: "read",
    access: "read",
    description: "Read the full content of a single 3MS document by its docId (bare numeric id, or the full detail URL). Returns the complete document body plus title, author, date, views/likes/comments. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.",
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: "doc_id", positional: true, required: true, help: "The full 3ms.huawei.com detail URL (e.g. https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113) — take it from a search result's detail_url. A bare numeric id is not accepted (3MS detail URLs require the group id)." },
    ],
    columns: ["title", "author", "author_id", "date", "views", "likes", "comments", "body", "comments_thread", "url"],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError("Browser session required for huawei-3ms read");

        const raw = String(kwargs.doc_id || "").trim();
        if (!raw) throw new ArgumentError("huawei-3ms read doc_id cannot be empty");

        // Resolve to a full detail URL. A full URL is used as-is; a bare docId
        // is resolved by searching for it (3MS detail URLs require the group
        // id: /km/groups/<gid>/blogs/details/<id>, and the group-less form
        // /km/blogs/details/<id> redirects to the user profile, not the doc).
        const { docId, detailUrl } = await resolveDetailUrl(page, raw);

        // Navigate to the detail page (SSO-gated; the bridge drives the
        // logged-in Chrome tab). The page is an SPA — wait for the body
        // container to render before scraping (a bare time wait races it).
        await page.goto(detailUrl);
        await page.wait("selector", "#content-body, .content").catch(() => {});
        await page.wait("time", RENDER_WAIT_S).catch(() => {});

        // Auth gate.
        const authOk = await page.evaluate(() => {
            const body = document.querySelector("#content-body, .content");
            const hasLoginPrompt = /请登录|sign\s*in/i.test(document.documentElement.outerHTML) && !body;
            return !!body || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, "3MS requires a logged-in session. Open https://3ms.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.");
        }

        // Scrape the rendered detail content (all extraction in-page).
        const doc = await page.evaluate(() => {
            const text = (el) => (el?.textContent || "").trim();
            const bodyEl = document.querySelector("#content-body") || document.querySelector(".content");

            // Title: document.title is "<title> - <community> - 3MS知识管理社区".
            const title = (document.title || "").split(/\s*-\s*3MS知识管理社区/)[0].split(/\s*-\s*/)[0].trim();

            // The body container text mixes breadcrumb + meta + article body.
            // Parse the meta out of it, then take the article body as the text
            // after the meta block.
            const raw = text(bodyEl);
            const authorMatch = raw.match(/楼主\s*([^\s]+)\s*等级/);
            const author = authorMatch ? authorMatch[1] : "";
            const dateMatch = raw.match(/日期[：:]\s*(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)/);
            const viewsMatch = raw.match(/浏览[：:]\s*(\d+)/);
            const repliesMatch = raw.match(/回复[：:]\s*(\d+)/);

            // Body: everything after the "最近编辑时间：<timestamp>" meta line.
            // The textContent has no newlines, so match the timestamp
            // specifically (not [^\n]*) — else the greedy match eats the body.
            // Fallback: after "回复：N" if no edit-time marker.
            let body = raw;
            const editMatch = body.match(/最近编辑时间[：:]\s*\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?\s*/);
            if (editMatch) {
                body = body.slice(body.indexOf(editMatch[0]) + editMatch[0].length);
            } else {
                const repliesMatch = body.match(/回复[：:]\s*\d+/);
                if (repliesMatch) body = body.slice(body.indexOf(repliesMatch[0]) + repliesMatch[0].length);
            }
            body = body.replace(/^当前位置[：:].*/, "").trim();

            // Author id: look for a /Ufield/<id> link.
            const authorLink = document.querySelector('a[href*="/Ufield/"]');
            const authorId = (authorLink?.getAttribute("href") || "").match(/\/Ufield\/(\w+)/)?.[1] || "";

            // Comments count (from the #blog_commentCount span if present).
            const commentsCount = text(document.querySelector("#blog_commentCount"));

            return {
                title,
                author,
                author_id: authorId,
                date: dateMatch ? dateMatch[1] : "",
                views: viewsMatch ? viewsMatch[1] : "",
                likes: "", // likes not rendered on the detail page; use search stats if needed
                comments: commentsCount,
                body,
            };
        });

        if (!doc.body) {
            throw new EmptyResultError("huawei-3ms", `No body rendered for docId ${docId}. The document may be deleted, access-restricted, or the page markup may have changed — inspect with \`opencli browser huawei-3ms state\`.`);
        }

        return {
            title: String(doc.title || "").trim(),
            author: String(doc.author || "").trim(),
            author_id: String(doc.author_id || "").trim(),
            date: String(doc.date || "").trim(),
            views: String(doc.views || "").trim(),
            likes: String(doc.likes || "").trim(),
            comments: String(doc.comments || "").trim(),
            body: String(doc.body || "").trim(),
            // Comments are lazy-loaded (widget/iframe) on 3MS detail pages and
            // often not rendered on a cold navigation — left empty rather than
            // risk scraping partial/stale markup.
            comments_thread: [],
            url: detailUrl,
        };
    },
});

/**
 * Resolve the `doc_id` arg into { docId, detailUrl }. Accepts a full detail URL
 * (`https://3ms.huawei.com/km/groups/<gid>/blogs/details/<id>`) — used as-is,
 * since 3MS requires the group id in the path. A bare numeric id is rejected
 * with a pointer to `search`'s `detail_url` (the group id can't be recovered
 * from a bare id: the group-less URL redirects to the user profile, and
 * searching the numeric id as text doesn't surface the doc).
 */
async function resolveDetailUrl(page, raw) {
    // Full URL: extract docId + use as-is.
    if (raw.includes("://") || raw.includes("/details/")) {
        const m = raw.match(/\/details\/(\d+)/);
        if (m) return { docId: m[1], detailUrl: raw.startsWith("http") ? raw : BASE_URL + raw };
        throw new ArgumentError(`Could not read a docId from URL: ${raw}`);
    }
    // Bare id: 3MS detail URLs require the group id
    // (/km/groups/<gid>/blogs/details/<id>); the group-less form redirects to
    // the user profile, and searching the numeric id as text doesn't surface
    // the doc. So a bare id can't be resolved without the gid — ask for the
    // full detail_url (which `search` returns).
    throw new ArgumentError(
        `3MS read needs the full detail URL (it carries the group id that the detail route requires). ` +
        `Run \`opencli huawei-3ms search "<query>"\` and pass the result's \`detail_url\` to read, e.g. ` +
        `opencli huawei-3ms read "https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113". ` +
        `Got bare id: ${raw}`,
    );
}
