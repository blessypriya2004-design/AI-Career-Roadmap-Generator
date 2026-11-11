import os
from pathlib import Path

import faiss
import numpy as np
from openai import OpenAI


ROOT = Path(__file__).resolve().parent
DOCS_FOLDER = ROOT / "career_docs"


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    return OpenAI(api_key=api_key)


def load_documents():
    documents = []

    for file_path in DOCS_FOLDER.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        if text.strip():
            documents.append(text)

    return documents


def split_text(text, chunk_size=500):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def get_embeddings(texts):
    client = get_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return np.array(
        [item.embedding for item in response.data],
        dtype="float32"
    )


def create_knowledge_index():
    documents = load_documents()

    chunks = []
    for document in documents:
        chunks.extend(split_text(document))

    if not chunks:
        raise ValueError("No career documents found in career_docs folder.")

    embeddings = get_embeddings(chunks)
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, chunks


def retrieve_context(question, index, chunks, top_k=3):
    question_embedding = get_embeddings([question])
    faiss.normalize_L2(question_embedding)

    scores, indices = index.search(
        question_embedding,
        min(top_k, len(chunks))
    )

    results = []

    for idx in indices[0]:
        if idx >= 0:
            results.append(chunks[idx])

    return "\n\n".join(results)
