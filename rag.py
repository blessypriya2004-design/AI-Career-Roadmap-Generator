
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


ROOT = Path(__file__).resolve().parent
DOCS_FOLDER = ROOT / "career_docs"


def load_documents():
    """Load all text files from career_docs folder."""
    documents = []

    if not DOCS_FOLDER.exists():
        raise FileNotFoundError(
            f"Career documents folder not found: {DOCS_FOLDER}"
        )

    for file_path in DOCS_FOLDER.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        if text.strip():
            documents.append(text)

    return documents


def split_text(text, chunk_size=500):
    """Split document into smaller word-based chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])

        if chunk.strip():
            chunks.append(chunk)

    return chunks


class KnowledgeIndex:
    """Stores TF-IDF vectors and document chunks."""

    def __init__(self, vectorizer, matrix):
        self.vectorizer = vectorizer
        self.matrix = matrix


def create_knowledge_index():
    """Create a TF-IDF knowledge index from career documents."""
    documents = load_documents()

    chunks = []

    for document in documents:
        chunks.extend(split_text(document))

    if not chunks:
        raise ValueError(
            "No career documents found in career_docs folder."
        )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(chunks)

    index = KnowledgeIndex(vectorizer, matrix)

    return index, chunks


def retrieve_context(question, index, chunks, top_k=3):
    """Retrieve the most relevant document chunks."""
    if not question.strip():
        return ""

    question_vector = index.vectorizer.transform([question])

    similarities = cosine_similarity(
        question_vector,
        index.matrix
    ).flatten()

    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for idx in top_indices:
        if similarities[idx] > 0:
            results.append(chunks[idx])

    return "\n\n".join(results)
