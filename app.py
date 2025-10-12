# app.py
# Streamlit demo: Global Impact Report Drafting Tool (Responsible Sourcing focus)
# Baseline: 2024 report (hard-coded for demo)
# Working draft: in-file "2025" text (hard-coded for demo)
# Side tabs: Enter New Update, View All Changes, Review Updates

import json
import re
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

import streamlit as st
from difflib import SequenceMatcher

# --------------- Page Setup ---------------
st.set_page_config(
    page_title="Global Impact — Drafting Tool",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS (dark-mode friendly)
st.markdown(
    """
    <style>
      /* Track changes styling */
      .diff-del { text-decoration: line-through; background: rgba(255,0,0,0.12); color: #cc3344; }
      .diff-ins { text-decoration: underline;  text-decoration-thickness: 2px; background: rgba(0,255,0,0.12); color: #1f7a1f; }

      /* Snippet highlights for selected update */
      .hi-old { background: rgba(255, 196, 0, 0.35); }
      .hi-new { background: rgba(0, 167, 225, 0.25); }

      /* Chip styling */
      .chip { display: inline-block; padding: 6px 10px; margin: 4px 6px 4px 0;
              border-radius: 9999px; font-size: 0.85rem; cursor: pointer; border: 1px solid rgba(255,255,255,0.15);}
      .chip-selected { background: #41007F; color: #fff; border-color: #41007F; }
      .chip-neutral { background: rgba(127,127,127,0.15); }

      /* Headings */
      .subtle { opacity: 0.8; }

      /* Scrollable panels */
      .panel {
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 16px;
        height: 70vh;
        overflow-y: auto;
        background: rgba(255,255,255,0.03);
      }

      .legend-box {
        display: inline-block; padding: 8px 12px; border-radius: 8px;
        margin-right: 8px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.2);
      }
      .legend-ins { background: rgba(0,255,0,0.12); color: #1f7a1f; }
      .legend-del { background: rgba(255,0,0,0.12); color: #cc3344; }

      /* KLA purple accents */
      .kla-purple { color: #41007F; }
      .muted { opacity: 0.7; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------- Demo Data ---------------

# Baseline (Benchmark) 2024 — keep concise but realistic
baseline_2024 = """
Responsible Sourcing (2024)

We source materials and services with a focus on human rights, environmental stewardship, and ethical business conduct. In 2024, we expanded the Supplier Code of Conduct acknowledgement to tier-1 suppliers and completed Reasonable Country of Origin Inquiry (RCOI) for 3TG.

Our due diligence program follows the OECD Guidance and aligns with the RBA Code of Conduct. We assess supplier risk by category and geography, conduct on-site and remote audits, and issue Corrective Action Plans (CAPs) with defined timelines. We track closure and escalate where needed.

We increased material declaration completeness for new parts at release and advanced smelter/refiner mapping for tin, tantalum, tungsten, and gold. We trained priority suppliers on forced-labor indicators.

Key metrics (2024): 78% of direct spend risk-assessed; 26% of high-risk suppliers audited; 86% CAP closure within 120 days; 91% smelters conformant or active in RMAP.
""".strip()

# Working Draft (in-app) — pretend this is the evolving 2025 draft
working_draft = """
Responsible Sourcing (Draft)

We procure materials, components, and services in ways that respect human rights, minimize environmental harm, and uphold ethical conduct across all tiers. Building on our 2024 baseline, we extended Supplier Code acknowledgements to tier-1 and tier-2 and completed RCOI across 3TG and cobalt.

Our due diligence follows the OECD Guidance, aligns with RBA 8.0, and integrates a standardized CAP playbook. We risk-rank by category and geography, verify through audits, and accelerate CAP closure with re-audit protocols.

We increased new-part material declarations at release and deepened smelter/refiner traceability for 3TG. Supplier training expanded to include forced-labor indicators and grievance mechanisms.

Key outcomes (to date): 84% of direct spend risk-assessed; 38% of high-risk suppliers audited; 91% CAP closure within 90 days; 94% smelters conformant or active in RMAP.
""".strip()

# Minimal standards index
standards_index = {
    "OECD:DDG": {"source": "OECD", "title": "Due Diligence Guidance", "clause": "General"},
    "RBA:8.0": {"source": "RBA", "title": "Code of Conduct v8.0", "clause": "Labor & Ethics"},
    "ISS:A.1.0.1.2": {"source": "ISS", "title": "Supply Chain: Policy & Oversight", "clause": "A.1.0.1.2"},
}

# Example update requests and transformed items
user_input_updates = [
    {
        "id": "u1",
        "change_type": "addition",
        "request": "Add that we extended Supplier Code acknowledgements to tier-2 suppliers.",
        "section_hint": "Policy & Governance",
    },
    {
        "id": "u2",
        "change_type": "modification",
        "request": "Change 'Key metrics (2024)' to 'Key outcomes (to date)' and update values accordingly.",
        "section_hint": "Performance",
    },
]

transformed_updates = [
    {
        "id": "u1",
        "raw_request": user_input_updates[0]["request"],
        "rephrased_update": "Extend Supplier Code acknowledgements to tier-2 suppliers.",
        "change_type": "addition",
        "standard_refs": ["OECD:DDG", "ISS:A.1.0.1.2"],
        "original_text_to_highlight": "Supplier Code of Conduct acknowledgement to tier-1 suppliers",
        "new_text_to_highlight": "Supplier Code acknowledgements to tier-1 and tier-2",
    },
    {
        "id": "u2",
        "raw_request": user_input_updates[1]["request"],
        "rephrased_update": "Retitle metrics block to 'Key outcomes (to date)' and update KPI values.",
        "change_type": "modification",
        "standard_refs": ["RBA:8.0", "OECD:DDG"],
        "original_text_to_highlight": "Key metrics (2024): 78% of direct spend risk-assessed; 26% of high-risk suppliers audited; 86% CAP closure within 120 days; 91% smelters conformant or active in RMAP.",
        "new_text_to_highlight": "Key outcomes (to date): 84% of direct spend risk-assessed; 38% of high-risk suppliers audited; 91% CAP closure within 90 days; 94% smelters conformant or active in RMAP.",
    },
]

# --------------- Helpers ---------------

def tokenize_words(text: str) -> List[str]:
    # Split on word boundaries but keep punctuation as tokens
    return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)

def diff_track_changes(a: str, b: str) -> str:
    """Return HTML with word-level track changes from a→b"""
    a_tok, b_tok = tokenize_words(a), tokenize_words(b)
    sm = SequenceMatcher(None, a_tok, b_tok)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append(" ".join(a_tok[i1:i2]))
        elif tag == "delete":
            chunk = " ".join(a_tok[i1:i2])
            if chunk.strip():
                out.append(f'<span class="diff-del">{chunk}</span>')
        elif tag == "insert":
            chunk = " ".join(b_tok[j1:j2])
            if chunk.strip():
                out.append(f'<span class="diff-ins">{chunk}</span>')
        elif tag == "replace":
            del_chunk = " ".join(a_tok[i1:i2])
            ins_chunk = " ".join(b_tok[j1:j2])
            if del_chunk.strip():
                out.append(f'<span class="diff-del">{del_chunk}</span>')
            if ins_chunk.strip():
                out.append(f'<span class="diff-ins">{ins_chunk}</span>')
    # Join, fix spaces around punctuation
    html = " ".join(out)
    html = re.sub(r"\s+([,.;:!?])", r"\1", html)
    return html

def apply_exact_highlight(text: str, snippet: Optional[str], cls: str) -> str:
    """Exact substring highlight; if not found, return text unchanged."""
    if not snippet or not snippet.strip():
        return st.session_state.get("_safe_html", text)
    # Escape for regex
    q = re.escape(snippet.strip())
    def _repl(m):
        return f'<span class="{cls}">{m.group(0)}</span>'
    try:
        return re.sub(q, _repl, text, count=1, flags=re.DOTALL)
    except re.error:
        return text

def render_standards(refs: List[str]):
    with st.expander("Standards & Clauses"):
        for rid in refs:
            meta = standards_index.get(rid, {})
            st.markdown(
                f"- **{rid}** — *{meta.get('source','?')}*: {meta.get('title','?')} — {meta.get('clause','?')}"
            )

def chip(label: str, selected: bool = False):
    cls = "chip chip-selected" if selected else "chip chip-neutral"
    st.markdown(f'<span class="{cls}">{label}</span>', unsafe_allow_html=True)

def ensure_state():
    if "updates" not in st.session_state:
        st.session_state.updates = transformed_updates.copy()
    if "sel_idx" not in st.session_state:
        st.session_state.sel_idx = 0

ensure_state()

# --------------- Sidebar Tabs ---------------

with st.sidebar:
    st.markdown("## 🧰 Controls")
    tab1, tab2, tab3 = st.tabs(["Enter New Update", "View All Changes", "Review Updates"])

    with tab1:
        st.markdown("### Enter New Update")
        c1, c2 = st.columns(2)
        with c1:
            change_type = st.selectbox("Change Type", ["addition", "modification", "removal"])
        with c2:
            section_hint = st.text_input("Section (hint)", "Responsible Sourcing")

        raw_request = st.text_area("Describe the update (plain English)", height=120,
                                   placeholder="E.g., Expand Supplier Code to tier-2 and add CAP playbook reference.")
        use_llm = st.checkbox("LLM assist (rephrase + propose snippets)")
        rephrased = st.text_input("Rephrased (editable)", value="")
        orig_snip = st.text_area("Original snippet to highlight (optional)", height=80)
        new_snip = st.text_area("New snippet to highlight (optional)", height=80)
        std_refs = st.text_input("Standard refs (comma-separated)", value="OECD:DDG")

        if use_llm and not rephrased and raw_request.strip():
            # Stub: in your env, you can call OpenAI/Anthropic here to rephrase and propose snippets.
            # Example OpenAI pattern (commented to avoid runtime dependency):
            # from openai import OpenAI
            # client = OpenAI()
            # prompt = f"Rephrase this ESG update succinctly and propose one original and one new snippet:\n{raw_request}"
            # resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
            # rephrased = resp.choices[0].message.content
            # st.session_state["_llm_rephrased"] = rephrased
            st.info("LLM assist stub ready — plug your API call here.")

        if st.button("Add Update", use_container_width=True, type="primary"):
            uid = f"u{uuid.uuid4().hex[:6]}"
            entry = {
                "id": uid,
                "raw_request": raw_request.strip(),
                "rephrased_update": rephrased.strip() or raw_request.strip(),
                "change_type": change_type,
                "standard_refs": [s.strip() for s in std_refs.split(",") if s.strip()],
                "original_text_to_highlight": orig_snip.strip(),
                "new_text_to_highlight": new_snip.strip(),
                "section_hint": section_hint.strip(),
            }
            st.session_state.updates.append(entry)
            st.success(f"Added update {uid}")

    with tab2:
        st.markdown("### View All Changes (Track Changes)")
        st.caption("Full-document view showing insertions (green underline) and deletions (red strikethrough).")
        st.markdown(
            '<span class="legend-box legend-ins">Insertion</span> '
            '<span class="legend-box legend-del">Deletion</span>',
            unsafe_allow_html=True,
        )
        all_changes_html = diff_track_changes(baseline_2024, working_draft)
        st.markdown("#### Combined Track-Changes View")
        st.markdown(f'<div class="panel mono">{all_changes_html}</div>', unsafe_allow_html=True)

        st.download_button(
            "Export Combined Diff (HTML)",
            data=all_changes_html.encode("utf-8"),
            file_name="responsible_sourcing_track_changes.html",
            mime="text/html",
            use_container_width=True,
        )

    with tab3:
        st.markdown("### Review Updates (List)")
        q = st.text_input("Search updates (text or standard id)", "")
        types = st.multiselect("Filter by type", ["addition", "modification", "removal"], default=["addition", "modification", "removal"])

        filtered = []
        for u in st.session_state.updates:
            hay = " ".join([u.get("raw_request",""), u.get("rephrased_update",""), " ".join(u.get("standard_refs",[]))]).lower()
            if (not q or q.lower() in hay) and (u.get("change_type") in types):
                filtered.append(u)

        st.caption(f"{len(filtered)} updates")
        cols = st.columns(3)
        with cols[0]:
            if st.button("⟵ Prev", use_container_width=True):
                st.session_state.sel_idx = max(0, st.session_state.sel_idx - 1)
        with cols[1]:
            st.write("")
        with cols[2]:
            if st.button("Next ⟶", use_container_width=True):
                st.session_state.sel_idx = min(max(0, len(filtered)-1), st.session_state.sel_idx + 1)

        # Chips
        for i, u in enumerate(filtered):
            selected = (i == st.session_state.sel_idx)
            if st.button(f"{u['id']} · {u['change_type']}", key=f"chip_{i}"):
                st.session_state.sel_idx = i

        # Show selected update details
        if filtered:
            sel = filtered[st.session_state.sel_idx]
            st.markdown("---")
            st.markdown(f"**Selected:** `{sel['id']}` · *{sel['change_type']}* — {sel.get('section_hint','')}")
            st.markdown(f"**Request:** {sel['raw_request']}")
            st.markdown(f"**Rephrased:** {sel['rephrased_update']}")
            render_standards(sel.get("standard_refs", []))

            # Mini diff (snippet vs snippet) if both available
            old_snip = sel.get("original_text_to_highlight", "").strip()
            new_snip = sel.get("new_text_to_highlight", "").strip()
            if old_snip or new_snip:
                st.markdown("**Mini Diff (snippet → snippet)**")
                mini_html = diff_track_changes(old_snip or "", new_snip or "")
                st.markdown(f'<div class="panel mono">{mini_html}</div>', unsafe_allow_html=True)

            # Export one update
            st.download_button(
                "Export Selected Update (JSON)",
                data=json.dumps(sel, indent=2).encode("utf-8"),
                file_name=f"{sel['id']}.json",
                mime="application/json",
            )

# --------------- Main 3-Column Layout ---------------

st.markdown("# 🌱 Responsible Sourcing — AI Drafting Tool")
st.markdown(
    '<span class="muted">Baseline benchmark year: <span class="kla-purple mono">2024</span> · Working draft compares against your 2024 baseline.</span>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

# Selected update (for snippet highlighting in panels)
sel_update = None
if "updates" in st.session_state and st.session_state.updates:
    # Try to match the sidebar filtered selection; fall back to first item
    try:
        # Use the selection from tab3 if present; else default to first
        # Note: We can't read tab internal state directly; we keep sel_idx global.
        from itertools import islice
        # Build same filtered list as tab3 default (no query), for highlight fallback:
        sel_update = st.session_state.updates[min(st.session_state.sel_idx, len(st.session_state.updates)-1)]
    except Exception:
        sel_update = st.session_state.updates[0]

with left:
    st.markdown("### Baseline: 2024 Report")
    base_html = baseline_2024
    if sel_update and sel_update.get("original_text_to_highlight"):
        base_html = apply_exact_highlight(base_html, sel_update["original_text_to_highlight"], "hi-old")
    st.markdown(f'<div class="panel mono">{base_html}</div>', unsafe_allow_html=True)

with right:
    st.markdown("### Working Draft (Compared to 2024)")
    work_html = working_draft
    if sel_update and sel_update.get("new_text_to_highlight"):
        work_html = apply_exact_highlight(work_html, sel_update["new_text_to_highlight"], "hi-new")
    st.markdown(f'<div class="panel mono">{work_html}</div>', unsafe_allow_html=True)

# Export bundle
bundle = {
    "baseline_year": 2024,
    "baseline_text": baseline_2024,
    "working_draft_text": working_draft,
    "standards_index": standards_index,
    "user_input_updates": user_input_updates,
    "transformed_updates": st.session_state.updates,
}
st.download_button(
    "⬇️ Export All (JSON)",
    data=json.dumps(bundle, indent=2).encode("utf-8"),
    file_name="gir_responsible_sourcing_bundle.json",
    mime="application/json",
    use_container_width=True,
)

st.markdown("---")
st.caption("Tip: Replace the hard-coded texts with your 2024 baseline and evolving draft. The LLM assist stub is ready for your API key.")
