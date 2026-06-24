"""
Sample 30 stratified examples (10 per class) for inter-annotator reliability study.

Usage:
    python sample_for_annotation.py

Outputs:
    annotation_sheet.csv  — id + text only; give this to your second annotator to fill in 'second_label'
    annotation_key.csv    — id + text + original_label; keep this private until after annotation
"""

import csv
import random

DATASET = "dataset.csv"
LABELS = ["critical_analysis", "visceral_reaction", "hot_take"]
SAMPLE_PER_CLASS = 10
SEED = 42

random.seed(SEED)

rows_by_label: dict[str, list] = {label: [] for label in LABELS}

with open(DATASET, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        label = row["label"].strip()
        if label in rows_by_label:
            rows_by_label[label].append((i + 1, row["text"]))  # 1-indexed to match CSV line numbers

sample: list[tuple] = []
for label in LABELS:
    pool = rows_by_label[label]
    chosen = random.sample(pool, min(SAMPLE_PER_CLASS, len(pool)))
    for row_id, text in chosen:
        sample.append((row_id, text, label))

random.shuffle(sample)

with open("annotation_sheet.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text", "second_label"])
    for row_id, text, _label in sample:
        writer.writerow([row_id, text, ""])

with open("annotation_key.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text", "original_label"])
    for row_id, text, label in sample:
        writer.writerow([row_id, text, label])

print(f"Sampled {len(sample)} examples ({SAMPLE_PER_CLASS} per class).")
print("  annotation_sheet.csv  -- share with second annotator (no labels)")
print("  annotation_key.csv    -- keep private until annotation is complete")
print()
print("Label distribution in sample:")
for label in LABELS:
    count = sum(1 for _, _, l in sample if l == label)
    print(f"  {label}: {count}")
