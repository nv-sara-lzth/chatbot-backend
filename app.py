import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS  # Importar CORS

# Cargar la API Key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurar la aplicación Flask
app = Flask(__name__)
CORS(app)  # Activar CORS para todas las rutas, permitiendo que el frontend pueda hacer solicitudes a esta API

# Endpoint de la API para el chat
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint para recibir mensajes del usuario y responder usando la API de GPT-3.5.
    Espera un JSON en el formato: { "message": "tu mensaje" }
    """
    user_input = request.json.get('message')
    
    # Verificar si el mensaje está vacío
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
        
        # Obtener la respuesta de la API
        reply = response['choices'][0]['message']['content']
        
        # Responder al frontend en formato JSON
        return jsonify({"reply": reply})
    
    except Exception as e:
        # Manejo de errores, respondiendo al cliente en caso de fallo
        return jsonify({"error": "Ocurrió un error al procesar la solicitud.", "details": str(e)}), 500

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(port=5000)
