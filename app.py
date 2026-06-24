"""
TakeMeter -- Discourse Quality Classifier
Gradio interface powered by llama-3.3-70b-versatile via Groq.

Run locally:
    GROQ_API_KEY=your_key python app.py

Deploy to Hugging Face Spaces:
    1. Create a new Space (Gradio SDK)
    2. Upload app.py and requirements.txt
    3. Add GROQ_API_KEY as a Space secret
"""

import json
import os
import re

import gradio as gr
import groq

MODEL = "llama-3.3-70b-versatile"
LABELS = ["critical_analysis", "visceral_reaction", "hot_take"]

LABEL_DISPLAY = {
    "critical_analysis": "Critical Analysis",
    "visceral_reaction": "Visceral Reaction",
    "hot_take": "Hot Take",
}

LABEL_COLOR = {
    "critical_analysis": "#4A90D9",
    "visceral_reaction": "#E8735A",
    "hot_take": "#F5A623",
}

LABEL_DESC = {
    "critical_analysis": "A structured argument about a work's themes, craft, or lore, backed by specific reasoning.",
    "visceral_reaction": "An immediate emotional or physical response. Focus is the personal felt experience.",
    "hot_take": "A bold opinion stated as fact, with little or no supporting evidence.",
}

SYSTEM_PROMPT = """You are a classifier for horror community posts. Classify the post into exactly one of three discourse-quality labels.

Labels:
- critical_analysis: A structured argument about a work's themes, craft, pacing, subtext, or lore, backed by specific examples or reasoning. Argues or analyzes rather than asserts.
- visceral_reaction: An immediate emotional or physical response (fear, disgust, awe, boredom). Focus is the personal felt experience, not why the work succeeds.
- hot_take: A bold, confident, often contrarian opinion stated as fact, with little or no supporting evidence. Asserts a debatable value judgment rather than arguing it.

Respond with JSON only, in this exact format:
{
  "label": "<one of: critical_analysis, visceral_reaction, hot_take>",
  "confidence": {
    "critical_analysis": <0.0-1.0>,
    "visceral_reaction": <0.0-1.0>,
    "hot_take": <0.0-1.0>
  },
  "reason": "<one sentence explaining the key signal that determined the label>"
}

The three confidence values must sum to 1.0."""


def classify(text: str) -> tuple[str, str]:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return (
            "<p style='color:red'>GROQ_API_KEY environment variable not set.</p>",
            "",
        )

    client = groq.Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=200,
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()},
        ],
    )

    raw = response.choices[0].message.content.strip()
    json_match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not json_match:
        return f"<p style='color:red'>Unexpected model response: {raw[:200]}</p>", ""

    data = json.loads(json_match.group())
    label = data["label"]
    confidence = data.get("confidence", {})
    reason = data.get("reason", "")

    if label not in LABELS:
        return f"<p style='color:red'>Unexpected label: {label}</p>", ""

    total = sum(confidence.values()) or 1
    confidence = {k: v / total for k, v in confidence.items()}

    color = LABEL_COLOR[label]
    display = LABEL_DISPLAY[label]
    desc = LABEL_DESC[label]
    pct = confidence.get(label, 0) * 100

    def conf_bar(lbl):
        p = confidence.get(lbl, 0) * 100
        c = LABEL_COLOR[lbl]
        return (
            f"<div style='margin:4px 0'>"
            f"<span style='display:inline-block;width:160px;font-size:0.8em;color:#555'>{LABEL_DISPLAY[lbl]}</span>"
            f"<span style='display:inline-block;background:{c};width:{p * 2:.0f}px;height:14px;border-radius:3px;vertical-align:middle'></span>"
            f" <span style='font-size:0.8em;color:#333'>{p:.0f}%</span>"
            f"</div>"
        )

    bars = "".join(conf_bar(l) for l in LABELS)

    result_html = f"""
<div style="border-left:5px solid {color};padding:12px 16px;background:#f9f9f9;border-radius:4px;margin-bottom:12px;">
  <div style="font-size:1.4em;font-weight:bold;color:{color}">{display}</div>
  <div style="font-size:0.9em;color:#555;margin-top:4px">{desc}</div>
  <div style="font-size:0.85em;color:#333;margin-top:10px"><strong>Key signal:</strong> {reason}</div>
</div>
<div style="background:#fff;border:1px solid #e0e0e0;border-radius:4px;padding:12px">
  <div style="font-size:0.85em;font-weight:bold;color:#333;margin-bottom:6px">Confidence</div>
  {bars}
</div>
"""
    return result_html, label


EXAMPLES = [
    "The Descent isn't just a monster movie -- the cave is a physical manifestation of Sarah's grief after the crash. Every tightening passage mirrors how the film withholds her recovery.",
    "Just finished Hereditary for the first time. I literally could not breathe during the attic scene. Absolutely wrecked me.",
    "Unpopular opinion: every NoSleep creepypasta-turned-novel I've read has been disappointing. The format just doesn't translate.",
]

with gr.Blocks(title="TakeMeter") as demo:
    gr.Markdown(
        """# TakeMeter
### Discourse Quality Classifier for Horror Communities
Classifies horror-community posts into **Critical Analysis**, **Visceral Reaction**, or **Hot Take**.
Powered by `llama-3.3-70b-versatile` via Groq.
"""
    )

    with gr.Row():
        with gr.Column(scale=3):
            text_input = gr.Textbox(
                label="Post text",
                placeholder="Paste a Reddit post or write your own take...",
                lines=5,
            )
            classify_btn = gr.Button("Classify", variant="primary")
            gr.Examples(examples=EXAMPLES, inputs=text_input, label="Try an example")

        with gr.Column(scale=2):
            result_output = gr.HTML(label="Result")
            label_output = gr.Textbox(label="Predicted label", interactive=False)

    classify_btn.click(
        fn=classify,
        inputs=text_input,
        outputs=[result_output, label_output],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
