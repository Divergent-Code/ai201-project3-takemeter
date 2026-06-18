import re

with open('dataset.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

cleaned_lines = []
for line in lines:
    # Remove any trailing spaces before commas and at the end of the line
    line = re.sub(r'\s+,', ',', line)
    line = re.sub(r'\s+$', '\n', line)
    cleaned_lines.append(line)

with open('dataset.csv', 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print("dataset.csv has been cleaned of trailing spaces!")
