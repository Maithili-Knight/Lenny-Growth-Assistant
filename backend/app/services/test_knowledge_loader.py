from app.services.knowledge_loader import load_knowledge_base

knowledge = load_knowledge_base()

print(f"Loaded {len(knowledge)} chunks")

print()

print(knowledge[0].keys())

print()

print(knowledge[0]["text"][:300])