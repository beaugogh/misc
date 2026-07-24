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
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://3ms.huawei.com';
const DOMAIN = '3ms.huawei.com';

// Footer markers that mark where the article body ends and page chrome
// (classification labels, comment form, prev/next nav, site footer) begins.
// The body is cut at the earliest marker that appears.
const FOOTER_MARKERS = [
    '多维分类', '分类：日常活动', '推荐度', '我来推荐', '印象：', '发表评论',
    'Tag：', '[Edit]Category', 'Share (', 'Favorite (', 'Praises (',
    'Previous：', 'Next：', '人在这个团队内', '关于3MS+', '用户协议', '知识服务服务中心',
];

// How long (seconds) to wait for the body to render after navigation.
const RENDER_WAIT_S = 5;

/**
 * Cut page-chrome noise off the end of a scraped body. The detail containers
 * (#content-body for blogs, .detail-content for wikis) render the article body
 * followed by classification labels, the comment form, prev/next nav, and the
 * site footer — none of which is article content. Cut at the earliest footer
 * marker. Also collapses runs of blank lines.
 */
function stripFooter(s: string): string {
    let cut = s.length;
    for (const m of FOOTER_MARKERS) {
        const i = s.indexOf(m);
        if (i >= 0 && i < cut) cut = i;
    }
    return s.slice(0, cut).replace(/\n{3,}/g, '\n\n').trim();
}

/**
 * Poll the body container's text length until it stops growing (or the max
 * polls are hit). The body element appears before its content is fully
 * populated — without this, a cold navigation can scrape a half-rendered body
 * (e.g. just the title before the attachment list streams in).
 */
async function waitForBodyStable(page: any, selector: string): Promise<void> {
    const len = (await page.evaluate((sel: string) => {
        const el = document.querySelector(sel);
        return el ? (el.textContent || '').trim().length : 0;
    }, selector).catch(() => 0)) as number;
    let prev = typeof len === 'number' ? len : 0;
    for (let i = 0; i < 4; i++) {
        await page.wait('time', 1).catch(() => {});
        const next = (await page.evaluate((sel: string) => {
            const el = document.querySelector(sel);
            return el ? (el.textContent || '').trim().length : 0;
        }, selector).catch(() => 0)) as number;
        const n = typeof next === 'number' ? next : 0;
        if (n === prev) break; // stable
        prev = n;
    }
}

/**
 * Wait for the body container to exist AND have non-trivial content. Polls up
 * to ~20s. A plain `page.wait('selector', ...)` resolves against stale markup
 * from the previous page (the SPA doesn't clear #content-body between routes),
 * so this checks the *article* text length — the text between the meta block
 * and the footer markers — not the raw container length. The footer
 * (多维分类…) can render before the article body streams in, so a raw-length
 * check would pass on a title+footer-only state; this waits for real article
 * content.
 */
/**
 * Compute the article-body length (text between the meta prefix and the footer
 * markers) in the body container. Used to decide whether the body has real
 * content or is still title-only (which happens when the blog attachment-list
 * XHR hasn't fired).
 */
function articleBodyLenJs(sel: string, marker: string): number {
    if (!location.href.includes(marker)) return 0;
    const el = document.querySelector(sel);
    if (!el) return 0;
    let raw = (el.textContent || '').trim();
    const editMatch = raw.match(/最近编辑时间[：:]\s*\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?\s*/);
    if (editMatch) raw = raw.slice(raw.indexOf(editMatch[0]) + editMatch[0].length);
    const markers = ['多维分类', '分类：日常活动', '推荐度', 'Tag：', '[Edit]Category', 'Share (', 'Previous：', 'Next：'];
    let cut = raw.length;
    for (const m of markers) { const j = raw.indexOf(m); if (j >= 0 && j < cut) cut = j; }
    return raw.slice(0, cut).trim().length;
}

/**
 * Wait for the body container to render WITH content. Polls up to ~25s. A plain
 * `page.wait('selector', ...)` resolves against stale markup from the previous
 * page (the SPA doesn't clear #content-body between routes), so this checks the
 * *article* text length — the text between the meta block and the footer
 * markers — not the raw container length. The footer (多维分类…) can render
 * before the article body streams in, so a raw-length check would pass on a
 * title+footer-only state; this waits for real article content.
 */
async function waitForBody(page: any, selector: string, type: string): Promise<void> {
    const urlMarker = type === 'wiki' ? 'wiki_' : (type === 'doc' ? '/docinfo/' : '/details/');
    for (let i = 0; i < 25; i++) {
        const len = (await page.evaluate(articleBodyLenJs, selector, urlMarker).catch(() => 0)) as number;
        if (typeof len === 'number' && len > 80) return;
        await page.wait('time', 1).catch(() => {});
    }
}

