# Claude's free tier in April 2026: capabilities, limits, and public health research utility

**Claude Sonnet 4.6 is the most powerful model available for free on claude.ai**, offering a surprisingly robust feature set that includes web search, code execution, file uploads, vision, and PDF analysis — all at zero cost. Free users are locked to this single model and cannot access Claude Opus 4.6 (Anthropic's most intelligent model overall) or switch between models. While the free tier imposes meaningful usage caps — a session-based limit that resets every five hours — its analytical capabilities are substantial enough for public health data work, including CSV processing, statistical analysis via Python, and literature-grade PDF review.

This report draws exclusively from official Anthropic documentation across `support.anthropic.com` (the claude.ai help center, also accessible via `support.claude.com`), `docs.anthropic.com` / `platform.claude.com` (API and technical documentation), and `anthropic.com` (product pages and announcements). All URLs cited below are direct links to these official sources.

---

## The free tier runs Sonnet 4.6, Anthropic's second-most-powerful model

The most powerful Claude model available on the free tier is **Claude Sonnet 4.6**, released on February 17, 2026. Anthropic's official Sonnet product page at `anthropic.com/claude/sonnet` states: "Anyone can chat with Claude using Sonnet 4.6 on Claude.ai, available on web, iOS, and Android." Free users cannot change their model — the model selector is exclusive to paid plans. This is confirmed by the support article at `support.anthropic.com/en/articles/8114491-how-do-i-get-started-with-claude-ai`, which states: "The model you're currently chatting with is displayed below your text input. Free users can't adjust this."

Sonnet 4.6 is described officially as offering "the best combination of speed and intelligence" and is positioned as Anthropic's frontier-intelligence model built for coding, agents, and enterprise workflows. It sits one tier below **Claude Opus 4.6** (released February 5, 2026), which Anthropic calls "the most intelligent broadly available model" but restricts to Pro ($20/month), Max ($100–$200/month), Team, and Enterprise plans. The pricing page at `anthropic.com/pricing` confirms that the Pro plan adds "Ability to use more Claude models" over the Free plan, further verifying that free users receive a single default model.

Key Sonnet 4.6 specifications from the official models documentation at `docs.anthropic.com/en/docs/about-claude/models/all-models`:

- **API model ID**: `claude-sonnet-4-6`
- **Training data cutoff**: January 2026
- **Reliable knowledge cutoff**: August 2025
- **Supports**: text and image input, text output, multilingual capabilities, vision, extended thinking, and adaptive thinking

---

## Full capability breakdown on the free tier

The free tier of claude.ai provides access to a broad set of features, many of which were historically paid-only. Here is every verified capability with its official source:

**Web search** is available on the free tier. The support article at `support.anthropic.com/en/articles/10684626-enabling-and-using-web-search` confirms: "As a free user, you have daily usage limits for Claude. Since web search and fetch both contribute to these limits, here are some tips to make the most of your capacity." Users enable it via the slider icon in the chat input. Web search and web fetch both count against the session usage limit.

**File uploads** are supported for all users. According to the support documentation at `support.anthropic.com/en/articles/8241126-uploading-files-to-claude`, users can upload files up to **30MB per file** and up to **20 files per chat**. Supported formats include images, PDFs, CSVs, spreadsheets, and other common file types. Image uploads support JPEG, PNG, GIF, and WebP formats with a maximum resolution of **8,000 × 8,000 pixels**.

**Code execution and file creation** is available to all claude.ai users, including free accounts. Per `support.anthropic.com/en/articles/12111783-create-and-edit-files-with-claude`, Claude can write and execute Python code in a secure server-side sandboxed environment. This environment comes pre-installed with **pandas, numpy, matplotlib**, and other common Python libraries — enabling statistical computation, data transformation, and chart generation. Claude can also create downloadable output files including Excel (.xlsx), Word (.docx), PowerPoint (.pptx), and PDF formats.

**Artifacts** — Claude's interactive content panel for code, visualizations, documents, and applications — is available on all plans. The support article at `support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them` states: "Accessing artifacts in the sidebar and Claude-powered artifacts are supported on free, Pro, Max, and Claude for Work (Team and Enterprise) plans." Free users can also publish and remix artifacts per `support.anthropic.com/en/articles/9547008-publishing-remixing-and-sharing-artifacts`.

**Vision and image understanding** is supported across all current Claude models, including the Sonnet 4.6 used on the free tier. Per the vision documentation at `docs.anthropic.com/en/docs/build-with-claude/vision`, Claude can analyze photographs, charts, diagrams, screenshots, and other images. On claude.ai, users can upload up to **20 images per chat**. Limitations include inability to identify people by name, reduced accuracy with low-quality or rotated images, approximate object counting, and limited spatial reasoning.

**PDF and document analysis** leverages Claude's vision capabilities. Per `docs.anthropic.com/en/docs/build-with-claude/pdf-support`, Claude processes PDFs by converting each page to an image while also extracting text, enabling analysis of text, charts, tables, and figures. Each page typically consumes **1,500–3,000 tokens**. On the free tier's 200K context window, this allows analysis of roughly 60–130 pages in a single conversation.

**Context window size** on the free tier is **200K tokens** (approximately 500+ pages of text). The support article at `support.anthropic.com/en/articles/11647753-understanding-usage-and-length-limits` states: "Currently, Claude's context window size is 200K tokens across all models and paid plans." Note that while Sonnet 4.6 supports a **1M-token context window** via the API, this extended window on claude.ai is only available to Enterprise plans (at 500K tokens). Free tier users are limited to 200K tokens.

**Extended thinking** — Claude's ability to reason step-by-step before responding — is available on the free tier with limited usage, documented at `support.anthropic.com/en/articles/10574485-using-extended-thinking-on-claude-3-7-sonnet`.

**Memory across conversations** is available for all users, including free accounts. Per the release notes at `docs.anthropic.com/en/release-notes/claude-apps`: "Memory from chat history is now available for all Claude users, including free users" (as of March 2, 2026).

**Voice mode** is available on all plans in beta for mobile apps, with free users able to send approximately **20–30 voice messages** before hitting session limits, per `support.anthropic.com/en/articles/11101966-using-voice-mode-on-claude-mobile-apps`.

Additional free-tier features include **desktop extensions**, **Slack and Google Workspace connectors**, **remote MCP (Model Context Protocol) connectors**, and up to **5 projects** for organizing conversations with custom instructions.

---

## How the free tier compares to paid plans

The most significant constraints on the free tier are **usage volume** and **model access**. The table below summarizes the key differences based on `anthropic.com/pricing` and `support.anthropic.com/en/articles/11049762-choosing-a-claude-ai-plan`:

| Feature | Free ($0) | Pro ($20/mo) | Max 5x ($100/mo) | Max 20x ($200/mo) |
|---|---|---|---|---|
| **Model** | Sonnet 4.6 only | Sonnet 4.6, Opus 4.6, Haiku 4.5 | All models | All models |
| **Session usage** | Baseline | ≥5× free | 25× free | 100× free |
| **Session reset** | Every 5 hours | Every 5 hours | Every 5 hours | Every 5 hours |
| **Weekly limit** | N/A (session only) | Yes, across all models | Yes (dual limits) | Yes (dual limits) |
| **Context window** | 200K tokens | 200K tokens | 200K tokens | 200K tokens |
| **Projects** | 5 maximum | Unlimited | Unlimited | Unlimited |
| **Claude Code** | ✗ | ✓ | ✓ | ✓ |
| **Research mode** | ✗ | ✓ | ✓ | ✓ |
| **Claude Cowork** | ✗ | ✓ | ✓ | ✓ |
| **Claude for Excel** | ✗ | ✓ (beta) | ✓ (beta) | ✓ (beta) |
| **Claude in Chrome** | ✗ | ✗ | ✓ | ✓ |
| **Extra usage (pay-as-you-go)** | ✗ | ✓ | ✓ | ✓ |
| **Priority during high traffic** | ✗ | ✓ | ✓ | ✓ |
| **Training data opt-out** | Available | Available | Available | Default off |

The usage limit is the most impactful constraint for heavy users. Per `support.anthropic.com/en/articles/8114491-how-do-i-get-started-with-claude-ai`: "While using the free Claude plan, there is a session-based usage limit that will reset every five hours. The number of messages you can send will vary based on demand." Anthropic does not publish exact message counts — limits are dynamic and depend on message length, file attachments, conversation complexity, and current server demand. When you hit the limit, Claude notifies you, and you must wait for the 5-hour reset. Paid plans can enable "extra usage" at API rates to continue working past limits, per `support.anthropic.com/en/articles/12429409-extra-usage-for-paid-claude-plans`.

Two other noteworthy differences: **Research mode** (a multi-step, multi-source structured investigation feature at `support.anthropic.com/en/articles/11088861-using-research-on-claude-ai`) is exclusive to Pro and above. And free-tier conversations **may be used for model training**, though users can opt out; paid Team and Enterprise plans disable training by default.

---

## What free-tier Claude can do for public health data research

For a public health internship, the free tier's analytical toolkit is more capable than it might appear. Here are the specific capabilities most relevant to epidemiological and public health work:

**CSV and spreadsheet analysis** is directly supported through the code execution environment. You can upload CSV files (up to 30MB) and Claude will use pandas to clean, transform, filter, aggregate, and analyze tabular data. This covers common public health tasks like calculating incidence rates, generating frequency distributions, cross-tabulating demographic variables, and running descriptive statistics. Claude can produce summary tables, pivot tables, and export results as Excel files for further use in tools like SAS or Stata.

**Data visualization** uses matplotlib (and potentially other installed libraries) to generate publication-quality charts directly within the conversation. This includes bar charts, line graphs, scatter plots, histograms, heatmaps, and other visualization types commonly used in epidemiological reporting. Generated charts can be downloaded as image files.

**PDF analysis for literature review** allows you to upload research papers, CDC reports, WHO briefs, or other public health documents (up to 30MB each, 20 per chat) and have Claude extract key findings, summarize methodologies, compare results across studies, and identify relevant data points. The 200K-token context window supports analysis of substantial documents — roughly equivalent to a 100-page report with mixed text and figures.

**Citation and reference support** is built into Claude's capabilities. The API-level documentation at `docs.anthropic.com/en/docs/build-with-claude/pdf-support` confirms citations are supported for PDFs, plain text, and custom content documents. While the free tier does not include Research mode (which automates multi-source literature searches), you can manually upload papers and ask Claude to generate properly formatted citations in APA, AMA, Vancouver, or other styles commonly used in public health publications.

**Web search for current data** enables Claude to retrieve up-to-date epidemiological statistics, recent publications, and current public health guidelines — critical since the model's training data has a cutoff (January 2026 for Sonnet 4.6). This is especially useful for accessing recent CDC MMWR reports, WHO situation updates, or state health department dashboards during your research.

**Practical limitations for research work** should be noted. The 5-hour session reset means you cannot run continuous, extended analyses — plan work in focused sessions. The 200K context window limits how many documents you can analyze simultaneously (roughly 3–5 full journal articles at once). You cannot access Opus 4.6, which has superior reasoning for complex analytical tasks. And Research mode's automated multi-source investigation is unavailable on the free tier, meaning literature reviews require more manual effort. For an internship with sustained daily usage, the **Pro plan at $20/month** would be worth considering, as it provides at least 5× the usage capacity and access to Research mode and Claude Opus 4.6.

---

## Conclusion

Claude Sonnet 4.6 on the free tier delivers genuine analytical capability for public health data work — including Python-powered statistical analysis, PDF document review, data visualization, and web search — at no cost. The primary trade-offs are usage volume (session limits resetting every 5 hours with unpublished message caps), lack of access to Opus 4.6 and Research mode, and the 200K-token context window that constrains multi-document analysis. For an academic deliverable, the key official documentation sources to reference are:

- **Plan comparison and features**: `anthropic.com/pricing`
- **Free tier overview**: `support.anthropic.com/en/articles/8114491-how-do-i-get-started-with-claude-ai`
- **Usage limits**: `support.anthropic.com/en/articles/11647753-understanding-usage-and-length-limits`
- **File creation and code execution**: `support.anthropic.com/en/articles/12111783-create-and-edit-files-with-claude`
- **Model specifications**: `docs.anthropic.com/en/docs/about-claude/models/all-models`
- **Context window details**: `support.anthropic.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-ai-plans`
- **Web search**: `support.anthropic.com/en/articles/10684626-enabling-and-using-web-search`
- **Vision capabilities**: `docs.anthropic.com/en/docs/build-with-claude/vision`
- **PDF support**: `docs.anthropic.com/en/docs/build-with-claude/pdf-support`

All information in this report was verified against these official Anthropic sources as of April 2026. Given that Anthropic iterates rapidly on features and pricing, confirm current details at the URLs above before finalizing any professional deliverable.