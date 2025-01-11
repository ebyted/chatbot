from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def conectar_db():
    return sqlite3.connect("chatbot.db")

# Ruta para la página principal que muestra el chat
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar las respuestas del chat
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_message = request.form['message']
    
    # Preprocesar y encontrar respuesta (debes adaptar la lógica de procesamiento del mensaje)
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM respuestas;")
    respuestas = cursor.fetchall()
    
    # Implementar lógica de búsqueda de la respuesta
    respuesta = "Lo siento, no entiendo tu pregunta."
    for item in respuestas:
        if item[1] in user_message:
            respuesta = item[2]
            break

    conexion.close()
    
    return jsonify({'response': respuesta})

if __name__ == '__main__':
    app.run(debug=True)
