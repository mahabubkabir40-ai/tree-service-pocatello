import json
import os

log_path = r"C:\Users\USER\Desktop\Tree Service Pocatello\scratch\search_transcript.py" # wait, the real path is in brain
log_path = r"C:\Users\USER\.gemini\antigravity\brain\00651c66-d23b-49d4-aa84-8e1e7f7e3075\.system_generated\logs\transcript_full.jsonl"
if not os.path.exists(log_path):
    log_path = r"C:\Users\USER\.gemini\antigravity\brain\00651c66-d23b-49d4-aa84-8e1e7f7e3075\.system_generated\logs\transcript.jsonl"

if os.path.exists(log_path):
    print("Found transcript log!")
    with open(log_path, 'r', encoding='utf-8') as f:
        count = 0
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index", 0)
                content = str(data.get("content", ""))
                tool_calls = str(data.get("tool_calls", ""))
                
                # Check for image replacement or file writes
                if "replace_file_content" in tool_calls or "write_to_file" in tool_calls:
                    if ".jpg" in tool_calls or ".png" in tool_calls or "img" in tool_calls:
                        print(f"Step {step}: {tool_calls[:300]}")
                        count += 1
            except Exception as e:
                pass
        print(f"Total matching steps: {count}")
else:
    print("Transcript log not found!")
