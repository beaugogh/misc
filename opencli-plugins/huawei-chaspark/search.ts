/**
 * Search Huawei's 黄大年茶思屋 academic community (chaspark.com) — Huawei's
 * academic/paper community (papers, videos, patents, conferences).
 *
 * Input: an arbitrary question/query. Output: the top N most relevant items,
 * each with title, type, author, date, views, summary, and a detail URL/item_id.
 *
 * Strategy: COOKIE — the site is a Vue SPA behind Huawei SSO. The adapter drives
 * the logged-in Chrome tab to the search route (`#/search?keyword=<query>`),
 * fills the search input + presses Enter (in-page — the bridge's click doesn't
 * dispatch real events), and scrapes the rendered result cards.
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - search route: /#/search?keyword=<urlencoded>
 *   - search input: input.ant-input-borderless  (placeholder "搜索关键字、标题、字幕...")
 *   - result item:  [class*=style_m_][class*=Item]  (e.g. style_m_videoItem__,
 *                    style_m_paperItem__). EXCLUDE style_m_trackItem__ — those
 *                    are video transcript segments (timestamp + text), not
 *                    separate results.
 *   - type:         the style_m_<type>Item__ class → video / paper / live / …
 *   - title+url:    .style_m_title__jA-1d a[href]  (href is #/stw/media/<id>,
 *                    #/research/paper/<id>, or #/live/<id>; the <id> is the
 *                    item_id, with an optional ?anchorV=<id> query suffix)
 *   - author/date/views/summary: not consistently present on every card type
 *                    (video cards embed the player, polluting the text); parsed
 *                    best-effort from the card's non-player text.
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://www.chaspark.com';
const DOMAIN = 'www.chaspark.com';

cli({
cli({
    site: 'huawei-chaspark',
    name: 'search',
    access: 'read',
    description: 'Search Huawei\'s 黄大年茶思屋 academic community (chaspark.com). Given an arbitrary question, returns the top N most relevant items (title, type, author, date, views, summary, item_id, detail_url). Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'query', positional: true, required: true, help: 'Your question or search term (e.g. "大模型", "光通信")' },
        { name: 'limit', type: 'int', default: 10, help: 'Max number of items to return (N)' },
    ],
    columns: ['rank', 'title', 'type', 'author', 'date', 'views', 'summary', 'item_id', 'detail_url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-chaspark search');

        const query = String(kwargs.query || '').trim();
        if (!query) throw new ArgumentError('huawei-chaspark search query cannot be empty');

        const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));

        // Navigate to the site so the session cookies are available to fetch.
        // The search is done via the JSON API directly (not card scraping):
        // the SPA's card rendering doesn't reliably fire under page.goto, but
        // the API (/chasiwu/v1/content/search) returns clean JSON with the
        // CSRF token from the X-CSRF-TOKEN cookie.
        await page.goto(`${BASE_URL}/#/home`).catch(() => {});
        await page.wait('time', 2).catch(() => {});

        const result = await page.evaluate(async (q: string, max: number) => {
            const stripEm = (s: string): string => s.replace(/<[^>]+>/g, '').trim();
            const csrf = (document.cookie.match(/X-CSRF-TOKEN=([^;]+)/) || [])[1] || '';
            const url = `https://www.chaspark.com/chasiwu/v1/content/search?sortBy=2&current=1&size=${max}&searchTxt=${encodeURIComponent(q)}&lang=zh`;
            const r = await fetch(url, { credentials: 'include', headers: { 'X-CSRF-TOKEN': csrf, 'Column-Type': 'searchDoc' } });
            if (r.status === 403) return { error: 'auth' };
            if (!r.ok) return { error: 'http ' + r.status };
            const j = await r.json();
            const recs = (j.data && j.data.records) || [];
            const fmtDate = (ts: string): string => {
                const n = Number(ts);
                if (!n) return '';
                const d = new Date(n * 1000);
                return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
            };
            const items = recs.map((rec: any) => ({
                title: stripEm(rec.title || ''),
                type: rec.columnType || '',
                author: rec.creatorName || '',
                author_id: rec.creatorNid || '',
                date: fmtDate(rec.publishTime),
                views: String(rec.views || ''),
                likes: String(rec.likes || ''),
                comments: String(rec.comments || ''),
                summary: stripEm(rec.subjectIntroduction || rec.thesisIntroduction || ''),
                item_id: rec.id || rec.contentId || '',
                detail_url: rec.route || '',
            })).filter((x: any) => x.title && x.item_id);
            return { items };
        }, query, limit).catch(() => ({ error: 'evaluate failed' })) as { error?: string; items?: any[] };

        if (result.error === 'auth') {
            throw new AuthRequiredError(DOMAIN, 'ChASpark requires a logged-in session. Open https://www.chaspark.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }
        if (result.error) {
            throw new CommandExecutionError(`huawei-chaspark search failed (${result.error})`);
        }
        const items = result.items || [];
        if (!items.length) {
            throw new EmptyResultError('huawei-chaspark', `No results for "${query}". Try a different keyword.`);
        }

        return items.slice(0, limit).map((item: any, index: number) => ({
            rank: index + 1,
            title: String(item.title || '').trim(),
            type: String(item.type || '').trim(),
            author: String(item.author || '').trim(),
            date: String(item.date || '').trim(),
            views: String(item.views || '').trim(),
            summary: String(item.summary || '').trim(),
            item_id: String(item.item_id || '').trim(),
            detail_url: String(item.detail_url || '').trim(),
        }));
    },
});
