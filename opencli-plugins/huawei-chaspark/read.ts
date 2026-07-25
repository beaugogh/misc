/**
 * Read the full content of a single chaspark item (paper or video).
 *
 * Input: a full chaspark detail URL (the `detail_url` from a `search` result):
 *   - paper:  https://www.chaspark.com/#/research/paper/<id>
 *   - video:  https://www.chaspark.com/#/stw/media/<id>
 *   - live:   https://www.chaspark.com/#/live/<id>
 * Output: the item's full content (article body for papers, AI summary +
 * transcript for videos) plus title, author, date, views.
 *
 * Strategy: COOKIE — the detail page is SSO-gated, so the adapter drives the
 * logged-in Chrome tab to the detail URL and scrapes the rendered content.
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - title:  h2  (paper) / document.title  (video)
 *   - paper body:  .style_m_text__hMFtq  (the article text; strip nav + meta)
 *   - video body:  the AI video summary ("AI视频摘要：...") + transcript segments
 *   - meta:   "MM-DD" date + "N次浏览" views inline in the page text
 */

import { cli, Strategy } from '@jackwener/opencli/registry';
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from '@jackwener/opencli/errors';

const BASE_URL = 'https://www.chaspark.com';
const DOMAIN = 'www.chaspark.com';

// How long (seconds) to wait for the body to render after navigation.
const RENDER_WAIT_S = 5;

