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
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://3ms.huawei.com';
const DOMAIN = '3ms.huawei.com';

// The search app route. The query goes in the `text` query param.
const SEARCH_PATH = '/doc3ms/index.html';

// CSS selector for the MAIN search-results list. The page also renders sidebar
// "相关社区" / recommendation cards as .ant-list-item — scoping to the main
// results list (.list___1nr2P) excludes them. Its header reads "共N个结果".
const RESULTS_LIST_SELECTOR = '.ant-list.list___1nr2P';
// Items inside the main list. Each is .ant-list-item plus a type class:
//   .blog  → /km/groups/<gid>/blogs/details/<docId>
//   .wiki  → /hi/group/<gid>/wiki_<docId>.html
//   .frameItem___2tD0c → external link, no docId (skip)
//   (no 2nd class)     → "相关搜索" related-searches block (skip)
const CARD_SELECTOR = '.ant-list-item';

// How long (seconds) to wait for results to render after clicking search.
const RENDER_WAIT_S = 5;

// The search tabs (scopes). The `type` query param selects the scope.
const TABS: Record<string, string> = {
    community: 'community',
    doc: 'doc',
    blog: 'blog',
    expert: 'expert',
    know: 'know',
    external: 'external',
};

cli({
    site: 'huawei-3ms',
    name: 'search',
    access: 'read',
    description: 'Search Huawei\'s 3MS 知识管理社区 (3ms.huawei.com). Given an arbitrary question, returns the top N most relevant documents (title, type, author, source, date, summary, doc_id, detail_url). Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'query', positional: true, required: true, help: 'Your question or search term (e.g. "盘古平台", "5G架构演进")' },
        { name: 'limit', type: 'int', default: 10, help: 'Max number of documents to return (N)' },
        { name: 'tab', default: 'community', help: 'Search scope/tab: community | doc | blog | expert | know | external' },
    ],
    columns: ['rank', 'title', 'type', 'author', 'author_id', 'source', 'date', 'views', 'likes', 'comments', 'summary', 'doc_id', 'detail_url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-3ms search');

        const query = String(kwargs.query || '').trim();
        if (!query) throw new ArgumentError('huawei-3ms search query cannot be empty');

        const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));
        const tab = TABS[String(kwargs.tab || 'community')] || 'community';

        // Navigate to the search app with the query in the URL. The app reads
        // `text` and runs the search on load — no input-filling needed for the
        // initial query. (Re-searching within the page fills input.ant-input +
        // clicks button.ant-input-search-button; not needed here.)
        const searchUrl = `${BASE_URL}${SEARCH_PATH}?type=${tab}&l=zh&text=${encodeURIComponent(query)}#/`;
        await page.goto(searchUrl, { waitUntil: 'load', settleMs: 1500 });
        // Wait for the MAIN results list to render. The search app is an SPA
        // that fetches results after load, so wait on the selector (with a time
        // fallback) — a bare time wait races the fetch.
        await page.wait('selector', RESULTS_LIST_SELECTOR).catch(() => {});
        await page.wait('time', RENDER_WAIT_S).catch(() => {});

        // Auth gate: a logged-in page renders result cards or the search UI;
        // a gated page shows a login/SSO prompt instead.
        const authOk = await page.evaluate(() => {
            const hasUser = !!document.querySelector('[class*=avatar],[class*=user-info]') || /b\d{8}|w\d{8}|s\d{8}/.test(document.body.innerText || '');
            const hasLoginPrompt = /请登录|sign\s*in/i.test(document.documentElement.outerHTML) && !hasUser;
            return hasUser || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, '3MS requires a logged-in session. Open https://3ms.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }

        // Scrape the real search results from the MAIN results list. Each
        // knowledge-document result has a link whose pattern reveals its type:
        //   blog → /km/groups/<gid>/blogs/details/<docId>
        //   wiki → /hi/group/<gid>/wiki_<docId>.html
        // Sidebar "相关社区" cards and the "相关搜索" block live outside this
        // list (or have no docId link) — scoping to the main list + requiring a
        // docId-bearing link excludes them.
        const docs = await page.evaluate((listSelector: string, max: number) => {
            const text = (el: Element | null | undefined): string => (el?.textContent || '').trim();
            const stripEm = (s: string): string => s.replace(/<[^>]+>/g, '').trim();
            const list = document.querySelector(listSelector);
            if (!list) return [];
            const nodes = Array.from(list.querySelectorAll('.ant-list-item')).slice(0, max);
            return nodes.map((card) => {
                // type = 2nd class on the card (blog / wiki / frameItem / none)
                const cls = card.className.split(/\s+/).filter((c) => c !== 'ant-list-item');
                const type = cls[0] || '';
                // Find the doc-bearing link: blog (/details/) or wiki (wiki_<id>.html).
                const blogLink = card.querySelector('a[href*="/blogs/details/"]');
                const wikiLink = card.querySelector('a[href*="wiki_"]');
                const link = blogLink || wikiLink;
                if (!link) return null; // frameItem (external) or 相关搜索 block
                const href = link.getAttribute('href') || '';
                const blogMatch = href.match(/\/blogs\/details\/(\d+)/);
                const wikiMatch = href.match(/wiki_(\d+)\.html/);
                const docId = (blogMatch?.[1] || wikiMatch?.[1] || '');
                if (!docId) return null;
                const resourceType = blogMatch ? 'blog' : (wikiMatch ? 'wiki' : type);
                // Title: prefer .title_em___2OVTv (clean, no "浏览 N" suffix);
                // fall back to the link's title attr / text.
                const titleEm = card.querySelector('.title_em___2OVTv');
                const titleAttr = stripEm(link.getAttribute('title') || '');
                const titleText = stripEm(link.textContent || '');
                const title = stripEm((titleEm?.textContent || '')) || titleAttr || titleText;
                // detail url (absolute)
                const detailUrl = href.startsWith('http') ? href : (href.startsWith('/') ? BASE_URL + href : BASE_URL + '/' + href);
                // author: a[href^="/Ufield/"] → author id
                const authorLink = card.querySelector('a[href^="/Ufield/"]');
                const authorText = text(authorLink);
                const authorId = (authorLink?.getAttribute('href') || '').match(/\/Ufield\/(\w+)/)?.[1] || '';
                // source community: the wikis.html / group link
                const sourceLink = card.querySelector('a[href*="/hi/group/"][href*="wikis.html"], a[href*="/hi/group/"]');
                const source = text(sourceLink);
                // views: .titleRight___2MXLQ ("浏览 N")
                const viewsText = text(card.querySelector('.titleRight___2MXLQ, [class*=view], [class*=browse]'));
                const viewsNum = (viewsText.match(/(\d[\d,]*)/) || [])[1] || '';
                // summary
                const summary = text(card.querySelector('.ant-list-item-meta-description, [class*=summary],[class*=desc],[class*=abstract]'));
                return {
                    title,
                    type: resourceType,
                    author: authorText,
                    author_id: authorId,
                    source,
                    views: viewsNum,
                    summary,
                    doc_id: docId,
                    detail_url: detailUrl,
                };
            }).filter((r: any) => r && r.title && r.doc_id);
        }, RESULTS_LIST_SELECTOR, limit);

        if (!docs.length) {
            throw new EmptyResultError('huawei-3ms', `No results parsed for "${query}". Try a different keyword or tab, or inspect the page with \`opencli browser huawei-3ms state\`.`);
        }

        // Enrich with stats (views/likes/comments) via the stats API. The API
        // is type-specific: blog ids use moduleType=blog, wiki ids use
        // moduleType=wiki. Best-effort — if it fails, stats stay empty (the
        // card's own "浏览 N" already gave us views as a fallback).
        const blogIds = docs.filter((d: any) => d.type === 'blog').map((d: any) => d.doc_id);
        const wikiIds = docs.filter((d: any) => d.type === 'wiki').map((d: any) => d.doc_id);
        const [blogStats, wikiStats] = await Promise.all([
            fetchStats(page, 'blog', blogIds),
            fetchStats(page, 'wiki', wikiIds),
        ]);
        const stats = { ...blogStats, ...wikiStats };

        return docs.slice(0, limit).map((item: any, index: number) => {
            const s = stats[item.doc_id] || {};
            return {
                rank: index + 1,
                title: String(item.title || '').trim(),
                type: String(item.type || '').trim(),
                author: String(item.author || '').trim(),
                author_id: String(item.author_id || '').trim(),
                source: String(item.source || '').trim(),
                date: String(item.date || '').trim(),
                views: String(s.views || '').trim(),
                likes: String(s.likes || '').trim(),
                comments: String(s.comments || '').trim(),
                summary: String(item.summary || '').trim(),
                doc_id: String(item.doc_id || '').trim(),
                detail_url: String(item.detail_url || '').trim(),
            };
        });
    },
});

