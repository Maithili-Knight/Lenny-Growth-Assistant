from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "all-MiniLM-L6-v2"

model = SentenceTransformer(str(MODEL_PATH), local_files_only=True)

def create_embedding(text: str):
    return model.encode(text).tolist()