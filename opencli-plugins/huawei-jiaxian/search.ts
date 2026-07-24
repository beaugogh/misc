/**
 * Search Huawei's 稼先社区 (jx.huawei.com) — the internal expert and engineer
 * knowledge community.
 *
 * Input: an arbitrary question/query. Output: the top N most relevant posts,
 * each with title, type, author, date, and a rich summary (author + abstract +
 * expert viewpoints). The summaries are long (often 1,000–4,000 chars) and
 * carry enough substance for a downstream agent or reader to triage the
 * question. For one post's full article body, use `read <postId>`.
 *
 * Strategy: COOKIE — the site is a Vue SPA behind Huawei SSO. The adapter
 * drives the logged-in Chrome tab to the dedicated search-results route
 * (`/searchResult?searchKey=<query>&search=true`), which renders ranked
 * full-text-search result cards server-side, and scrapes them from the page
 * context.
 *
 * Why /searchResult and not the homepage search box: the homepage "search" is
 * actually a filtered recommendation feed (card class
 * `.recommended-page-list-item` surfaced on the homepage), whose ranking
 * differs from — and is less relevant than — the real full-text search at
 * /searchResult. The /searchResult route is what a logged-in human sees when
 * they search, and is the on-topic result set. (Switched after a quality bug:
 * the homepage surfaced an off-topic daily briefing for "华为云AI痛点" while
 * /searchResult ranked the actual 痛点 posts first.)
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - results route:  /searchResult?searchKey=<urlencoded>&search=true
 *   - result card:    .recommended-page-list-item
 *   - type:           .result-page-content-type-item   (思想简报 / 自由讨论 / …)
 *   - title:          .contention-page-content-title
 *   - rich summary:   .contention-page-content-summary  (textContent is the
 *                     full summary — 1k–4k chars; strip the leading
 *                     "查看原帖或评论，请访问原帖>>" nav prefix)
 *   - author:         .author-name   date: .create-time
 *   - views/replies:  not rendered on /searchResult cards (left empty)
 *
 * postId extraction: clicking a card's inner `.contention-page-content` fires
 * `window.open('/community/comgroup/postsDetails?postId=<id>…')` (a new tab).
 * The adapter intercepts window.open in-page, clicks each card, and reads the
 * postId + resource type from the captured URL — so each result carries a
 * `post_id` that `read` consumes directly. Cards whose click uses a different
 * route (思想简报 briefings, etc.) get an empty `post_id`; `read` only supports
 * free_post, so those are surfaced for triage via their summary instead.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://jx.huawei.com';
const DOMAIN = 'jx.huawei.com';

// The dedicated search-results route. The searchKey is URL-encoded in the
// query string — no box-filling or button-clicking needed, which avoids the
// Vue synthetic-event problem entirely.
const SEARCH_ROUTE = '/searchResult';

// CSS selector for a rendered result card.
const CARD_SELECTOR = '.recommended-page-list-item';

// How long (seconds) to wait for results to render after navigation.
const RENDER_WAIT_S = 5;

cli({
    site: 'huawei-jiaxian',
    name: 'search',
    access: 'read',
    description: 'Search Huawei\'s 稼先社区 (jx.huawei.com). Given an arbitrary question, returns the top N most relevant posts (title, type, author, date, rich summary). Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'query', positional: true, required: true, help: 'Your question or search term (e.g. "大模型推理优化", "5G架构演进")' },
        { name: 'limit', type: 'int', default: 10, help: 'Max number of documents to return (N)' },
        { name: 'language', default: 'cn', help: 'Source language: cn | en' },
    ],
    columns: ['rank', 'title', 'type', 'author', 'date', 'views', 'replies', 'summary', 'post_id', 'resource_type', 'url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-jiaxian search');

        const query = String(kwargs.query || '').trim();
        if (!query) throw new ArgumentError('huawei-jiaxian search query cannot be empty');

        const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));
        // `language` is accepted for interface parity with sibling plugins but
        // not consumed: the 稼先社区 SPA search has no language toggle.

        // Navigate straight to the search-results route with the query in the
        // URL. No box-filling / button-clicking — the route renders ranked
        // full-text-search results server-side.
        const searchUrl = `${BASE_URL}${SEARCH_ROUTE}?searchKey=${encodeURIComponent(query)}&search=true`;
        await page.goto(searchUrl);
        await page.wait('time', RENDER_WAIT_S).catch(() => {});

        // Auth gate: a logged-in page renders result cards; a gated page shows
        // a login/SSO prompt instead.
        const authOk = await page.evaluate(() => {
            const hasAvatar = !!(document.querySelector('[class*="avatar"]') || document.querySelector('[class*="user-info"]'));
            const hasLoginPrompt = /登录|sign\s*in/i.test(document.documentElement.outerHTML) && !hasAvatar;
            return hasAvatar || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, '稼先社区 requires a logged-in session. Open https://jx.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }

        // Scrape the rendered result cards + extract each post's postId.
        // postId extraction: clicking a card's inner `.contention-page-content`
        // fires `window.open('/community/comgroup/postsDetails?postId=<id>…')`
        // (a new tab — which is why the original tab's URL never changed and
        // why the bridge's click, which doesn't dispatch real events, can't
        // trigger it). We intercept window.open in-page, click each card's
        // inner div, and read the postId out of the captured URL. Cards whose
        // click uses a different route (e.g. 思想简报 briefings, which don't go
        // to postsDetails) get an empty post_id — `read` only supports
        // free_post anyway, so those are skipped honestly.
        const docs = await page.evaluate(async (selector: string, max: number) => {
            const text = (el: Element | null | undefined): string => (el?.textContent || '').trim();
            const stripNavPrefix = (s: string): string =>
                s.replace(/^查看原帖.*?访问原帖.*?>>\s*/, '').replace(/^查看原帖.*?>>\s*/, '').trim();
            const nodes = Array.from(document.querySelectorAll(selector)).slice(0, max);

            // Intercept window.open (return a stub so the page doesn't actually
            // open tabs / lose focus). Restore after extraction.
            const opens: string[] = [];
            const OO = window.open;
            window.open = (u?: string | URL) => { if (u) opens.push(String(u)); return { focus() {}, close() {} }; };

            const out: any[] = [];
            for (const card of nodes) {
                const typeEl = card.querySelector('.result-page-content-type-item');
                const titleEl = card.querySelector('.contention-page-content-title');
                const summaryEl = card.querySelector('.contention-page-content-summary');
                const authorEl = card.querySelector('.author-name');
                const dateEl = card.querySelector('.create-time');

                // Click the inner content div to fire window.open with the
                // detail URL, then extract postId + resource type from it.
                opens.length = 0;
                const inner = card.querySelector('.contention-page-content') as HTMLElement | null;
                inner?.click();
                await new Promise((r) => setTimeout(r, 200));
                let postId = '';
                let resourceType = '';
                for (const u of opens) {
                    const m = u.match(/postId=([0-9a-f]{32})/i);
                    if (m) { postId = m[1]; resourceType = (u.match(/type=(\w+)/) || [])[1] || ''; break; }
                }

                out.push({
                    title: text(titleEl),
                    type: text(typeEl),
                    author: text(authorEl),
                    date: text(dateEl),
                    // /searchResult cards don't render views/replies.
                    views: '',
                    replies: '',
                    // The textContent is the full summary (1k–4k chars); the
                    // `title` attribute is empty on this route. Strip the
                    // leading "查看原帖…访问原帖>>" navigation prefix.
                    summary: stripNavPrefix(text(summaryEl)),
                    post_id: postId,
                    resource_type: resourceType,
                });
            }
            window.open = OO;
            return out.filter((r) => r.title);
        }, CARD_SELECTOR, limit);

        if (!docs.length) {
            throw new EmptyResultError('huawei-jiaxian', `No results parsed for "${query}". Try a different keyword, or inspect the page with \`opencli browser huawei-jiaxian state\`.`);
        }

        return docs.slice(0, limit).map((item: any, index: number) => ({
            rank: index + 1,
            title: String(item.title || '').trim(),
            type: String(item.type || '').trim(),
            author: String(item.author || '').trim(),
            date: String(item.date || '').trim(),
            views: String(item.views || '').trim(),
            replies: String(item.replies || '').trim(),
            summary: String(item.summary || '').trim(),
            // postId for `read` (empty for non-free_post types like briefings).
            post_id: String(item.post_id || '').trim(),
            resource_type: String(item.resource_type || '').trim(),
            url: searchUrl,
        }));
    },
});

