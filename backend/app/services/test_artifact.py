from app.services.ollama_service import generate_artifact

artifact = generate_artifact(
    artifact_type="summary",
    prompt="Summarize the benefits of Artificial Intelligence in software engineering."
)

print(artifact)