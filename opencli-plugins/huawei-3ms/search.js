/**
 * Search Huawei's 3MS 知识管理社区 (3ms.huawei.com) — Huawei's knowledge-management
 * community (blogs, docs, forums, experts, courses).
 *
 * Input: an arbitrary question/query. Output: the top N most relevant documents,
 * each with title, type, author, source, date, summary, and a detail URL/docId.
 * The detail URL is a real <a href> in the rendered card, so the docId is
 * directly available (unlike 稼先社区, which needed a window.open intercept).
 *
 * Strategy: COOKIE — the site is a Vue SPA (Element/Ant Design) behind Huawei SSO.
 * The adapter drives the logged-in Chrome tab to the dedicated search app
 * (`/doc3ms/index.html?...&text=<query>#/`), fills the search input + clicks the
 * search button (in-page — the bridge's click doesn't dispatch real events), and
 * scrapes the rendered `.ant-list-item` result cards from the page context.
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - search app:    /doc3ms/index.html?type=community&l=zh&text=<urlencoded>#/
 *   - search input:  input.ant-input  (placeholder "请输入关键词搜索")
 *   - search button: button.ant-input-search-button  (text "搜 索")
 *   - result card:   .ant-list-item  (e.g. .ant-list-item.blog)
 *   - type:          the card's 2nd class (blog / doc / forum / …)
 *   - title+url:     .ant-list-item-meta-title a[href]  (href has /blogs/details/<docId>;
 *                    the `title` attr has the full title — strip <em> highlight tags)
 *   - author:        a[href^="/Ufield/"]  (href "/Ufield/w00454454" → author id w00454454)
 *   - source:        a[href*="/hi/group/"]  (the originating community)
 *
 * The stats API (`/api/projectspace/1-2-4/v1/statistics?moduleType=blog&resourceIds=<csv>`)
 * returns views/likes/comments per docId — called for the visible results to
 * enrich the cards (which don't render counts inline).
 *
 * NOTE: hand-mirrored from search.ts (no build step). Keep the two in sync.
 */

import { cli, Strategy } from "@jackwener/opencli/registry";
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from "@jackwener/opencli/errors";

const BASE_URL = "https://3ms.huawei.com";
const DOMAIN = "3ms.huawei.com";

// The search app route. The query goes in the `text` query param.
const SEARCH_PATH = "/doc3ms/index.html";

// CSS selector for a rendered result card.
const CARD_SELECTOR = ".ant-list-item";

// How long (seconds) to wait for results to render after clicking search.
const RENDER_WAIT_S = 5;

// The search tabs (scopes). The `type` query param selects the scope.
const TABS = {
    community: "community",
    doc: "doc",
    blog: "blog",
    expert: "expert",
    know: "know",
    external: "external",
};

