/**
 * Search Huawei's 稼先社区 (jx.huawei.com) — the internal expert and engineer
 * knowledge community.
 *
 * Input: an arbitrary question/query. Output: the top N most relevant posts,
 * each with title, author, type, date, views, replies, a rich summary, and a
 * URL; plus a synthesized `answer` string assembled from the top results.
 *
 * Strategy: COOKIE — the site is a Vue SPA with no public search API (no JSON
 * XHR observed on search). Results are JS-rendered inline on the homepage, so
 * the adapter drives the logged-in Chrome tab, fills the search box the
 * Vue-reactive way (native value setter + dispatched input/change events),
 * clicks the search button, and scrapes the rendered result cards from the
 * page context.
 *
 * Recon-confirmed selectors (see README.md "Parts most likely to need
 * adjustment"):
 *   - search input:  input.form-control  (placeholder "搜内容 搜话题")
 *   - search button: .search-btn          (text "搜索"; appears after typing)
 *   - result card:   .recommended-page-list-item
 *   - type:          .contention-page-content-type-item
 *   - title:         .contention-page-content-title
 *   - rich summary:  .contention-page-content-summary  (the `title` attribute
 *                    holds the untruncated author + abstract + viewpoints text)
 *   - author:        .author-name   date: .create-time
 *   - stats:         .stat-item (1st = views, 2nd = replies)
 *
 * Detail-page navigation is Vue click-handler based and does not yield a
 * stable URL from the card, so `url` is the community homepage where the card
 * is surfaced; the rich summary carries the actual content.
 */

import { cli, Strategy } from "@jackwener/opencli/registry";
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from "@jackwener/opencli/errors";

const HOME_URL = "https://jx.huawei.com/";
const DOMAIN = "jx.huawei.com";

// CSS selector for a rendered result card. The class names are hashed
// (data-v-*) and may change between builds; adjust here if the markup shifts.
const CARD_SELECTOR = ".recommended-page-list-item";

// How long (seconds) to wait for results to render after clicking search.
const SUBMIT_WAIT_S = 4;

