"""Save generated dialogue to a local JSON history file."""

import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path("dialogue_history.json")

def save_dialogue(prompt, dialogue, path=HISTORY_FILE):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    if path.exists():
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            records = []
    records.append({
        "starting_phrase": prompt,
        "dialogue": dialogue,
        "created_at": datetime.now().isoformat(timespec="seconds")
    })
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    return path