/**
 * Fetch views/likes/comments for a batch of docIds of ONE resource type via the
 * 3MS stats API. Returns a map { docId: {views, likes, comments} }. Best-effort:
 * on any failure returns an empty map (the search still returns, just without
 * stats).
 *
 * The endpoint: GET /api/projectspace/1-2-4/v1/statistics?moduleType=<blog|wiki>&resourceIds=<csv>
 * Returns: [{ resourceId, views, likes, comments, collections, attach }]
 */
async function fetchStats(page: any, moduleType: string, docIds: string[]): Promise<Record<string, { views: string; likes: string; comments: string }>> {
    if (!docIds.length) return {};
    try {
        const csv = docIds.join(',');
        const json = await page.evaluate(async (url: string) => {
            const r = await fetch(url, { credentials: 'include' });
            const t = await r.text();
            return t;
        }, `${BASE_URL}/api/projectspace/1-2-4/v1/statistics?moduleType=${moduleType}&resourceIds=${encodeURIComponent(csv)}`);
        const arr = JSON.parse(json);
        const out: Record<string, { views: string; likes: string; comments: string }> = {};
        for (const item of Array.isArray(arr) ? arr : []) {
            out[String(item.resourceId)] = {
                views: String(item.views ?? ''),
                likes: String(item.likes ?? ''),
                comments: String(item.comments ?? ''),
            };
        }
        return out;
    } catch {
        return {};
    }
}
