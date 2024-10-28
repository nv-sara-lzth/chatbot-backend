import openai
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Cargar la API Key desde el archivo .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurar la aplicación Flask y la base de datos SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'  # Base de datos SQLite llamada "chat.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Permitir CORS para todas las rutas

# Definir el modelo de Mensaje
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10))  # "user" o "bot"
    text = db.Column(db.String(500))

# Crear la base de datos
with app.app_context():
    db.create_all()

# Endpoint para manejar el chat y almacenar mensajes
@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    # Verificar que el mensaje no esté vacío
    if not user_input:
        return jsonify({"error": "Mensaje vacío"}), 400

    # Guardar el mensaje del usuario en la base de datos
    user_message = Message(sender="user", text=user_input)
    db.session.add(user_message)
    db.session.commit()
    
    try:
        # Llamada a la API de GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente irónico con muy pocas ganas de trabajar."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.8
        )
        
        # Obtener y guardar la respuesta del bot
        bot_reply = response['choices'][0]['message']['content']
        bot_message = Message(sender="bot", text=bot_reply)
        db.session.add(bot_message)
        db.session.commit()
        
        # Enviar la respuesta al usuario
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Nuevo endpoint para obtener el historial de mensajes
@app.route('/api/messages', methods=['GET'])
def get_messages():
    # Obtener todos los mensajes de la base de datos
    messages = Message.query.all()
    # Formatear los mensajes en una lista de diccionarios
    all_messages = [{"sender": msg.sender, "text": msg.text} for msg in messages]
    # Devolver la lista de mensajes en formato JSON
    return jsonify(all_messages)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(port=5000)
