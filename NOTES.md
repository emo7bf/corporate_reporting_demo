📝 Demo Slide Outline (9 slides)
Slide 1 — Title

AI‑Drafted Global Impact Report – Responsible Sourcing Demo

🚀 Hackathon Winner, KLA 2025

Your name & ESG/AI Innovation tagline

Slide 2 — The Pain

Annual ESG / Global Impact Reports = time‑consuming, fragmented, reactive

Input from EHS, Governance, Supply Chain, Legal… + evolving ESG frameworks

Drafting = manual alignment → slow progress + inconsistencies

Slide 3 — Our Idea

AI‑powered first‑draft generator for the Global Impact Report

Sources leveraged:

📘 Last year’s report (baseline)

📝 Department & director updates

🌍 ESG rater/ranker frameworks (ISS, CDP, RBA)

🏭 Peer company publications (Lam, Applied, etc.)

Key Innovation: Automates text comparison, change tracking, and alignment across inputs

Slide 4 — The Impact

🚀 Speeds up annual reporting cycle

📊 Ensures alignment with top ESG raters/rankers

🌱 Positions KLA as a leader in transparent, forward‑looking reporting

Slide 5 — Golden Updates Example (Colloquial Inputs)

(Big emojis, casual quotes from directors)

🧑‍🏭 Daniel: “Add the compliance training webinar (REACH, RoHS, PFAS…) + new risk survey.”

🧑‍🔧 Nadine: “Turn LEGO bullet from a plan into something live — PFAS prep, EU iron/steel.”

🧑‍💼 Rajiv: “Swap out Theo’s quote for Sharon’s. Make it more engineering‑grounded.”

🧑‍🔬 Carla: “Include EMRT for cobalt & mica.”

🧑‍💻 Jeremy: “Update all SAQ/CDP stats: 94% direct, 85% indirect, 72% CDP.”

🧑‍🎓 Sofia: “Add Supplier Sustainability Award — three companies received it.”

(Note: each update also has a follow‑up question prompting ESG clarity, e.g. “Is the hotline disclosure public?”)

Slide 6 — How the App Works (Architecture)

Visual of 3 panes:

Left: Director types an update

Center: 2023 section (baseline)

Right: Rewritten section (2024 draft)
Below: Standards (ISS/RBA/CDP) + competitor excerpts auto‑pulled (RAG pipelines)

Callout box:

“Today’s demo is hard‑coded for transparency. In production, these boxes will run live LLM + RAG calls.”

Slide 7 — Demo Screenshot

Show Streamlit app with left input box, center 2023 text, right 2024 text

Highlight the Sharon quote swap + updated metrics

Small footer: “Hard‑coded demo; illustrates the pipeline”

Slide 8 — Peer Benchmarking

Lam Research: Supplier ESG awards + CDP disclosure stats

Applied Materials: PFAS disclosures + DEI goals + hotline

KLA aligns and leapfrogs with proactive EMRT + LEGO forum + supplier training

Slide 9 — Next Steps

Integrate live LLM + RAG pipelines behind the demo UI

Expand from Responsible Sourcing to all Global Impact Report sections

Onboard ESG department as co‑designers of the pipeline

🎙️ Speaker Script Highlights

Opening:
“Good morning — I’m Elizabeth, and our team built an AI‑powered drafting tool for KLA’s Global Impact Report. We just won the hackathon, but today I want to slow down and show you how it actually works.”

Pain Point:
“Every year, ESG staff spend months merging updates from EHS, governance, supply chain, and new standards. It’s slow, fragmented, and reactive.”

Our Idea:
“What if AI generated the first draft for you — combining last year’s report, new updates from directors, ESG frameworks like ISS & CDP, and even what Lam and Applied are publishing?”

Golden Updates Slide:
“These are real‑looking updates from our directors — written quickly, casually, and sometimes missing a keyword. The system’s job is to ‘fix’ and expand them into ISS‑aligned language.”

How It Works Slide:
“The app is simple: you type an update on the left, see the 2023 text in the middle, and get the rewritten 2024 text on the right. Below, the system shows linked standards and competitor excerpts.
Today’s version is hard‑coded because I can’t run GPT on site — but it demonstrates the exact workflow the live system will have.”

Peer Benchmarking:
“We also pull in competitor excerpts automatically — Lam’s supplier ESG awards, Applied’s PFAS disclosure practices — so our text isn’t just compliant, it’s competitive.”

Closing:
“Our next step is to integrate the live pipelines and expand beyond Responsible Sourcing. We’re excited to co‑design this with the ESG department so you can spend less time wrangling and more time leading.”
