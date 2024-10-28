import openai
import os
from dotenv import load_dotenv

# Cargar la API Key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hola, ¿cómo estás?"}]
    )
    print(response['choices'][0]['message']['content'])
except Exception as e:
    print("Error:", e)