cli({
    site: "huawei-3ms",
    name: "search",
    access: "read",
    description: "Search Huawei's 3MS 知识管理社区 (3ms.huawei.com). Given an arbitrary question, returns the top N most relevant documents (title, type, author, source, date, summary, doc_id, detail_url). Requires a logged-in Huawei session via the OpenCLI Browser Bridge.",
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: "query", positional: true, required: true, help: 'Your question or search term (e.g. "盘古平台", "5G架构演进")' },
        { name: "limit", type: "int", default: 10, help: "Max number of documents to return (N)" },
        { name: "tab", default: "community", help: "Search scope/tab: community | doc | blog | expert | know | external" },
    ],
    columns: ["rank", "title", "type", "author", "author_id", "source", "date", "views", "likes", "comments", "summary", "doc_id", "detail_url"],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError("Browser session required for huawei-3ms search");

        const query = String(kwargs.query || "").trim();
        if (!query) throw new ArgumentError("huawei-3ms search query cannot be empty");

        const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));
        const tab = TABS[String(kwargs.tab || "community")] || "community";

        // Navigate to the search app with the query in the URL. The app reads
        // `text` and runs the search on load — no input-filling needed for the
        // initial query. (Re-searching within the page fills input.ant-input +
        // clicks button.ant-input-search-button; not needed here.)
        const searchUrl = `${BASE_URL}${SEARCH_PATH}?type=${tab}&l=zh&text=${encodeURIComponent(query)}#/`;
        await page.goto(searchUrl);
        // Wait for result cards to render. The search app is an SPA that
        // fetches results after load, so wait on the selector (with a time
        // fallback) — a bare time wait races the fetch.
        await page.wait("selector", CARD_SELECTOR).catch(() => {});
        await page.wait("time", RENDER_WAIT_S).catch(() => {});

        // Auth gate: a logged-in page renders result cards or the search UI;
        // a gated page shows a login/SSO prompt instead.
        const authOk = await page.evaluate(() => {
            const hasUser = !!document.querySelector('[class*=avatar],[class*=user-info]') || /b\d{8}|w\d{8}|s\d{8}/.test(document.body.innerText || "");
            const hasLoginPrompt = /请登录|sign\s*in/i.test(document.documentElement.outerHTML) && !hasUser;
            return hasUser || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, "3MS requires a logged-in session. Open https://3ms.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.");
        }

        // Scrape the rendered result cards. Each knowledge-document card has a
        // real <a href> with /details/<docId> in the main DOM (not iframed).
        // The community tab mixes in iframe-based service/product cards
        // (.ant-list-item.iotItem) with no details link — filter to cards that
        // HAVE a /details/ link so only knowledge documents are returned.
        const docs = await page.evaluate((selector, max) => {
            const text = (el) => (el?.textContent || "").trim();
            const stripEm = (s) => s.replace(/<[^>]+>/g, "").trim();
            const nodes = Array.from(document.querySelectorAll(selector))
                .filter((card) => !!card.querySelector('a[href*="/details/"]'))
                .slice(0, max);
            return nodes.map((card) => {
                // type = 2nd class on the card (e.g. .ant-list-item.blog → "blog")
                const cls = card.className.split(/\s+/).filter((c) => c !== "ant-list-item");
                const type = cls[0] || "";
                // title + detail url + docId from the title link
                const titleLink = card.querySelector(".ant-list-item-meta-title a[href], .title a[href], h3 a[href], h4 a[href]");
                const titleAttr = stripEm(titleLink?.getAttribute("title") || "");
                const titleText = stripEm(titleLink?.textContent || "");
                const detailUrl = titleLink?.getAttribute("href") || "";
                const docIdMatch = detailUrl.match(/\/details\/(\d+)/);
                const docId = docIdMatch ? docIdMatch[1] : "";
                // author: a[href^="/Ufield/"] → author id
                const authorLink = card.querySelector('a[href^="/Ufield/"]');
                const authorText = text(authorLink);
                const authorId = (authorLink?.getAttribute("href") || "").match(/\/Ufield\/(\w+)/)?.[1] || "";
                // source community: a[href*="/hi/group/"]
                const sourceLink = card.querySelector('a[href*="/hi/group/"]');
                const source = text(sourceLink);
                // date + views may be inline in the meta text
                const metaText = text(card.querySelector(".ant-list-item-meta-content"));
                const dateMatch = metaText.match(/20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}/);
                // summary: any description/abstract element
                const summary = text(card.querySelector("[class*=summary],[class*=desc],[class*=abstract]"));
                return {
                    title: titleAttr || titleText,
                    type,
                    author: authorText,
                    author_id: authorId,
                    source,
                    date: dateMatch ? dateMatch[0] : "",
                    summary,
                    doc_id: docId,
                    detail_url: detailUrl.startsWith("http") ? detailUrl : (detailUrl ? BASE_URL + detailUrl : ""),
                };
            }).filter((r) => r.title && r.doc_id);
        }, CARD_SELECTOR, limit);

        if (!docs.length) {
            throw new EmptyResultError("huawei-3ms", `No results parsed for "${query}". Try a different keyword or tab, or inspect the page with \`opencli browser huawei-3ms state\`.`);
        }

        // Enrich with stats (views/likes/comments) via the stats API, batching
        // the docIds. Best-effort — if it fails, stats stay empty.
        const stats = await fetchStats(page, docs.map((d) => d.doc_id));

        return docs.slice(0, limit).map((item, index) => {
            const s = stats[item.doc_id] || {};
            return {
                rank: index + 1,
                title: String(item.title || "").trim(),
                type: String(item.type || "").trim(),
                author: String(item.author || "").trim(),
                author_id: String(item.author_id || "").trim(),
                source: String(item.source || "").trim(),
                date: String(item.date || "").trim(),
                views: String(s.views || "").trim(),
                likes: String(s.likes || "").trim(),
                comments: String(s.comments || "").trim(),
                summary: String(item.summary || "").trim(),
                doc_id: String(item.doc_id || "").trim(),
                detail_url: String(item.detail_url || "").trim(),
            };
        });
    },
});

/**
 * Fetch views/likes/comments for a batch of docIds via the 3MS stats API.
 * Returns a map { docId: {views, likes, comments} }. Best-effort: on any
 * failure returns an empty map (the search still returns, just without stats).
 *
 * The endpoint: GET /api/projectspace/1-2-4/v1/statistics?moduleType=blog&resourceIds=<csv>
 * Returns: [{ resourceId, views, likes, comments, collections, attach }]
 */
async function fetchStats(page, docIds) {
    if (!docIds.length) return {};
    try {
        const csv = docIds.join(",");
        const json = await page.evaluate(async (url) => {
            const r = await fetch(url, { credentials: "include" });
            const t = await r.text();
            return t;
        }, `${BASE_URL}/api/projectspace/1-2-4/v1/statistics?moduleType=blog&resourceIds=${encodeURIComponent(csv)}`);
        const arr = JSON.parse(json);
        const out = {};
        for (const item of Array.isArray(arr) ? arr : []) {
            out[String(item.resourceId)] = {
                views: String(item.views ?? ""),
                likes: String(item.likes ?? ""),
                comments: String(item.comments ?? ""),
            };
        }
        return out;
    } catch {
        return {};
    }
}
