"""Tiny on-device classifier + template engine for form suggestions.

The model is a TF-IDF vectoriser + Logistic Regression classifier trained
on the (purpose -> category) examples in dataset.py. At inference time we
classify the user's description into a category, then fill the matching
template from templates.py with a short topic noun extracted from the
input. No external API calls, no LLM.

This is not a magic generative model — it is a real-but-modest text
classifier. Output quality is bounded by the training data and templates.
"""
import re
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .dataset import TRAINING_EXAMPLES
from .templates import CATEGORY_LABELS, STOP_WORDS, TEMPLATES

MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"

_PIPELINE = None  # lazy-loaded singleton


def train():
    """Train and persist the classifier. Returns (pipeline, accuracy)."""
    texts = [t for t, _ in TRAINING_EXAMPLES]
    labels = [c for _, c in TRAINING_EXAMPLES]

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            stop_words="english",
            lowercase=True,
        )),
        ("clf", LogisticRegression(max_iter=1000, C=2.0)),
    ])
    pipe.fit(texts, labels)
    train_acc = pipe.score(texts, labels)
    joblib.dump(pipe, MODEL_PATH)
    return pipe, train_acc


def load():
    global _PIPELINE
    if _PIPELINE is None:
        if not MODEL_PATH.exists():
            train()
        _PIPELINE = joblib.load(MODEL_PATH)
    return _PIPELINE


def _extract_topic(text):
    """Pull a likely topic noun from the user's input.

    Cheap heuristic: strip stop words, return the first remaining 1-3 words
    capitalised. Used to fill the `{topic_title}` placeholder in templates.
    """
    words = re.findall(r"[A-Za-z][A-Za-z\-']+", text.lower())
    keep = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    if not keep:
        return ""
    snippet = " ".join(keep[:2])  # 1-2 words is enough for "Mobile App"
    return snippet.title()


def suggest(text):
    """Classify input text and return a populated form suggestion.

    Returns a dict:
        category: str
        category_label: human-readable
        confidence: float in [0, 1]
        topic: extracted noun used to fill the template
        title: suggested title
        description: suggested description
        fields: list of field dicts ready for bulk creation
        alternatives: list of (category_label, confidence) for next-best matches
    """
    text = (text or "").strip()
    if not text:
        return None

    pipe = load()
    probs = pipe.predict_proba([text])[0]
    classes = pipe.classes_
    ranked = sorted(zip(classes, probs), key=lambda x: -x[1])
    best_cat, best_conf = ranked[0]
    topic = _extract_topic(text) or "our service"

    tmpl = TEMPLATES[best_cat]
    if topic and topic.lower() not in {"our service", ""}:
        title = tmpl["title_with_topic"].format(topic_title=topic)
    else:
        title = tmpl["title_default"]

    return {
        "category": best_cat,
        "category_label": CATEGORY_LABELS[best_cat],
        "confidence": round(float(best_conf), 3),
        "topic": topic,
        "title": title,
        "description": tmpl["description"],
        "fields": tmpl["fields"],
        "alternatives": [
            {"category": c, "label": CATEGORY_LABELS[c], "confidence": round(float(p), 3)}
            for c, p in ranked[1:4]
        ],
    }


if __name__ == "__main__":
    # Train and report a quick smoke test when run as a script.
    pipe, acc = train()
    print(f"Trained. Training-set accuracy: {acc:.3f}")
    print(f"Model saved to: {MODEL_PATH}")
    print()
    for sample in [
        "customer satisfaction survey for our restaurant",
        "bug report form for our mobile app",
        "rsvp for my birthday party",
        "student feedback after the course",
        "how happy are our employees",
        "contact us for sales inquiries",
        "we want feedback after our hackathon event",
        "feedback for our new chess app product",
    ]:
        s = suggest(sample)
        print(f"  in : {sample!r}")
        print(f"  out: {s['category_label']} ({s['confidence']:.2f}) -> {s['title']!r}")
        print()