cli({
    site: 'huawei-3ms',
    name: 'read',
    access: 'read',
    description: 'Read the full content of a single 3MS document by its detail URL (a blog /km/groups/<gid>/blogs/details/<id> or wiki /hi/group/<gid>/wiki_<id>.html URL — take it from a search result\'s detail_url). Returns the complete document body plus title, author, date, views/likes/comments. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'doc_id', positional: true, required: true, help: 'The full 3ms.huawei.com detail URL from a search result\'s detail_url — a blog URL (https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113) or wiki URL (http://3ms.huawei.com/hi/group/3591759/wiki_7433309.html). A bare numeric id is not accepted (3MS detail URLs require the group id).' },
    ],
    columns: ['title', 'author', 'author_id', 'date', 'views', 'likes', 'comments', 'body', 'comments_thread', 'url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-3ms read');

        const raw = String(kwargs.doc_id || '').trim();
        if (!raw) throw new ArgumentError('huawei-3ms read doc_id cannot be empty');

        // Resolve to a full detail URL + resource type (blog or wiki). A full
        // URL is used as-is; a bare docId is rejected (3MS detail URLs require
        // the group id, which a bare id doesn't carry).
        const { docId, detailUrl, type } = await resolveDetailUrl(page, raw);

        // Navigate to the detail page (SSO-gated; the bridge drives the
        // logged-in Chrome tab). Match the bridge `open` command's call
        // (page.goto with default options) — passing waitUntil/settleMs here
        // changed the load behavior on 3MS blog pages (the attachment-list XHR
        // didn't fire, leaving the body title-only).
        await page.goto(detailUrl);
        const bodySelector = type === 'wiki' ? '.detail-content' : (type === 'doc' ? '#root, .content' : '#content-body');
        // Wait for the body container to render WITH content. A bare selector
        // wait races the SPA, so poll for a non-trivial article-body length,
        // then let it stabilize.
        await waitForBody(page, bodySelector, type);
        await page.wait('time', RENDER_WAIT_S).catch(() => {});
        await waitForBodyStable(page, bodySelector);

        // Auth gate.
        const authOk = await page.evaluate((sel: string) => {
            const body = document.querySelector(sel);
            const hasLoginPrompt = /请登录|sign\s*in/i.test(document.documentElement.outerHTML) && !body;
            return !!body || !hasLoginPrompt;
        }, bodySelector);
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, '3MS requires a logged-in session. Open https://3ms.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }

        // Scrape the rendered detail content. Blog and wiki detail pages have
        // different markup, so branch on type (all extraction in-page).
        const doc = await page.evaluate((resourceType: string) => {
            const text = (el: Element | null | undefined): string => (el?.textContent || '').trim();

            // ---- Doc detail page (/documents/docinfo/<id> → "3MS文档库").
            // Body in #root; these pages are mostly attachment pointers, so the
            // body is short (title + meta + attachment list). Strip the nav
            // prefix and the trailing chrome (历史版本/基本信息/评论列表). ----
            if (resourceType === 'doc') {
                const bodyEl = document.querySelector('#root') || document.querySelector('.content');
                const raw = text(bodyEl);
                const title = (document.title || '').split(/\s*-\s*3MS文档库/)[0].split(/\s*-\s*/)[0].trim();
                // Body: from "更新摘要：" (or the title echo) to the trailing chrome.
                let body = raw;
                const summaryIdx = body.indexOf('更新摘要');
                if (summaryIdx >= 0) body = body.slice(summaryIdx);
                const cutIdx = body.search(/历史版本|基本信息|上架信息|评论列表/);
                if (cutIdx >= 0) body = body.slice(0, cutIdx);
                const pageText = document.body.innerText;
                const viewsMatch = pageText.match(/浏览[：:]\s*(\d+)/) || pageText.match(/浏览\s*(\d+)/);
                const dateMatch = pageText.match(/20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}/);
                const authorLink = document.querySelector('a[href*="/Ufield/"]');
                return {
                    title,
                    author: '',
                    author_id: (authorLink?.getAttribute('href') || '').match(/\/Ufield\/(\w+)/)?.[1] || '',
                    date: dateMatch ? dateMatch[0] : '',
                    views: viewsMatch ? viewsMatch[1] : '',
                    likes: '',
                    comments: '',
                    body: body.trim(),
                };
            }

            // ---- Wiki detail page (/hi/group/<gid>/wiki_<id>.html → redirects
            // to /next/groups/index.html#/wiki/detail). Body in .detail-content,
            // which starts with "<title>Summary：..." — strip that prefix. ----
            if (resourceType === 'wiki') {
                const bodyEl = document.querySelector('.detail-content') || document.querySelector('.content');
                const raw = text(bodyEl);
                const title = (document.title || '').split(/\s*-\s*(Huawei Cloud|3ms)/i)[0].trim();
                // Body: drop leading "<title>目录[Show All]" and "Summary："
                // prefixes that the wiki detail-content prepends.
                let body = raw
                    .replace(/^[^\n]*?目录\[Show All\]/, '')
                    .replace(/^[^\n]*?Summary[：:]/, '')
                    .trim();
                const pageText = document.body.innerText;
                const viewsMatch = pageText.match(/浏览[：:]\s*(\d+)/);
                const dateMatch = pageText.match(/20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}/);
                const authorLink = document.querySelector('a[href*="/Ufield/"]');
                return {
                    title,
                    author: '',
                    author_id: (authorLink?.getAttribute('href') || '').match(/\/Ufield\/(\w+)/)?.[1] || '',
                    date: dateMatch ? dateMatch[0] : '',
                    views: viewsMatch ? viewsMatch[1] : '',
                    likes: '',
                    comments: '',
                    body,
                };
            }

            // ---- Blog detail page (/km/groups/<gid>/blogs/details/<id>). Body
            // in #content-body, which mixes breadcrumb + meta + article body. ----
            const bodyEl = document.querySelector('#content-body') || document.querySelector('.content');

            // Title: document.title is "<title> - <community> - 3MS知识管理社区".
            const title = (document.title || '').split(/\s*-\s*3MS知识管理社区/)[0].split(/\s*-\s*/)[0].trim();

            // The body container text mixes breadcrumb + meta + article body.
            // Parse the meta out of it, then take the article body as the text
            // after the meta block.
            const raw = text(bodyEl);
            const authorMatch = raw.match(/楼主\s*([^\s]+)\s*等级/);
            const author = authorMatch ? authorMatch[1] : '';
            const dateMatch = raw.match(/日期[：:]\s*(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)/);
            const viewsMatch = raw.match(/浏览[：:]\s*(\d+)/);

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
            body = body.replace(/^当前位置[：:].*/, '').trim();

            // Author id: look for a /Ufield/<id> link.
            const authorLink = document.querySelector('a[href*="/Ufield/"]');
            const authorId = (authorLink?.getAttribute('href') || '').match(/\/Ufield\/(\w+)/)?.[1] || '';

            // Comments count (from the #blog_commentCount span if present).
            const commentsCount = text(document.querySelector('#blog_commentCount'));

            return {
                title,
                author,
                author_id: authorId,
                date: dateMatch ? dateMatch[1] : '',
                views: viewsMatch ? viewsMatch[1] : '',
                likes: '', // likes not rendered on the detail page; use search stats if needed
                comments: commentsCount,
                body,
            };
        }, type);

        if (!doc.body) {
            throw new EmptyResultError('huawei-3ms', `No body rendered for docId ${docId}. The document may be deleted, access-restricted, or the page markup may have changed — inspect with \`opencli browser huawei-3ms state\`.`);
        }

        return {
            title: String(doc.title || '').trim(),
            author: String(doc.author || '').trim(),
            author_id: String(doc.author_id || '').trim(),
            date: String(doc.date || '').trim(),
            views: String(doc.views || '').trim(),
            likes: String(doc.likes || '').trim(),
            comments: String(doc.comments || '').trim(),
            body: stripFooter(String(doc.body || '')),
            // Comments are lazy-loaded (widget/iframe) on 3MS detail pages and
            // often not rendered on a cold navigation — left empty rather than
            // risk scraping partial/stale markup.
            comments_thread: [],
            url: detailUrl,
        };
    },
});

