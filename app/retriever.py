from sentence_transformers import SentenceTransformer

from app import config


def search(
    query: str,
    collection,
    embed_model: SentenceTransformer,
    top_k: int = config.TOP_K,
) -> list[dict]:
    # BGE models require this prefix for queries (not for documents)
    prefixed_query = config.BGE_QUERY_PREFIX + query

    query_embedding = embed_model.encode(
        [prefixed_query],
        normalize_embeddings=True,
    ).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        hits.append({
            "text": text,
            "source": meta.get("source", "unknown"),
            "chunk_index": meta.get("chunk_index", 0),
            "file_type": meta.get("file_type", ""),
            "similarity": round((1 - distance) * 100, 1),  # cosine distance -> % similarity
        })

    return hits
