Concept Overview – AI-Drafted Global Impact Report

Health, Safety and Well-being

KLA’s outstanding performance in environmental and occupational health and safety is rooted in our values, with high-performing teams working together to solve challenges and drive ongoing improvement. Our priority is the safety and well-being of our employees, whether in our business offices and manufacturing facilities or at customer sites where our field services teams install, maintain and update KLA products. We deliver specialized training based on each employee’s job-specific risks and adhere to global health and safety best practices. This proactive, risk-based approach allows us to maintain high safety and health standards, stay ahead of regulatory changes, and enhance coordination and consistency across our operations.

Our environmental, health and safety team (EHS) is led by a dedicated global EHS director, who reports to our vice president for Global Workplace Services and Operations, Real Estate, EHS and Security. In 2023, we updated and made public our Environmental, Health & Safety Commitment Policy.

In 2023, we continued to make progress expanding our ISO 14001 and ISO 45001 programs across our main production and R&D facilities. As of year-end 2023, our sites in Singapore; Newport, Wales; Milpitas, California; and Migdal Ha’emek, Israel, are certified to ISO 14001, the internationally recognized standard for environmental management systems (EMS). Our Wales site is also certified to ISO 45001, which specifies requirements for occupational health and safety (OH&S) management systems.

Throughout the year, we continued to enhance our health and safety policies and practices globally, implementing multiple new systems to standardize best practices and establish a single source of truth in areas such as environmental data collection, operational controls, audit tracking, incident management, compliance monitoring and corrective actions. To better and more efficiently manage our chemical products, we’re expanding the use of software to create safety data sheets, which define the properties, hazards and required safety procedures for chemical products that are formulated and used with our tools. Our compliance software also monitors regulations and alerts us to changes, allowing us to update our compliance posture as necessary, and on a timely basis.

Problem:

Annual sustainability / impact reports are time-consuming, fragmented, and reactive.

Input comes from multiple departments (EHS, governance, supply chain, etc.) plus evolving ESG frameworks and peer benchmarks.

Drafting requires manual alignment across all sources → slows progress and risks inconsistencies.

Our Solution:

Build an AI-powered drafting system that generates the first draft of the Global Impact Report.

Sources leveraged:

📘 Last year’s final report (baseline)
📝 Department & director updates (EHS, governance, diversity, etc.)
🌍 ESG rater/ranker frameworks & metrics (ISS, CDP, RBA, etc.)
🏭 Peer company publications (benchmarking + best practices)

Key Innovation:
AI automates text comparison, change tracking, and alignment across inputs.
Produces a cohesive, standards-ready draft that integrates corporate voice, peer positioning, and rating agency criteria.
Cuts drafting time, increases consistency, and improves ESG score alignment.

Impact:
🚀 Speeds up the annual reporting cycle.
📊 Ensures alignment with top ESG raters/rankers.
🌱 Positions company as a leader in transparent, forward-looking reporting.


# Responsible Sourcing Demo – Update Reviewer (Streamlit)  
_A quick README for hackathon UI demo repo_

This app is a **review tool for ESG copy updates**. It lets a human (or an LLM “teammate”) line up the **original 2023** text against the **updated 2024** text and review each requested change with standards context, tiny diffs, and export.

It’s intentionally simple: all “data” is defined at the top of the file, and the Streamlit UI below renders it.

---

## TL;DR Quickstart

1. Install dependencies:
   ```bash
   pip install streamlit
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

3. Use the sidebar to pick an update → highlights show in both panes.

---

## What’s in this app?

### 1) Inputs (data you can edit)

**A. Source documents**
- `original_text_2023`: the baseline 2023 “Responsible Sourcing” section.
- `outputted_text_2024`: the new draft for 2024.

**B. Human requests (`user_input_updates`)**  
A list of dictionaries, each representing a requested change in natural language.

Fields include:
- `id` (e.g., "u1")  
- `change_type` ("addition", "modification", or "removal")  
- `request` (plain English ask)  
- `section_hint` (where it belongs)

**C. Standards index (`standards_index`)**  
A small dictionary acting as a knowledge base. Keys are standard IDs (e.g. "RBA:L.2.3") mapping to `source`, `title`, and `clause` fields.

**D. Transformed updates (`transformed_updates`)**  
The authoritative list the UI uses. Each entry ties together:
- `raw_request`
- `rephrased_update`
- `standard_refs` (links into `standards_index`)
- `original_text_to_highlight` and/or `new_text_to_highlight`

---

### 2) UI features

- **Sidebar**: filter updates, search by text or standard, click a chip to select, view standards.  
- **Main panels**: left shows original text with highlight; right shows updated text with highlight.  
- **Standards drawer**: expander showing linked standards and clauses.  
- **Mini diff**: optional word-level diff.  
- **Export**: download selected update + both documents as JSON.  
- **Prev/Next buttons**: step through updates quickly.

---

## Data contracts for teammates or LLMs

1. `original_text_2023` and `outputted_text_2024` must be plain text.  
2. `transformed_updates` is the driver of the UI. Each update should reference standards correctly and have exact snippets for highlighting.  
3. Standards referenced in `standard_refs` must exist in `standards_index`.  
4. Highlight matching in the OG app is exact substring search—make snippets verbatim.

---

## Common tasks

- **Add a new change request**: append to `user_input_updates` and `transformed_updates`.  
- **Add/update a standard**: add entry to `standards_index`, then reference it.  
- **Update metrics or quotes**: edit `outputted_text_2024` and sync `transformed_updates` accordingly.

---

## Known quirks (OG version)

- Hover highlighting is cosmetic only; selection requires clicking a chip.  
- Exact string matching means mismatched punctuation/whitespace breaks highlights.  
- Additions without a placed snippet won’t highlight; they just show a planned insertion.

---

## Example `transformed_updates` item

```text
id: "u2"
raw_request: "Change 'Source to Manage' to 'Sourcing Guidelines' for indirect suppliers."
change_type: "modification"
standard_refs: ["ISS:A.1.0.1.2"]
rephrased_update: "Update indirect supplier process terminology to 'Sourcing Guidelines'..."
original_text_to_highlight: "A similar process called Source to Manage provides guidance..."
new_text_to_highlight: "Similarly, our Sourcing Guidelines provide guidance..."
```

---

## Handoff tips

- For each `user_input_updates` entry, ensure one corresponding `transformed_updates` item exists.  
- Validate: standards exist, snippets match text, additions include proposed insertion text.
