from app.services.ollama_service import generate_response

response = generate_response("Say hello in one sentence.")

print(response)