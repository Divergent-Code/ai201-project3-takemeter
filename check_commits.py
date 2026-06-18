# Co-Authored-By: VEGA <vega@noreply.local>
# Co-Authored-By: Hayden <hayden@noreply.local>

import subprocess
import csv
import io

commits = ["e5b01d6", "16df6e3", "3853fca", "527bb9a", "07c0ce7", "5e2d572"]

for commit in commits:
    try:
        # Run git show to get the dataset.csv file from that commit
        result = subprocess.run(
            ["git", "show", f"{commit}:dataset.csv"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True
        )
        
        # Parse the CSV contents
        csv_file = io.StringIO(result.stdout)
        reader = csv.reader(csv_file)
        header = next(reader)
        
        total = 0
        labeled = 0
        label_counts = {}
        
        for row in reader:
            total += 1
            if len(row) > 1 and row[1]:
                labeled += 1
                lbl = row[1]
                label_counts[lbl] = label_counts.get(lbl, 0) + 1
                
        print(f"Commit {commit}:")
        print(f"  Total Rows: {total}")
        print(f"  Labeled Rows: {labeled}")
        print(f"  Label Counts: {label_counts}")
        print("-" * 40)
        
    except Exception as e:
        print(f"Failed to check commit {commit}: {e}")
