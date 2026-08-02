import pickle
from pathlib import Path

KNOWLEDGE_PATH = Path(__file__).resolve().parents[1] / "knowledge" / "knowledge_base.pkl"


def load_knowledge_base():
    with open(KNOWLEDGE_PATH, "rb") as f:
        return pickle.load(f)