/**
 * Read the full content of a single 稼先社区 (jx.huawei.com) post.
 *
 * Input: a post id (the 32-char hex `postId` from a detail URL) — either bare
 * (`da25639435334344912733f65c592a1b`) or as the full detail URL
 * (`https://jx.huawei.com/community/comgroup/postsDetails?postId=...&type=freePost`).
 * Output: the complete article — title, author, date, views/likes/replies, and
 * the full body text (rendered from the detail page's `.detail-content`).
 *
 * This complements `search`, which returns rich summaries + metadata for many
 * posts but not the full body. `read` fetches one post's full content.
 *
 * Why navigation + scrape instead of a content API: the 稼先社区 detail body is
 * rendered server-side into the page HTML (`.detail-content`), and no clean
 * JSON content API was found in the app bundle. Navigating to the detail URL
 * (`/community/comgroup/postsDetails?postId=<id>&type=free_post`, discovered
 * from the bundle's resourceType → URL mapping) and reading the rendered body
 * is the reliable path. The `type` maps to a route:
 *   free_post        → /community/comgroup/postsDetails?postId=<id>
 *   technical_report → /TI/report/details/<id>
 *   industry_report  → /TI/industry/details/<id>
 * Only `free_post` is wired here; the report routes have different markup.
 *
 * Strategy: COOKIE — the detail page is SSO-gated, so the adapter drives the
 * logged-in Chrome tab to the detail URL and scrapes the rendered content.
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - body:     .detail-content  (or <article>; full post text. Cloned with
 *               .video-js / <video> players stripped — their DOM text
 *               "Video Player is loading…Play Video…Chapters…" would
 *               otherwise pollute the body)
 *   - title:    .contention-page-content-title  (or h1)
 *   - author:   .author-card__info-row  (name + id + dept, one string)
 *   - views:    .author-card__stat-label "访问量" → sibling stat-value
 *   - likes:    .nav-name "点赞 <n>"
 *   - date:     container of .meta-icon-date  (matches 20YY-MM-DD)
 *
 * NOTE: hand-mirrored from read.ts (no build step). Keep the two in sync.
 */

import { cli, Strategy } from "@jackwener/opencli/registry";
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from "@jackwener/opencli/errors";

const DOMAIN = 'jx.huawei.com';
const BASE_URL = 'https://jx.huawei.com';

// Detail route per resource type. Only free_post (自由讨论) is supported; the
// report types have different page markup and would need their own extractors.
const DETAIL_ROUTE = {
    free_post: (id) => `/community/comgroup/postsDetails?postId=${id}&noTop=true&type=freePost`,
};

// How long (seconds) to wait for the detail body to render after navigation.
const RENDER_WAIT_S = 5;

