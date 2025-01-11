from flask import Flask, render_template, request, jsonify
import re
import nltk
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Configuración inicial de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Inicializa Flask
app = Flask(__name__)

# Función para inicializar la base de datos
def inicializar_base_datos():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respuestas (
            palabra_clave TEXT NOT NULL UNIQUE,
            respuesta TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Función para insertar respuestas en la base de datos
def insertar_respuesta(palabra_clave, respuesta):
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO respuestas (palabra_clave, respuesta)
        VALUES (?, ?)
    """, (palabra_clave, respuesta))
    conexion.commit()
    conexion.close()

# Función de preprocesamiento
def preprocesar_texto(texto):
    texto = texto.lower()
    tokens = word_tokenize(texto)
    tokens = [t for t in tokens if t not in string.punctuation]
    stop_words = set(stopwords.words('spanish'))
    tokens = [t for t in tokens if t not in stop_words]
    return tokens

# Función para buscar respuesta en la base de datos
def buscar_respuesta(tokens):
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    for token in tokens:
        cursor.execute("SELECT respuesta FROM respuestas WHERE palabra_clave = ?", (token,))
        resultado = cursor.fetchone()
        if resultado:
            conexion.close()
            return resultado[0]
    conexion.close()
    return "Lo siento, no entiendo tu pregunta. ¿Puedes intentarlo de otra manera?"

# Inicializar la base de datos y agregar respuestas
inicializar_base_datos()
insertar_respuesta("horario", "Nuestro horario es de 9 a.m. a 6 p.m., de lunes a viernes.")
insertar_respuesta("servicio", "Ofrecemos servicios de atención al cliente y soporte técnico.")
insertar_respuesta("hora", "Nuestro horario es de 9 a.m. a 6 p.m., de lunes a viernes.")
insertar_respuesta("pago", "Aceptamos pago como llegue.")

# Ruta principal para la página del chatbot
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar mensajes del chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    mensaje_usuario = data.get('mensaje', '')
    tokens = preprocesar_texto(mensaje_usuario)
    respuesta = buscar_respuesta(tokens)
    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(debug=True)
