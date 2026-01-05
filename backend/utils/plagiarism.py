from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_plagiarism(current_text, existing_texts):
    # ✅ FIRST SUBMISSION CASE
    if not existing_texts:
        return 0.0   # 0% plagiarism

    documents = [current_text] + existing_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )

    return round(similarities.max() * 100, 2)