cli({
    site: 'huawei-jiaxian',
    name: 'read',
    access: 'read',
    description: 'Read the full content of a single 稼先社区 post by its postId (bare 32-char hex id, or the full detail URL). Returns the complete article body plus title, author, date, views, likes, replies. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.',
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: 'post_id', positional: true, required: true, help: 'The post id — either a bare 32-char hex postId (e.g. da25639435334344912733f65c592a1b) or a full detail URL from jx.huawei.com' },
        { name: 'type', default: 'free_post', help: 'Resource type: free_post | technical_report | industry_report (only free_post is supported)' },
    ],
    columns: ['title', 'author', 'author_id', 'dept', 'date', 'views', 'likes', 'replies', 'body', 'url'],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError('Browser session required for huawei-jiaxian read');

        const raw = String(kwargs.post_id || '').trim();
        if (!raw) throw new ArgumentError('huawei-jiaxian read post_id cannot be empty');

        const type = String(kwargs.type || 'free_post').trim();
        const routeFn = DETAIL_ROUTE[type];
        if (!routeFn) {
            throw new ArgumentError(`huawei-jiaxian read does not support type "${type}". Supported: ${Object.keys(DETAIL_ROUTE).join(', ')}.`);
        }

        // Accept either a bare postId or a full detail URL; extract the postId.
        const { postId, type: parsedType } = parsePostId(raw, type);
        const path = DETAIL_ROUTE[parsedType || type](postId);
        const detailUrl = BASE_URL + path;

        // Navigate to the detail page (SSO-gated; the bridge drives the
        // logged-in Chrome tab).
        await page.goto(detailUrl);
        await page.wait('time', RENDER_WAIT_S).catch(() => {});

        // Auth gate: a logged-in page renders the body; a gated page shows a
        // login/SSO prompt instead.
        const { authOk, bodyLen } = await page.evaluate(() => {
            const body = document.querySelector('.detail-content') || document.querySelector('article');
            const hasLoginPrompt = /登录|sign\s*in/i.test(document.documentElement.outerHTML) && !body;
            return { authOk: !!body || !hasLoginPrompt, bodyLen: body ? (body.textContent || '').trim().length : 0 };
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, '稼先社区 requires a logged-in session. Open https://jx.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.');
        }

        // Scrape the rendered detail content (all extraction in-page).
        const doc = await page.evaluate(() => {
            const text = (el) => (el?.textContent || '').trim();
            const bodyEl = document.querySelector('.detail-content') || document.querySelector('article');
            const titleEl = document.querySelector('.contention-page-content-title') || document.querySelector('h1');

            // The detail body may embed a video.js player whose DOM text
            // ("Video Player is loading…Play Video…Chapters…Font Size…")
            // would pollute the body. Clone the body, strip video players,
            // then read textContent + collapse excess blank lines.
            const bodyText = (() => {
                if (!bodyEl) return '';
                const clone = bodyEl.cloneNode(true);
                clone.querySelectorAll('.video-js, video').forEach((e) => e.remove());
                return (clone.textContent || '').replace(/\n{3,}/g, '\n\n').trim();
            })();

            // Author: .author-card__info-row holds "name + id + dept" as one
            // string (e.g. "李景宇l00974523高教军团..."). Split into name, id,
            // dept. The id is an [lsd]\d+ token; the rest before it is the
            // name, after it the department.
            const authorRow = document.querySelector('.author-card__info-row');
            const authorText = text(authorRow);
            const authorMatch = authorText.match(/^(.*?)([lsd]\d{4,})(.*)$/);
            const authorName = authorMatch ? authorMatch[1].trim() : authorText;
            const authorId = authorMatch ? authorMatch[2] : '';
            const dept = authorMatch ? authorMatch[3].trim() : '';

            // Stats: "访问量" label → its stat-value sibling; "点赞 <n>" nav.
            const labels = Array.from(document.querySelectorAll('.author-card__stat-label, .nav-name'));
            const statFor = (needle) => {
                const lbl = labels.find((e) => (e.textContent || '').includes(needle));
                if (!lbl) return '';
                const val = lbl.parentElement?.querySelector('.author-card__stat-value')?.textContent?.trim();
                if (val) return val;
                return lbl.nextElementSibling?.textContent?.trim() || '';
            };
            const views = statFor('访问量') || statFor('浏览');
            const likesEl = labels.find((e) => /点赞/.test(e.textContent || ''));
            const likes = likesEl ? (likesEl.textContent || '').replace(/点赞\s*/, '').trim() : '';

            // Date: the .meta-icon-date container holds a 20YY-MM-DD string.
            const dateIcon = document.querySelector('.meta-icon-date');
            const dateText = dateIcon?.parentElement?.textContent || dateIcon?.closest('[class*=meta]')?.textContent || '';
            const dateMatch = dateText.match(/20\d{2}[-/.]\d{1,2}[-/.]\d{1,2}/);

            // Replies: count next to the 评论 label, if present.
            const replies = statFor('评论');

            return {
                title: text(titleEl) || document.title,
                author: authorName,
                author_id: authorId,
                dept,
                date: dateMatch ? dateMatch[0] : dateText.trim().slice(0, 20),
                views,
                likes,
                replies,
                body: bodyText,
            };
        });

        if (!doc.body) {
            throw new EmptyResultError('huawei-jiaxian', `No body rendered for postId ${postId}. The post may not be a free_post, may be deleted, or the page markup may have changed — inspect with \`opencli browser huawei-jiaxian state\`.`);
        }

        return {
            title: String(doc.title || '').trim(),
            author: String(doc.author || '').trim(),
            author_id: String(doc.author_id || '').trim(),
            dept: String(doc.dept || '').trim(),
            date: String(doc.date || '').trim(),
            views: String(doc.views || '').trim(),
            likes: String(doc.likes || '').trim(),
            replies: String(doc.replies || '').trim(),
            body: String(doc.body || '').trim(),
            url: detailUrl,
        };
    },
});

/**
 * Parse the `post_id` arg into a bare 32-char hex postId (+ optional type
 * override from the URL). Accepts:
 *   - a bare hex id:  da25639435334344912733f65c592a1b
 *   - a detail URL:   https://jx.huawei.com/community/comgroup/postsDetails?postId=...&type=freePost
 * The URL's `type` query param (freePost → free_post) overrides the `type`
 * arg when present, since the URL knows its own resource type.
 */
function parsePostId(raw, fallbackType) {
    // Full URL: extract postId + type from the query string.
    if (raw.includes('://') || raw.startsWith('/community/')) {
        try {
            const url = raw.startsWith('http') ? new URL(raw) : new URL(raw, BASE_URL);
            const postId = url.searchParams.get('postId') || '';
            const typeParam = url.searchParams.get('type') || '';
            // URL uses camelCase (freePost); normalize to snake (free_post).
            const type = typeParam ? typeParam.replace(/([a-z])([A-Z])/g, '$1_$2').toLowerCase() : fallbackType;
            if (!/^[0-9a-f]{32}$/i.test(postId)) {
                throw new ArgumentError(`Could not read a postId from URL: ${raw}`);
            }
            return { postId, type };
        } catch (e) {
            if (e instanceof ArgumentError) throw e;
            throw new ArgumentError(`Could not parse detail URL: ${raw}`);
        }
    }
    // Bare id.
    if (!/^[0-9a-f]{32}$/i.test(raw)) {
        throw new ArgumentError(`post_id must be a 32-char hex id or a jx.huawei.com detail URL, got: ${raw}`);
    }
    return { postId: raw, type: fallbackType };
}
