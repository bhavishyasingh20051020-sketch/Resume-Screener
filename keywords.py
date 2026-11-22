from keybert import KeyBERT
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from matcher import get_model

_kw_model = None

EXTRA_STOPWORDS = {
    "developer", "join", "team", "requirements", "responsibilities", "looking",
    "experience", "plus", "bonus", "knowledge", "understanding", "strong",
    "familiarity", "good", "grasp", "role", "company", "years", "work",
    "working", "skills", "ability", "opportunity", "candidate", "candidates",
}
STOP_WORDS = list(ENGLISH_STOP_WORDS.union(EXTRA_STOPWORDS))


def get_kw_model():
    global _kw_model
    if _kw_model is None:
        _kw_model = KeyBERT(model=get_model())
    return _kw_model


def extract_keywords(text, top_n=15):
    kw_model = get_kw_model()
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1),
        stop_words=STOP_WORDS,
        top_n=top_n,
        use_mmr=True,
        diversity=0.5,
    )
    return [kw for kw, score in keywords]


def find_missing_keywords(resume_text, jd_text, top_n=15):
    jd_keywords = extract_keywords(jd_text, top_n=top_n)
    resume_lower = resume_text.lower()
    return [kw for kw in jd_keywords if kw.lower() not in resume_lower]
