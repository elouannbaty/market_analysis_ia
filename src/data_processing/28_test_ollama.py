import requests

URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen3:8b",
    "prompt": "Réponds uniquement : TEST PYTHON OK",
    "stream": False
}

response = requests.post(URL, json=payload)

print("=" * 70)
print("RÉPONSE D'OLLAMA")
print("=" * 70)

print(response.json()["response"])

print("=" * 70)