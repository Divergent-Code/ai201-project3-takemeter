import csv
from collections import Counter

csv_path = 'dataset.csv'
labels = []
empty_count = 0
total_count = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for i, row in enumerate(reader):
        total_count += 1
        if len(row) > 1 and row[1]:
            labels.append(row[1])
        else:
            empty_count += 1

print(f"Total Rows: {total_count}")
print(f"Empty Labels: {empty_count}")
print("Label Distribution:")
for label, count in Counter(labels).items():
    print(f"  {label}: {count}")
