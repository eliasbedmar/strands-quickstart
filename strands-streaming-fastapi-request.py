import requests

response = requests.post(
    "http://localhost:8000/stream",
    json={"prompt": "What is 42+7 and tell me about Paris?"},
    stream=True
)

for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if chunk:
        print(chunk, end='', flush=True)
