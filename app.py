"""
TakeMeter -- Discourse Quality Classifier
Gradio interface powered by the fine-tuned DistilBERT model.

Run locally:
    python app.py

Deploy to Hugging Face Spaces:
    1. Create a new Space (Gradio SDK)
    2. Upload app.py and requirements.txt
    3. The model loads from HuggingFace Hub automatically (no secrets needed)
"""

import gradio as gr
from transformers import pipeline

MODEL_ID = "DivergentCode/takemeter"

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

classifier = pipeline("text-classification", model=MODEL_ID, top_k=None)


def classify(text: str) -> tuple[str, str]:
    if not text.strip():
        return "<p style='color:#888'>Enter some text to classify.</p>", ""

    results = classifier(text.strip(), top_k=None)
    scores = {r["label"]: r["score"] for r in results}
    label = max(scores, key=scores.get)

    if label not in LABELS:
        return f"<p style='color:red'>Unexpected label: {label}</p>", ""

    color = LABEL_COLOR[label]
    display = LABEL_DISPLAY[label]
    desc = LABEL_DESC[label]

    def conf_bar(lbl):
        p = scores.get(lbl, 0) * 100
        c = LABEL_COLOR[lbl]
        return (
            f"<div style='margin:4px 0'>"
            f"<span style='display:inline-block;width:160px;font-size:0.8em;color:#555'>{LABEL_DISPLAY[lbl]}</span>"
            f"<span style='display:inline-block;background:{c};width:{p * 2:.0f}px;height:14px;border-radius:3px;vertical-align:middle'></span>"
            f" <span style='font-size:0.8em;color:#333'>{p:.0f}%</span>"
            f"</div>"
        )

    bars = "".join(conf_bar(lbl) for lbl in LABELS)

    result_html = f"""
<div style="border-left:5px solid {color};padding:12px 16px;background:#f9f9f9;border-radius:4px;margin-bottom:12px;">
  <div style="font-size:1.4em;font-weight:bold;color:{color}">{display}</div>
  <div style="font-size:0.9em;color:#555;margin-top:4px">{desc}</div>
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
Powered by a fine-tuned `distilbert-base-uncased` model ([DivergentCode/takemeter](https://huggingface.co/DivergentCode/takemeter)).
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
