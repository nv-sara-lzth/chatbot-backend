import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # Importar CORS

# Cargar la API Key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Activar CORS para todas las rutas

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "Mensaje vacío"}), 400
    
    try:
        # Llamada a la API de GPT-3.5 usando ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente irónico con muy pocas ganas de trabajar."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.8
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
