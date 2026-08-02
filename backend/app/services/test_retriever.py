from app.services.retriever import retrieve_context

docs = retrieve_context(
    "How do startups hire great engineers?"
)

print()

for i, doc in enumerate(docs, start=1):
    print("=" * 60)
    print(f"Chunk {i}\n")
    print(doc[:600])