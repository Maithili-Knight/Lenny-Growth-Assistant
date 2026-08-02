from app.services.chunker import chunk_text

text = """
FastAPI is a modern Python framework.

It is fast.

It supports async programming.

It automatically generates Swagger documentation.

It is widely used for AI APIs.
"""

chunks = chunk_text(text)

print(f"Total chunks: {len(chunks)}\n")

for i, chunk in enumerate(chunks, start=1):
    print("=" * 60)
    print(f"Chunk {i}")
    print(chunk)