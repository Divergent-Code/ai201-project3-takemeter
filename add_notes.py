# Co-Authored-By: VEGA <vega@noreply.local>
# Co-Authored-By: Hayden <hayden@noreply.local>

import csv

rows = []
modified = 0

with open('dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for idx, row in enumerate(reader):
        # Grow the row to have 3 elements [text, label, notes] if it doesn't
        while len(row) < 3:
            row.append('')
        
        # Check specific rows to insert notes
        text = row[0]
        if "Oddity - im confused" in text:
            row[2] = "Tricky case: asking a specific plot question but also functions as a movie discussion starter."
            modified += 1
        elif "Drag Me To Hell is highly underrated" in text:
            row[2] = "Edge case: presents a hot take/opinion but structures it as an open question to the community."
            modified += 1
        elif "Presence (Movie) - SPOILER AHEAD!!!!!!" in text:
            row[2] = "Tricky case: contains deep critical analysis of themes/time mechanics, but framed with personal commentary."
            modified += 1
            
        rows.append(row)

with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Added notes to {modified} rows.")
