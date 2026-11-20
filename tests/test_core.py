from app.core import GAME_DIALOGUES, preprocess_dialogues
from app.llm import NGramLanguageModel

def test_corpus_has_at_least_50_lines():
    assert len(GAME_DIALOGUES) >= 50

def test_preprocessing_cleans_text():
    assert preprocess_dialogues(["Hello, HERO!"]) == [["hello", "hero"]]

def test_model_builds_trigram_counts():
    model = NGramLanguageModel(n=3).fit(preprocess_dialogues())
    assert model.vocabulary
    assert model.counts[3]

def test_smoothing_gives_positive_probabilities():
    model = NGramLanguageModel(n=3).fit(preprocess_dialogues())
    probabilities = model.next_word_probabilities(["the", "village"])
    assert all(value > 0 for value in probabilities.values())

def test_generation_keeps_starting_phrase():
    model = NGramLanguageModel(n=3).fit(preprocess_dialogues())
    result = model.generate("the village", max_words=8)
    assert result.lower().startswith("the village")

def test_generation_is_deterministic():
    model = NGramLanguageModel(n=3).fit(preprocess_dialogues())
    assert model.generate("the village") == model.generate("the village")
