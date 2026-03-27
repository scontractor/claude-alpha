"""Standalone CLI ingestion script. Run: python ingest.py"""
from app import config, ingestor

if __name__ == "__main__":
    print(f"Loading embedding model: {config.EMBED_MODEL}")
    embed_model = ingestor.load_embedding_model()
    client = ingestor.get_client()
    collection = ingestor.get_collection(client)

    print(f"Scanning: {config.DATA_DIR.resolve()}")
    results = ingestor.ingest_all(config.DATA_DIR, collection, embed_model)

    if not results:
        print("No supported files found.")
    else:
        for fname, count in results.items():
            print(f"  {fname}: {count} chunks")
        print(f"\nTotal chunks in store: {collection.count()}")
