# Game Dialogue Assistant

A command-line tool that helps game designers generate short, consistent NPC dialogue snippets from a small game-script corpus.

## Features

1. Collects a sample corpus of game dialogue lines.
2. Preprocesses text by lowercasing, cleaning punctuation, and tokenizing.
3. Builds a trigram (n-gram) language model.
4. Uses add-k smoothing to avoid zero-probability next-word choices.
5. Generates dialogue one word at a time from a starting phrase.
6. Provides an interactive CLI and saves generated dialogue to JSON.

## Requirements

- Python 3.9 or later
- No third-party packages are needed to run the application.
- `pytest` is only needed to run the tests locally.

## Run the application

From the project root:

```bash
python -m app.cli
```

Enter a starting phrase when prompted. Type `exit` to quit.

You can also generate dialogue directly:

```bash
python -m app.cli --start "the village" --words 20
```

Choose a different n-gram size or smoothing value:

```bash
python -m app.cli --start "the king" --n 3 --smoothing 1.0 --words 20
```

Generated dialogue is appended to `dialogue_history.json`.

## Run tests

Install pytest if it is not already available:

```bash
python -m pip install pytest
python -m pytest -q
```

The GitHub Actions workflow runs the test suite on pushes and pull requests.

## Project structure

```text
game-dialogue-assistant/
  .env.example
  .github/workflows/ci.yml
  .gitignore
  README.md
  app/
    __init__.py
    cli.py
    core.py
    llm.py
    storage.py
  pytest.ini
  requirements.txt
  tests/
    test_core.py
    test_smoke.py
```

## Model note

This is a lightweight statistical language model, not GPT-2 or a neural network. The sample corpus is intentionally small for a simple, dependency-free project demonstration. For stronger and more coherent dialogue, replace the sample lines with a larger, properly licensed game-script corpus.
