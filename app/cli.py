"""Command-line interface for the Game Dialogue Assistant."""

import argparse
from app.core import GAME_DIALOGUES, preprocess_dialogues
from app.llm import NGramLanguageModel
from app.storage import save_dialogue

def build_model(n=3, smoothing=0.1):
    return NGramLanguageModel(n=n, k=smoothing).fit(
        preprocess_dialogues()
    )

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate NPC dialogue using a smoothed n-gram model."
    )
    parser.add_argument("--start", help="Starting phrase")
    parser.add_argument("--words", type=int, default=20)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--smoothing", type=float, default=0.1)
    args = parser.parse_args(argv)

    model = build_model(args.n, args.smoothing)

    print("Game Dialogue Assistant")
    print("Corpus lines:", len(GAME_DIALOGUES))
    print(f"Model: {args.n}-gram with add-k smoothing")

    if args.start is not None:
        prompt = args.start
        dialogue = model.generate(prompt, args.words)
        print("\nGenerated dialogue:")
        print(dialogue)
        print("Saved to:", save_dialogue(prompt, dialogue))
        return

    print("Enter a starting phrase. Type 'exit' to quit.")

    while True:
        prompt = input("\nStarting phrase: ").strip()

        if prompt.lower() == "exit":
            break

        if not prompt:
            print("Please enter a starting phrase.")
            continue

        dialogue = model.generate(prompt, args.words)
        print("\nNPC:", dialogue)
        save_dialogue(prompt, dialogue)
        print("Dialogue saved.")

if __name__ == "__main__":
    main()
