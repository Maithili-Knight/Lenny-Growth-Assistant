from app.services.embedding_service import create_embedding

vector = create_embedding("FastAPI is a Python framework.")

print(f"Vector length: {len(vector)}")
print(vector[:10])