cli({
    site: "jiaxian",
    name: "search",
    access: "read",
    description: "Search Huawei's 稼先社区 (jx.huawei.com). Given an arbitrary question, returns the top N most relevant posts (title, author, type, date, views, replies, rich summary, url) plus a synthesized answer. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.",
    domain: DOMAIN,
    strategy: Strategy.COOKIE,
    browser: true,
    args: [
        { name: "query", positional: true, required: true, help: 'Your question or search term (e.g. "大模型推理优化", "5G架构演进")' },
        { name: "limit", type: "int", default: 10, help: "Max number of documents to return (N)" },
        { name: "language", default: "cn", help: "Source language: cn | en" },
    ],
    columns: ["rank", "title", "type", "author", "date", "views", "replies", "summary", "url"],
    func: async (page, kwargs) => {
        if (!page) throw new CommandExecutionError("Browser session required for jiaxian search");

        const query = String(kwargs.query || "").trim();
        if (!query) throw new ArgumentError("jiaxian search query cannot be empty");

        const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));
        // `language` is accepted for interface parity with sibling plugins but
        // not consumed: the 稼先社区 SPA search has no language toggle.

        // Land on the community so the page origin/cookies are right.
        await page.goto(HOME_URL);
        await page.wait("selector", 'input.form-control, input[placeholder*="搜"]').catch(() => {});

        // Auth gate: a logged-in page renders an avatar / user-info element.
        // A login-gated page shows a login/SSO prompt instead. If the SSO
        // session is missing or expired, every search will fail.
        const authOk = await page.evaluate(() => {
            const hasAvatar = !!(document.querySelector('[class*="avatar"]') || document.querySelector('[class*="user-info"]'));
            const hasLoginPrompt = /登录|sign\s*in/i.test(document.documentElement.outerHTML) && !hasAvatar;
            return hasAvatar || !hasLoginPrompt;
        });
        if (!authOk) {
            throw new AuthRequiredError(DOMAIN, "稼先社区 requires a logged-in session. Open https://jx.huawei.com/ in Chrome and sign in with your Huawei account, then re-run.");
        }

        // Trigger the search. Done entirely inside one page.evaluate to avoid
        // stale element refs between opencli find/click/type calls (Vue
        // re-renders between them). The native HTMLInputElement.value setter +
        // dispatched input/change events is what makes Vue's reactivity pick
        // the value up — page.type alone leaves it undefined.
        const triggered = await triggerSearch(page, query);
        if (!triggered) {
            throw new CommandExecutionError(
                "Could not trigger a search on jx.huawei.com. The search UI may have changed — run `opencli browser jxian state` after a manual search to inspect the new markup.",
            );
        }

        // Scrape the rendered result cards (all extraction happens in-page).
        const docs = await page.evaluate((selector, max) => {
            const text = (el) => (el?.textContent || "").trim();
            const nodes = Array.from(document.querySelectorAll(selector)).slice(0, max);
            return nodes.map((card) => {
                const typeEl = card.querySelector(".contention-page-content-type-item");
                const titleEl = card.querySelector(".contention-page-content-title");
                // The `title` attribute carries the full, untruncated summary
                // (author + abstract + viewpoints); the textContent is cut off
                // by an ellipsis class.
                const summaryEl = card.querySelector(".contention-page-content-summary");
                const authorEl = card.querySelector(".author-name");
                const dateEl = card.querySelector(".create-time");
                const stats = Array.from(card.querySelectorAll(".stat-item")).map((e) => text(e));
                return {
                    title: text(titleEl),
                    type: text(typeEl),
                    author: text(authorEl),
                    date: text(dateEl),
                    views: stats[0] || "",
                    replies: stats[1] || "",
                    summary: (summaryEl?.getAttribute("title") || text(summaryEl)).trim(),
                };
            }).filter((r) => r.title);
        }, CARD_SELECTOR, limit);

        if (!docs.length) {
            throw new EmptyResultError("jiaxian", `No results parsed for "${query}". Try a different keyword, or inspect the page with \`opencli browser jxian state\`.`);
        }

        // Synthesize an answer from the top results. The rich summaries carry
        // enough substance (author + abstract + viewpoints) to stand on their
        // own as an answer when the top hit is a good match.
        const answer = buildAnswer(query, docs);

        return docs.slice(0, limit).map((item, index) => ({
            rank: index + 1,
            title: String(item.title || "").trim(),
            type: String(item.type || "").trim(),
            author: String(item.author || "").trim(),
            date: String(item.date || "").trim(),
            views: String(item.views || "").trim(),
            replies: String(item.replies || "").trim(),
            summary: String(item.summary || "").trim(),
            url: HOME_URL,
            ...(index === 0 ? { answer } : {}),
        }));
    },
});

/**
 * Trigger the search entirely within the page context. Filling the input via
 * the native value setter + dispatched input/change events is what makes
 * Vue's v-model reactivity pick the value up; then we click .search-btn.
 *
 * Returns true if result cards render after the click, false otherwise.
 */
async function triggerSearch(page, query) {
    const ok = await page.evaluate((q) => {
        const input = document.querySelector("input.form-control")
            || document.querySelector('input[placeholder*="搜"]');
        if (!input) return false;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
        setter?.call(input, q);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        // The search button appears only after typing.
        return new Promise((resolve) => {
            setTimeout(() => {
                const btn = document.querySelector(".search-btn");
                if (!btn) { resolve(false); return; }
                btn.click();
                setTimeout(() => {
                    resolve(!!document.querySelector(".recommended-page-list-item"));
                }, 4000);
            }, 400);
        });
    }, query);
    return !!ok;
}

/**
 * Assemble a concise answer from the top results' rich summaries. Leads with
 * the best-matching summary (truncated for readability) and lists the sources
 * by rank so the caller can follow up.
 */
function buildAnswer(query, docs) {
    const top = docs.slice(0, 3).filter((d) => d.summary);
    if (!top.length) {
        return `No detailed summary available for "${query}". See the returned documents for details.`;
    }
    const parts = [`Answer for "${query}" (synthesized from 稼先社区 top results):\n`];
    top.forEach((d, i) => {
        const summary = String(d.summary).slice(0, 500);
        parts.push(`[${i + 1}] ${d.title} — ${d.type} by ${d.author} (${d.date})\n${summary}\n`);
    });
    if (docs.length > 3) {
        parts.push(`...and ${docs.length - 3} more source(s). See the full document list.`);
    }
    return parts.join("\n").trim();
}
