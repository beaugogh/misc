import { cli, Strategy } from "@jackwener/opencli/registry";
import { ArgumentError, AuthRequiredError, CommandExecutionError, EmptyResultError } from "@jackwener/opencli/errors";
const SEARCH_URL = "https://3ms.huawei.com/term-web/wiki/termSearch/searchWeb";
const HOME_URL = "https://3ms.huawei.com/terminology/#/main/home";
const DOMAIN = "3ms.huawei.com";
const CONFIDENCE_LABELS = {
  "4": "official",
  "3": "approved",
  "2": "reviewing",
  "1": "draft"
};
cli({
  site: "huawei-terminology",
  name: "search",
  access: "read",
  description: "Search the Huawei terminology database (3ms.huawei.com/terminology). Returns English term, Chinese term, domain, confidence, and definition. Requires a logged-in Huawei session via the OpenCLI Browser Bridge.",
  domain: DOMAIN,
  strategy: Strategy.COOKIE,
  browser: true,
  args: [
    { name: "query", positional: true, required: true, help: 'Term or abbreviation to search (e.g. "CloudDragon", "5G")' },
    { name: "limit", type: "int", default: 10, help: "Max results (server caps at ~50)" },
    { name: "language", default: "en", help: "Source language to search: en | cn" },
    { name: "filter-language", default: "", help: "Restrict to a result language, e.g. cn. Empty = all." }
  ],
  columns: ["rank", "term_en", "term_cn", "domain", "confidence", "definition", "url"],
  func: async (page, kwargs) => {
    if (!page) throw new CommandExecutionError("Browser session required for huawei-terminology search");
    const query = String(kwargs.query || "").trim();
    if (!query) throw new ArgumentError("huawei-terminology search query cannot be empty");
    const limit = Math.max(1, Math.min(Number(kwargs.limit) || 10, 50));
    const language = String(kwargs.language || "en");
    const filterLanguage = String(kwargs["filter-language"] || "");
    await page.goto(HOME_URL);
    const w3Account = await page.evaluate(`() => {
            try {
                const u = JSON.parse(localStorage.getItem('userInfo') || '{}');
                return u.w3Account || '';
            } catch { return ''; }
        }`);
    if (!w3Account) {
      throw new AuthRequiredError(DOMAIN, "Huawei terminology requires a logged-in session. Open https://3ms.huawei.com/terminology in Chrome and sign in, then re-run.");
    }
    const body = {
      page: 1,
      numpage: limit,
      language,
      query,
      filterLanguage,
      filterDomain: "",
      matchType: "match",
      resourceType: "",
      searchType: "RELATE",
      userinfo: { uid: "", userName: "", w3Account }
    };
    const json = await page.evaluate(`async () => {
            const r = await fetch(${JSON.stringify(SEARCH_URL)}, {
                method: 'POST',
                credentials: 'include',
                headers: { 'Content-Type': 'application/json' },
                body: ${JSON.stringify(JSON.stringify(body))}
            });
            if (!r.ok) return { __http: r.status };
            try { return await r.json(); } catch (e) { return { __parse: String(e && e.message || e) }; }
        }`);
    if (json?.__http) {
      if ([401, 403].includes(Number(json.__http))) {
        throw new AuthRequiredError(DOMAIN, `Huawei terminology search returned HTTP ${json.__http}; the session may have expired. Re-open https://3ms.huawei.com/terminology and sign in.`);
      }
      throw new CommandExecutionError(`Huawei terminology search returned HTTP ${json.__http}`);
    }
    if (json?.__parse) {
      throw new CommandExecutionError(`Huawei terminology search returned non-JSON body: ${json.__parse}`);
    }
    if (String(json?.code) !== "0") {
      throw new CommandExecutionError(`Huawei terminology search failed (code ${json?.code}): ${json?.info || "unknown error"}`);
    }
    const list = Array.isArray(json?.list) ? json.list : [];
    if (!list.length) {
      throw new EmptyResultError("huawei-terminology", `No terms found for "${query}". Try a different keyword.`);
    }
    return list.map((item, index) => ({
      rank: index + 1,
      term_en: String(item?.ftitleEn || item?.title || "").trim(),
      term_cn: String(item?.ftitleCn || "").trim(),
      domain: String(item?.nodeNameZh || item?.nodeName || "").trim(),
      confidence: CONFIDENCE_LABELS[String(item?.confidenceLevel || "")] || String(item?.confidenceLevel || ""),
      definition: String(item?.definitionContent || "").trim(),
      url: item?.fid ? `https://3ms.huawei.com/terminology/#/main/termDetail?id=${item.fid}` : ""
    }));
  }
});
