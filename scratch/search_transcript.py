import json
import os

log_path = r"C:\Users\USER\.gemini\antigravity\brain\00651c66-d23b-49d4-aa84-8e1e7f7e3075\.system_generated\logs\transcript.jsonl"
if os.path.exists(log_path):
    print("Found transcript log!")
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "jpg" in line or "png" in line or "image" in line:
                # print a snippet of the line
                print(line[:200])
else:
    print("Transcript log not found!")