cli({
    site: 'huawei-chaspark',
    name: 'read',
    access: 'read',
    description: 'Read the full content of a single chaspark item by its detail URL (a video #/stw/media/<id> or paper #/research/paper/<id> URL — take it from a search result\'s detail_url). Returns the full content (article body for papers, AI summary + transcript for videos) plus title, author, date, views. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'detail_url', positional: true, required: true, help: 'The full chaspark.com detail URL from a search result\'s detail_url — a video URL (https://www.chaspark.com/#/stw/media/1298064463498584064) or paper URL (https://www.chaspark.com/#/research/paper/1298427126325977088).' },
    ],
    columns: ['title', 'author', 'author_id', 'date', 'views', 'likes', 'comments', 'body', 'url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-chaspark read');

        const raw = String(kwargs.detail_url || '').trim();
        if (!raw) throw new ArgumentError('huawei-chaspark read detail_url cannot be empty');

        const { itemId, detailUrl, type } = resolveDetailUrl(raw);

        // Navigate to the detail page (SSO-gated; the bridge drives the
        // logged-in Chrome tab).
        await page.goto(detailUrl, { waitUntil: 'load', settleMs: 1500 });
        // Subject (#/s/<id>) pages are topic landings with little readable
        // text; paper/video pages have a real body. Wait for whichever.
        await page.wait('selector', '#content-main, h2, .style_m_text__hMFtq').catch(() => {});
        await page.wait('time', RENDER_WAIT_S).catch(() => {});

        // For subject pages, return title + metadata (no article body).
        if (type === 'subject') {
            const meta = await page.evaluate(() => {
                const pageText = document.body.innerText;
                const dateMatch = pageText.match(/(\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)/) || pageText.match(/(20\d{2}-\d{1,2}-\d{1,2})/);
                const viewsMatch = pageText.match(/(\d[\d,]*)\s*次浏览/);
                return {
                    title: (document.title || '').replace(/-黄大年茶思屋$/, '').trim(),
                    date: dateMatch ? dateMatch[1] : '',
                    views: viewsMatch ? viewsMatch[1] : '',
                    body: (document.querySelector('#content-main')?.textContent || '').trim(),
                };
            }).catch(() => ({} as any));
            return {
                title: String(meta.title || '').trim(),
                author: '', author_id: '', date: String(meta.date || '').trim(),
                views: String(meta.views || '').trim(), likes: '', comments: '',
                body: String(meta.body || '').trim(), url: detailUrl,
            };
        }

        // Auth gate.
        const authOk = await page.evaluate(() => {
            const deleted = /已被删除|无法查看/.test(document.body.innerText);
            const hasContent = !!document.querySelector('#content-main, h2, .style_m_text__hMFtq');
            const hasLoginPrompt = /请登录|sign\s*in|立即登录/i.test(document.body.innerText) && !hasContent;
            return deleted || hasContent || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, 'ChASpark requires a logged-in session. Open https://www.chaspark.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }

        // Scrape the rendered content. Branch on type (paper vs video/live).
        const doc = await page.evaluate((resourceType: string) => {
            const text = (el: Element | null | undefined): string => (el?.textContent || '').trim();

            // ---- Paper detail page (/#/research/paper/<id>). Article body in
            // .style_m_text__hMFtq. Meta (date/views/author) inline in the page. ----
            if (resourceType === 'paper') {
                const titleEl = document.querySelector('h2');
                const title = text(titleEl);
                const bodyEl = document.querySelector('.style_m_text__hMFtq');
                let body = text(bodyEl);
                const pageText = document.body.innerText;
                const dateMatch = pageText.match(/(\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)/) || pageText.match(/(20\d{2}-\d{1,2}-\d{1,2})/);
                const viewsMatch = pageText.match(/(\d[\d,]*)\s*次浏览/);
                // author: look for a user link near the title
                const authorLink = document.querySelector('a[href*="/user/"], [class*=author] a, [class*=userInfo] a');
                return {
                    title,
                    author: text(document.querySelector('[class*=author],[class*=userName],[class*=userInfo]')),
                    author_id: (authorLink?.getAttribute('href') || '').match(/\/user\/(\w+)/)?.[1] || '',
                    date: dateMatch ? dateMatch[1] : '',
                    views: viewsMatch ? viewsMatch[1] : '',
                    body,
                };
            }

            // ---- Video / live detail page (/#/stw/media/<id> or /#/live/<id>).
            // Title in h2; body = AI video summary + transcript segments. The
            // video player chrome (vjs-*) is stripped. ----
            const titleEl = document.querySelector('h2');
            const title = text(titleEl) || (document.title || '').replace(/-黄大年茶思屋$/, '').trim();
            const pageText = document.body.innerText;
            const dateMatch = pageText.match(/(\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)/) || pageText.match(/(20\d{2}-\d{1,2}-\d{1,2})/);
            const viewsMatch = pageText.match(/(\d[\d,]*)\s*次浏览/);
            // AI summary: text after "AI视频摘要：" up to the transcript
            const summaryMatch = pageText.match(/AI视频摘要[：:]([\s\S]*?)(?:字幕列表|相关推荐|$)/);
            // Transcript: collect trackItem timestamp + text pairs
            const transcript = Array.from(document.querySelectorAll('[class*=trackItem__]'))
                .map((t) => {
                    const time = text(t.querySelector('[class*=time]'));
                    const content = text(t.querySelector('[class*=content]'));
                    return `${time} ${content}`.trim();
                })
                .filter(Boolean);
            let body = '';
            if (summaryMatch) body += `AI视频摘要：${summaryMatch[1].trim()}\n\n`;
            if (transcript.length) body += `字幕 transcript:\n${transcript.join('\n')}`;
            if (!body) body = text(document.querySelector('#content-main')) || '';
            return {
                title,
                author: '',
                author_id: '',
                date: dateMatch ? dateMatch[1] : '',
                views: viewsMatch ? viewsMatch[1] : '',
                body,
            };
        }, type);

        // Deleted-content check.
        const deleted = await page.evaluate(() => /已被删除|无法查看/.test(document.body.innerText));
        if (deleted) {
            throw new EmptyResultError('huawei-chaspark', `Item ${itemId} has been deleted or is unavailable.`);
        }
        if (!doc.body) {
            throw new EmptyResultError('huawei-chaspark', `No content rendered for item ${itemId}. It may be access-restricted or the page markup may have changed — inspect with \`opencli browser huawei-chaspark state\`.`);
        }

        return {
            title: String(doc.title || '').trim(),
            author: String(doc.author || '').trim(),
            author_id: String(doc.author_id || '').trim(),
            date: String(doc.date || '').trim(),
            views: String(doc.views || '').trim(),
            likes: '',
            comments: '',
            body: String(doc.body || '').trim(),
            url: detailUrl,
        };
    },
});

/**
 * Resolve the `detail_url` arg into { itemId, detailUrl, type }. Accepts a full
 * chaspark detail URL:
 *   - paper:  https://www.chaspark.com/#/research/paper/<id>
 *   - video:  https://www.chaspark.com/#/stw/media/<id>
 *   - live:   https://www.chaspark.com/#/live/<id>
 */
function resolveDetailUrl(raw: string): { itemId: string; detailUrl: string; type: string } {
    const paperM = raw.match(/\/research\/paper\/(\d+)/);
    if (paperM) return { itemId: paperM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'paper' };
    const videoM = raw.match(/\/stw\/media\/(\d+)/);
    if (videoM) return { itemId: videoM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'video' };
    const liveM = raw.match(/\/live\/(\d+)/);
    if (liveM) return { itemId: liveM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'video' };
    const subjectM = raw.match(/\/s\/(\d+)/);
    if (subjectM) return { itemId: subjectM[1], detailUrl: raw.startsWith('http') ? raw : BASE_URL + raw, type: 'subject' };
    throw new ArgumentError(
        `Could not read an item id from URL: ${raw}. ` +
        `Pass a chaspark detail_url from a search result (e.g. https://www.chaspark.com/#/research/paper/1298427126325977088).`,
    );
}
