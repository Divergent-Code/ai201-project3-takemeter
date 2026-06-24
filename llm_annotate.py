"""
Second-annotator pass using Groq (llama-3.3-70b-versatile).

The model receives only the three label definitions -- no examples from the dataset,
no knowledge of the original labels. This mirrors a naive human annotator who has
read the rubric but has not seen the data.

Usage:
    python llm_annotate.py

Requires GROQ_API_KEY environment variable.
Writes second_label into annotation_sheet.csv in-place.
"""

import csv
import os
import groq

SHEET = "annotation_sheet.csv"
MODEL = "llama-3.3-70b-versatile"
VALID_LABELS = {"critical_analysis", "visceral_reaction", "hot_take"}

SYSTEM_PROMPT = """You are a text classifier. Classify posts from horror film and literature communities into exactly one of three labels. Reply with only the label name -- no explanation, no punctuation.

Labels:
- critical_analysis: A structured argument about a work's themes, craft, pacing, subtext, or lore, backed by specific examples or reasoning. Argues or analyzes rather than asserts.
- visceral_reaction: An immediate emotional or physical response (fear, disgust, awe, boredom). Focus is the personal felt experience, not why the work succeeds.
- hot_take: A bold, confident, often contrarian opinion stated as fact, with little or no supporting evidence. Asserts a debatable value judgment rather than arguing it.

Output exactly one of: critical_analysis, visceral_reaction, hot_take"""


def classify(client: groq.Groq, text: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=20,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    label = response.choices[0].message.content.strip().lower()
    if label not in VALID_LABELS:
        print(f"  [warn] unexpected response: {label!r} -- defaulting to hot_take")
        label = "hot_take"
    return label


def main():
    client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])

    with open(SHEET, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Classifying {len(rows)} examples with {MODEL}...")
    for i, row in enumerate(rows, 1):
        label = classify(client, row["text"])
        row["second_label"] = label
        print(f"  [{i:2d}/{len(rows)}] {label}")

    with open(SHEET, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone. Labels written to {SHEET}.")


if __name__ == "__main__":
    main()
