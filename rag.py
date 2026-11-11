
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parent
DOCS_FOLDER = ROOT / "career_docs"

# Text embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():
    documents = []

    for file_path in DOCS_FOLDER.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        documents.append(text)

    return documents


def split_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks


def create_knowledge_index():
    documents = load_documents()

    chunks = []
    for document in documents:
        chunks.extend(split_text(document))

    if not chunks:
        raise ValueError("No career documents found in career_docs folder.")

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings.astype("float32"))

    return index, chunks


def retrieve_context(question, index, chunks, top_k=3):
    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(
        question_embedding.astype("float32"),
        min(top_k, len(chunks))
    )

    results = []

    for idx in indices[0]:
        if idx >= 0:
            results.append(chunks[idx])

    return "\n\n".join(results)
