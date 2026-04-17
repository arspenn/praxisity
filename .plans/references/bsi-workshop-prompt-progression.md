# BSI Workshop Prompt Progression

Each prompt below is a complete, paste-able example. They share the same goal so the audience can see how each addition changes the output.

---

## Step 0 — Baseline

This is how most people use AI — like a search engine with a longer input box.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Steps:
1. Search news outlets in the United States in the last 30 days
2. Search global news outlets discussing the United States in the last 30 days
Output: List them in a table format. Make the output a markdown artifact.
```

---

## Step 1 — Source Selection

Tell the AI *where* to look, not just *what* to find.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Sources: Search news outlets, government health agencies (CDC, WHO, NIH), and peer-reviewed journals for each topic.
Output: List them in a table format. Make the output a markdown artifact.
```

**What changed:** Added a `Sources` field directing the AI to authoritative public health sources instead of general news only.

**What to look for:** Do the topics change? Do the descriptions include more specific public health data?

---

## Step 2 — Verification

Make the output checkable — quotations and working links.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Sources: Search news outlets, government health agencies (CDC, WHO, NIH), and peer-reviewed journals. For each claim, use web search to find the original source. Include direct quotations where possible.
Links: Every URL must point to the specific page where the information was found, not a homepage. If you cannot confirm a link, mark it [link unconfirmed].
Output: For each topic, include quoted sources and URLs. List them in a table with detailed findings below. Make the output a markdown artifact.
```

**What changed:** Added direct quotation instruction, link specificity requirement, and the `[link unconfirmed]` marking pattern.

**What to look for:** Does the output now include actual quotes from sources? Can you click the links and find the quoted text?

---

## Step 3 — Transparency

The AI tells you what it *couldn't* do, so you know where to double-check.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Sources: Search news outlets, government health agencies (CDC, WHO, NIH), and peer-reviewed journals. For each claim, use web search to find the original source. Include direct quotations where possible.
Links: Every URL must point to the specific page where the information was found, not a homepage. If you cannot confirm a link, mark it [link unconfirmed].
Output: Create a markdown artifact with:
- Findings organized by topic, with quoted sources and URLs
- A source list at the end grouped by topic
- A problem log noting: unconfirmed links, contradictions between sources, gaps where sources could not be found, and any claims you summarized rather than quoted directly
```

**What changed:** Added the Problem Log — a section where the AI reports its own limitations honestly.

**What to look for:** Does the Problem Log appear? Does it contain real issues, or is it empty? Try clicking a link marked `[link unconfirmed]` — is it actually broken?

---

## Step 4 — Structural Control

Keep the AI on-task. Prevent it from adding sections you didn't ask for.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Sources: Search news outlets, government health agencies (CDC, WHO, NIH), and peer-reviewed journals. For each claim, use web search to find the original source. Include direct quotations where possible.
Links: Every URL must point to the specific page where the information was found, not a homepage. If you cannot confirm a link, mark it [link unconfirmed].
Output: Create a markdown artifact with:
- Findings organized by topic, with quoted sources and URLs
- A source list at the end grouped by topic
- A problem log noting: unconfirmed links, contradictions between sources, gaps where sources could not be found, and any claims you summarized rather than quoted directly

Do not add editorial analysis or commentary sections beyond what the goal asks for.
```

**What changed:** One line at the end — a structural constraint preventing the AI from adding unsolicited analysis sections.

**What to look for:** Compare to Step 3. Did the AI add any extra sections like "Analysis" or "Implications" in Step 3 that are now gone?

---

## Step 5 — Interactivity

Let the AI gather context from you before it starts working.

```
Role: Act as an industry analyst for public health.
Goal: Identify the top 5 public health topics currently trending in the United States. For each topic, provide a brief description, the primary audience affected, and why it is currently trending.
Sources: Search news outlets, government health agencies (CDC, WHO, NIH), and peer-reviewed journals. For each claim, use web search to find the original source. Include direct quotations where possible.
Links: Every URL must point to the specific page where the information was found, not a homepage. If you cannot confirm a link, mark it [link unconfirmed].
Output: Create a markdown artifact with:
- Findings organized by topic, with quoted sources and URLs
- A source list at the end grouped by topic
- A problem log noting: unconfirmed links, contradictions between sources, gaps where sources could not be found, and any claims you summarized rather than quoted directly

Do not add editorial analysis or commentary sections beyond what the goal asks for.

Ask me highly detailed questions before beginning research.
```

**What changed:** One line — "Ask me highly detailed questions before beginning research." Now the AI asks you questions to understand what you need before it starts.

**What to look for:** Does the AI ask relevant questions? Does the output change based on your answers? This is where the conversation becomes a collaboration rather than a one-shot query.

**Note:** This step uses more of your free-tier session budget because each question-and-answer is an additional exchange. If you run low on usage, the earlier steps work without any conversation.