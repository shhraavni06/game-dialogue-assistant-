"""Smoothed n-gram language model with context backoff."""

from collections import Counter, defaultdict
import random
import re

class NGramLanguageModel:
    def __init__(self, n=3, k=0.1):
        if n < 2:
            raise ValueError("n must be at least 2")
        if k <= 0:
            raise ValueError("smoothing k must be positive")

        self.n = n
        self.k = float(k)
        self.counts = {
            order: defaultdict(Counter)
            for order in range(1, n + 1)
        }
        self.vocabulary = set()

    def fit(self, tokenized_dialogues):
        for order in self.counts:
            self.counts[order].clear()

        self.vocabulary.clear()

        for tokens in tokenized_dialogues:
            words = ["<s>"] * (self.n - 1) + list(tokens) + ["</s>"]
            self.vocabulary.update(tokens)
            self.vocabulary.add("</s>")

            for order in range(1, self.n + 1):
                for i in range(order - 1, len(words)):
                    context = tuple(words[i-order+1:i]) if order > 1 else ()
                    self.counts[order][context][words[i]] += 1

        return self

    def next_word_probabilities(self, context):
        """Use the longest available context with add-k smoothing."""
        if not self.vocabulary:
            raise RuntimeError("Train the model first.")

        for order in range(min(self.n, len(context) + 1), 0, -1):
            ctx = tuple(context[-(order-1):]) if order > 1 else ()
            counts = self.counts[order].get(ctx)

            if counts:
                total = sum(counts.values())
                candidates = set(counts)

                denominator = total + self.k * len(candidates)

                return {
                    word: (counts[word] + self.k) / denominator
                    for word in candidates
                }

        return {"</s>": 1.0}

    def generate(self, starting_phrase="", max_words=20, seed=7):
        if not self.vocabulary:
            raise RuntimeError("Train the model first.")

        if max_words < 1:
            raise ValueError("max_words must be positive")

        rng = random.Random(seed)
        phrase = re.findall(r"[a-z0-9']+", starting_phrase.lower())
        output = phrase[:]
        context = (["<s>"] * (self.n - 1) + phrase)[-(self.n - 1):]

        for _ in range(max_words):
            probabilities = self.next_word_probabilities(context)
            words = list(probabilities)
            weights = [probabilities[word] for word in words]

            word = rng.choices(words, weights=weights, k=1)[0]

            if word == "</s>":
                break

            output.append(word)
            context = (context + [word])[-(self.n - 1):]

        result = " ".join(output).strip()
        return result.capitalize() if result else ""
