Convert the following webpage into a Markdown file suitable for another AI agent to read and understand:

URL: <PASTE_URL_HERE>

Requirements:

1. Preserve the page text as verbatim as reasonably possible.
   - Keep headings, paragraphs, lists, captions, tables, code blocks, footnotes, citations, and links.
   - Do not summarize the article unless explicitly marking something as an added accessibility note.
   - Preserve the original order of the page.

2. Add metadata at the top as YAML front matter:
   - title
   - source_url
   - author, if available
   - published_date, if available
   - retrieved_date
   - license, if available

3. Preserve all images.
   - Include each image using Markdown syntax with the original remote image URL.
   - Keep nearby captions.
   - If the page uses relative image URLs, resolve them to absolute URLs.

4. Make the page understandable to a non-multimodal AI agent or LLM.
   For every meaningful image, add an “AI-readable visual equivalent” immediately after the image.
   Use one or more of the following:
   - Mermaid diagrams for workflows, architectures, loops, timelines, causal chains, plots, or comparisons.
   - SVG diagrams if layout or geometry matters.
   - Plain-text descriptions for photos, screenshots, charts, equations, or decorative images.
   - For complex equations from PDFs, include a rendered SVG crop for fidelity and a fenced text transcription labeled as lossy for text-only agents.

5. Clearly label added visual equivalents.
   Example:

   ```markdown
   ![Original figure](https://example.com/figure.png)

   Caption: Original caption from the page.

   AI-readable visual equivalent, added:
   ```mermaid
   flowchart TD
     A[Input] --> B[Model]
     B --> C[Output]
   ```
   ```

   Avoid generic placeholders. Each visual equivalent should use stable, structured fields such as Asset, Type, Extracted size, Caption/context, Nearby paper text, and Transcription status. Include an honest note about whether exact labels/data were extracted or only preserved visually.

6. Do not pretend the generated diagrams are part of the original page.
   Mark them as assistant-derived annotations.

6a. Do not silently flatten equations into prose when PDF extraction loses math structure.
    If LaTeX/source math is unavailable, preserve the visual equation as an SVG asset and label the adjacent extracted text as a potentially lossy transcription.

7. If a chart or figure contains data:
   - Extract visible labels, axes, legends, values, and trends where possible.
   - If exact values are not readable, say so.
   - Prefer a Mermaid chart, table, or structured text equivalent.

8. If an image is purely decorative:
   - Keep the image URL.
   - Add a short note such as: “Decorative image; no substantive content detected.”

9. Output the result as a `.md` file.
   Suggested filename:
   - derive from the title
   - lowercase
   - hyphen-separated
   - no special characters

10. After creating the file, verify:
   - The Markdown file exists.
   - The source URL is included.
   - All image URLs found in the page are included.
   - Added diagrams are syntactically fenced correctly.
   - The document is readable by a text-only AI agent or LLM, with added accessibility notes clearly separated from original paper text.

Important:
- Do not only summarize the webpage.
- Do not omit images.
- Do not replace images with diagrams; include both.
- Do not fabricate exact data from images if it is not visible.
- Keep added interpretation separate from original content.
