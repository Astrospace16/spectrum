"""Spectrum: a teen-first conversation safety companion.

Run from this directory with ``streamlit run app.py``. The app analyzes only
text the teen chooses to paste. It does not monitor accounts or send reports.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import streamlit as st
from openai import OpenAI


APP_DIR = Path(__file__).resolve().parent
PROMPT_PATH = APP_DIR / "prompts" / "risk_analysis.txt"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
MAX_TRANSCRIPT_CHARS = 20_000
DEMO_PATH = APP_DIR / "demo_conversations.json"

RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "risk_score": {"type": "integer", "minimum": 0, "maximum": 100},
        "overall_summary": {"type": "string"},
        "red_flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [
                            "Grooming",
                            "Cyberbullying",
                            "Emotional manipulation",
                            "Age-inappropriate request",
                        ],
                    },
                    "evidence": {"type": "string"},
                    "explanation": {"type": "string"},
                    "suggested_boundary": {"type": "string"},
                },
                "required": [
                    "category",
                    "evidence",
                    "explanation",
                    "suggested_boundary",
                ],
                "additionalProperties": False,
            },
        },
        "supportive_next_steps": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "risk_score",
        "overall_summary",
        "red_flags",
        "supportive_next_steps",
    ],
    "additionalProperties": False,
}


def analyze_transcript(transcript: str) -> dict[str, Any]:
    """Send the teen-provided transcript to the model and parse its analysis."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Add OPENAI_API_KEY to your environment to analyze a conversation.")

    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{TRANSCRIPT}}", transcript)
    client = OpenAI()
    response = client.responses.create(
        model=MODEL,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "spectrum_safety_analysis",
                "strict": True,
                "schema": RESPONSE_SCHEMA,
            }
        },
    )
    return json.loads(response.output_text)


def risk_color(score: int) -> tuple[str, str]:
    if score < 30:
        return "#15803d", "Lower concern"
    if score < 65:
        return "#b45309", "Some things to look at"
    return "#b91c1c", "Higher concern"


def make_share_report(result: dict[str, Any]) -> str:
    """Create a draft the teen can review and copy; never send it automatically."""
    lines = [
        "Spectrum conversation check-in",
        "",
        f"Risk indicator: {result['risk_score']}/100",
        result["overall_summary"],
        "",
        "Things Spectrum noticed:",
    ]
    if result["red_flags"]:
        for flag in result["red_flags"]:
            lines.extend(
                [
                    f"• {flag['category']}: {flag['evidence']}",
                    f"  Why it may matter: {flag['explanation']}",
                    f"  Possible boundary: {flag['suggested_boundary']}",
                ]
            )
    else:
        lines.append("• No clear high-risk patterns were identified in the text shared.")
    if result.get("supportive_next_steps"):
        lines += ["", "Possible next steps:"]
        lines += [f"• {step}" for step in result["supportive_next_steps"]]
    lines += ["", "I chose to share this and would like your support."]
    return "\n".join(lines)


