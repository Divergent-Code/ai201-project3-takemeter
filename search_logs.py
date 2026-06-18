import json
import re

log_path = r"C:\Users\onika\.gemini\antigravity-ide\brain\0ba144c0-e5a1-4483-81d2-69c257f010e4\.system_generated\logs\transcript.jsonl"

print("Searching transcript.jsonl for labels and python scripts...")
patterns = [
    re.compile(r"label_map", re.IGNORECASE),
    re.compile(r"apply_labels", re.IGNORECASE),
    re.compile(r"dataset\.csv", re.IGNORECASE),
    re.compile(r"critical_analysis", re.IGNORECASE),
]

with open(log_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            content = data.get("content", "")
            # check if any pattern matches in content
            matched = False
            for p in patterns:
                if p.search(content):
                    matched = True
                    break
            
            if matched:
                print(f"\n--- MATCH FOUND AT LINE {i+1} (step_index={data.get('step_index')}, source={data.get('source')}, type={data.get('type')}) ---")
                # print first 500 characters of content
                preview = content[:1500]
                print(preview)
                if len(content) > 1500:
                    print("... [TRUNCATED] ...")
        except Exception as e:
            print(f"Error parsing line {i+1}: {e}")
