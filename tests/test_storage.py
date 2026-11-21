import json
from app.storage import save_dialogue


def test_save_dialogue_creates_history_file(tmp_path):
    history = tmp_path / "history.json"

    result = save_dialogue("the village", "The village is safe", history)

    assert result == history
    records = json.loads(history.read_text(encoding="utf-8"))
    assert len(records) == 1
    assert records[0]["starting_phrase"] == "the village"
    assert records[0]["dialogue"] == "The village is safe"
    assert "created_at" in records[0]


def test_save_dialogue_appends_to_existing_history(tmp_path):
    history = tmp_path / "history.json"

    save_dialogue("the king", "The king is waiting", history)
    save_dialogue("the dragon", "The dragon sleeps", history)

    records = json.loads(history.read_text(encoding="utf-8"))
    assert len(records) == 2
    assert records[1]["starting_phrase"] == "the dragon"


def test_save_dialogue_recovers_from_corrupted_history(tmp_path):
    history = tmp_path / "history.json"
    history.write_text("invalid json", encoding="utf-8")

    save_dialogue("the wizard", "The wizard knows", history)

    records = json.loads(history.read_text(encoding="utf-8"))
    assert len(records) == 1
    assert records[0]["starting_phrase"] == "the wizard"