st.set_page_config(page_title="Spectrum | Your online safety companion", page_icon="🌈", layout="centered")
st.markdown(
    """
    <style>
      .stApp { background: #fbfaf8; }
      .block-container { max-width: 850px; padding-top: 2rem; }
      .spectrum-note { padding: 1rem 1.2rem; border-radius: 14px;
        background: #f0f4ff; border: 1px solid #dbe4ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌈 Spectrum")
st.subheader("Your online safety companion")
st.markdown(
    '<div class="spectrum-note">You choose what to check and what to share. '
    "Spectrum doesn’t monitor your accounts or contact anyone for you. Paste only text "
    "you’re comfortable sending to an AI service.</div>",
    unsafe_allow_html=True,
)
st.write("")

demo_conversations = json.loads(DEMO_PATH.read_text(encoding="utf-8"))
demo_titles = ["Choose a demo conversation…", *demo_conversations.keys()]
selected_demo = st.selectbox("Want to try a demo example?", demo_titles)
if st.button("Load selected demo", disabled=selected_demo == demo_titles[0]):
    st.session_state["conversation_input"] = demo_conversations[selected_demo]

with st.form("conversation_check"):
    transcript = st.text_area(
        "Paste a conversation you want help understanding",
        height=240,
        placeholder="You can remove names and personal details first. This can be a real conversation or a demo example.",
        max_chars=MAX_TRANSCRIPT_CHARS,
        key="conversation_input",
    )
    submitted = st.form_submit_button("Check this conversation", type="primary")

if submitted:
    if not transcript.strip():
        st.info("Paste a conversation first, or try one of the demo examples when available.")
    else:
        with st.spinner("Looking for patterns and preparing a clear explanation…"):
            try:
                st.session_state["spectrum_result"] = analyze_transcript(transcript.strip())
                st.session_state.pop("spectrum_error", None)
            except Exception as exc:
                # Keep the UI usable without exposing provider details or transcript contents.
                st.session_state["spectrum_error"] = str(exc)

if st.session_state.get("spectrum_error"):
    st.error(st.session_state["spectrum_error"])

result = st.session_state.get("spectrum_result")
if result:
    st.divider()
    st.header("Your check-in")
    score = max(0, min(100, int(result["risk_score"])))
    color, label = risk_color(score)
    st.markdown(
        f'<div style="padding:1rem 1.2rem;border-radius:14px;background:white;'
        f'border:1px solid #e7e5e4"><span style="font-size:2rem;font-weight:700;'
        f'color:{color}">{score}/100</span> &nbsp; <span style="color:{color};font-weight:600">'
        f'{label}</span><br><span>{result["overall_summary"]}</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("This is an AI-generated signal, not a verdict. Context matters, and you know the conversation best.")

    st.subheader("Patterns to notice")
    if result["red_flags"]:
        for index, flag in enumerate(result["red_flags"], start=1):
            with st.container(border=True):
                st.markdown(f"**{index}. {flag['category']}**")
                st.markdown(f"> {flag['evidence']}")
                st.write(flag["explanation"])
                st.markdown(f"**A boundary you could try:** {flag['suggested_boundary']}")
    else:
        st.success("No clear high-risk patterns stood out in the text you shared. That’s a good sign; it can still help to trust your instincts if something feels off.")

    if result.get("supportive_next_steps"):
        st.subheader("Options if you want support")
        for step in result["supportive_next_steps"]:
            st.markdown(f"- {step}")

    st.subheader("Share with a trusted adult")
    st.write("You’re in control. Review the draft, edit it, and decide whether to copy or share it.")
    if st.button("Prepare a shareable summary"):
        st.session_state["spectrum_share_report"] = make_share_report(result)
    if st.session_state.get("spectrum_share_report"):
        st.text_area("Your draft summary", key="spectrum_share_report", height=260)
        st.download_button(
            "Download this summary",
            data=st.session_state["spectrum_share_report"],
            file_name="spectrum-check-in.txt",
            mime="text/plain",
        )

with st.expander("Learn more: digital safety and boundaries"):
    st.markdown(
        """
        **What is grooming?** A person may build trust over time and then use it to push
        for secrecy, private contact, personal details, or things that make you uncomfortable.
        "One message alone doesn’t prove someone’s intent; repeated pressure and boundary-pushing matter.

        **What is a red flag?** A behavior worth pausing over—not proof that you did anything wrong.
        Pressure, threats, isolation, unwanted requests, and attempts to make you feel responsible
        "for someone else’s choices can all be reasons to get another perspective.

        **Setting a boundary:** You can say “I’m not comfortable with that,” stop replying,
        block or report someone, or ask a trusted adult to sit with you while you decide.
        "You don’t have to handle a worrying situation alone.

        **If you feel in immediate danger:** Contact a trusted adult or local emergency services now.
        """
    )

st.caption("Spectrum is an educational support tool. It can miss context and is not an emergency service.")
