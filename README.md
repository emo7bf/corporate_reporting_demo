Concept Overview – AI-Drafted Global Impact Report

Human Rights

KLA believes in individuals’ right to work in an environment that upholds labor rights, forbids harassment and discrimination, and is free from all forms of forced labor. We recognize the potential human rights issues and labor risks that may occur in our supply chain, especially for vulnerable populations in society, including women, children and minority groups. Through our Global Human Rights Standards, we communicate our high expectations to our supply chain partners, and our global supply chain management program supports efforts to drive ongoing compliance and transparency regarding human rights throughout our supply chain. We enforce our human rights policies through our annual RBA Supplier Assessment Questionnaire (SAQ), contractual supplier requirements and ongoing supplier relationship management.


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