/**
 * Resolve the `doc_id` arg into { docId, detailUrl, type }. Accepts a full
 * detail URL — blog (`/km/groups/<gid>/blogs/details/<id>`) or wiki
 * (`/hi/group/<gid>/wiki_<id>.html`) — used as-is, since 3MS requires the group
 * id in the path. A bare numeric id is rejected with a pointer to `search`'s
 * `detail_url` (the group id can't be recovered from a bare id: the group-less
 * blog URL redirects to the user profile, and searching the numeric id as text
 * doesn't surface the doc).
 */
async function resolveDetailUrl(page: any, raw: string): Promise<{ docId: string; detailUrl: string; type: string }> {
    // Wiki URL: /hi/group/<gid>/wiki_<id>.html
    const wikiM = raw.match(/wiki_(\d+)\.html/);
    if (wikiM) return { docId: wikiM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'wiki' };
    // Doc URL: /documents/docinfo/<id>  (document library)
    const docM = raw.match(/\/documents\/docinfo\/(\d+)/);
    if (docM) return { docId: docM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'doc' };
    // Blog URL: /km/groups/<gid>/blogs/details/<id>
    if (raw.includes('://') || raw.includes('/details/')) {
        const m = raw.match(/\/details\/(\d+)/);
        if (m) return { docId: m[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'blog' };
        throw new ArgumentError(`Could not read a docId from URL: ${raw}`);
    }
    // Bare id: rejected (see doc comment).
    throw new ArgumentError(
        `3MS read needs the full detail URL (it carries the group id that the detail route requires). ` +
        `Run \`opencli huawei-3ms search "<query>"\` and pass the result's \`detail_url\` to read, e.g. ` +
        `opencli huawei-3ms read "https://3ms.huawei.com/km/groups/3059465/blogs/details/22436113". ` +
        `Got bare id: ${raw}`,
    );
}
