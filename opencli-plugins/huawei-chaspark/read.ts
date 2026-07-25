/**
 * Read the full content of a single chaspark item (paper / hotspots / video).
 *
 * Input: a full chaspark detail URL (the `detail_url` from a `search` result):
 *   - paper:    https://www.chaspark.com/#/research/paper/<id>
 *   - hotspots: https://www.chaspark.com/#/hotspots/<id>
 *   - video:    https://www.chaspark.com/#/stw/media/<id>
 *   - live:     https://www.chaspark.com/#/live/<id>
 *   - subject:  https://www.chaspark.com/#/s/<id>
 * Output: the item's full content (article body) plus title, author, date, views.
 *
 * Strategy: COOKIE — calls the chaspark detail-content JSON API directly
 * (bypassing the SPA's detail-page rendering, which doesn't reliably fire under
 * page.goto). The API returns clean JSON with the CSRF token from the cookie:
 *   paper/hotspots/subject: GET /chasiwu/v1/content/thesis/detail/<id>
 *   video/live:             GET /chasiwu/v1/video/detail/1/<id>
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://www.chaspark.com';
const DOMAIN = 'www.chaspark.com';

cli({
    site: 'huawei-chaspark',
    name: 'read',
    access: 'read',
    description: 'Read the full content of a single chaspark item by its detail URL (a paper #/research/paper/<id>, hotspots #/hotspots/<id>, or video #/stw/media/<id> URL — take it from a search result\'s detail_url). Returns the full article body plus title, author, date, views. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'detail_url', positional: true, required: true, help: 'The full chaspark.com detail URL from a search result\'s detail_url — e.g. https://www.chaspark.com/#/hotspots/1232136419919421440 or https://www.chaspark.com/#/research/paper/1298427126325977088.' },
    ],
    columns: ['title', 'author', 'author_id', 'date', 'views', 'likes', 'comments', 'body', 'url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-chaspark read');

        const raw = String(kwargs.detail_url || '').trim();
        if (!raw) throw new ArgumentError('huawei-chaspark read detail_url cannot be empty');

        const { itemId, detailUrl, type } = resolveDetailUrl(raw);

        // Fetch the detail-content JSON API directly (bypasses the broken
        // page.goto). The SPA's detail-page rendering doesn't reliably fire
        // under page.goto (the tab ends at about:blank), but the API returns
        // clean JSON with the CSRF token from the cookie.
        //   paper/hotspots/subject: GET /chasiwu/v1/content/thesis/detail/<id>
        //   video/live:             GET /chasiwu/v1/video/detail/1/<id>
        await page.goto(`${BASE_URL}/#/home`).catch(() => {});
        await page.wait('time', 2).catch(() => {});

        const apiPath = type === 'video'
            ? `/chasiwu/v1/video/detail/1/${itemId}`
            : `/chasiwu/v1/content/thesis/detail/${itemId}`;
        const result = await page.evaluate(async (path: string) => {
            const csrf = (document.cookie.match(/X-CSRF-TOKEN=([^;]+)/) || [])[1] || '';
            const r = await fetch(`https://www.chaspark.com${path}?seat=1&lang=zh`, { credentials: 'include', headers: { 'X-CSRF-TOKEN': csrf } });
            if (r.status === 403) return { error: 'auth' };
            if (!r.ok) return { error: 'http ' + r.status };
            const j = await r.json();
            const d = j.data || {};
            const stripHtml = (s: string): string => (s || '').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ').replace(/&[a-z]+;/g, '').trim();
            const fmtDate = (ts: string): string => {
                const n = Number(ts);
                if (!n) return '';
                const d = new Date(n * 1000);
                return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
            };
            const creator = d.creator || {};
            return {
                title: stripHtml(d.title || ''),
                author: creator.name || '',
                author_id: d.creatorNid || creator.nid || creator.w3id || '',
                date: fmtDate(d.publishTime),
                views: String(d.viewCount || d.views || ''),
                body: stripHtml(d.content || ''),
            };
        }, apiPath).catch(() => ({ error: 'evaluate failed' })) as { error?: string; title?: string; author?: string; author_id?: string; date?: string; views?: string; body?: string };

        if (result.error === 'auth') {
            throw new AuthRequiredError(DOMAIN, 'ChASPark requires a logged-in session. Open https://www.chaspark.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }
        if (result.error) {
            throw new CommandExecutionError(`huawei-chaspark read failed (${result.error})`);
        }
        if (!result.body) {
            throw new EmptyResultError('huawei-chaspark', `No content for item ${itemId}. It may be deleted, access-restricted, or the API changed.`);
        }

        return {
            title: String(result.title || '').trim(),
            author: String(result.author || '').trim(),
            author_id: String(result.author_id || '').trim(),
            date: String(result.date || '').trim(),
            views: String(result.views || '').trim(),
            likes: '',
            comments: '',
            body: String(result.body).trim(),
            url: detailUrl,
        };
    },
});

/**
 * Resolve the `detail_url` arg into { itemId, detailUrl, type }. Accepts a full
 * chaspark detail URL:
 *   - paper:    /#/research/paper/<id>
 *   - hotspots: /#/hotspots/<id>
 *   - video:    /#/stw/media/<id>
 *   - live:     /#/live/<id>
 *   - subject:  /#/s/<id>
 */
function resolveDetailUrl(raw: string): { itemId: string; detailUrl: string; type: string } {
    const paperM = raw.match(/\/research\/paper\/(\d+)/);
    if (paperM) return { itemId: paperM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'paper' };
    const hotspotsM = raw.match(/\/hotspots\/(\d+)/);
    if (hotspotsM) return { itemId: hotspotsM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'paper' };
    const videoM = raw.match(/\/stw\/media\/(\d+)/);
    if (videoM) return { itemId: videoM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'video' };
    const liveM = raw.match(/\/live\/(\d+)/);
    if (liveM) return { itemId: liveM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'video' };
    const subjectM = raw.match(/\/s\/(\d+)/);
    if (subjectM) return { itemId: subjectM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'paper' };
    throw new ArgumentError(
        `Could not read an item id from URL: ${raw}. ` +
        `Pass a chaspark detail_url from a search result (e.g. https://www.chaspark.com/#/hotspots/1232136419919421440).`,
    );
}
