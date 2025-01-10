import re
import nltk
import sqlite3
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Descarga de datos necesarios para NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Función para inicializar la base de datos
def inicializar_base_datos():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    # Crear tabla de respuestas si no existe
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
    texto = texto.lower()  # Convierte a minúsculas
    tokens = word_tokenize(texto)  # Tokeniza el texto
    tokens = [t for t in tokens if t not in string.punctuation]  # Quita puntuación
    stop_words = set(stopwords.words('spanish'))  # Define palabras irrelevantes
    tokens = [t for t in tokens if t not in stop_words]  # Filtra palabras irrelevantes
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
            return resultado[0]  # Devuelve la respuesta encontrada
    conexion.close()
    return "Lo siento, no entiendo tu pregunta. ¿Puedes intentarlo de otra manera?"

# Función principal del chatbot
def chatbot(mensaje):
    tokens = preprocesar_texto(mensaje)  # Preprocesa el mensaje del usuario
    return buscar_respuesta(tokens)  # Busca la respuesta en la base de datos

# Inicializar la base de datos y agregar algunas respuestas
inicializar_base_datos()

# Insertar algunas respuestas de ejemplo (esto se puede hacer también dinámicamente desde la interfaz)
insertar_respuesta("horario", "Nuestro horario es de 9 a.m. a 6 p.m., de lunes a viernes.")
insertar_respuesta("servicio", "Ofrecemos servicios de atención al cliente y soporte técnico.")
insertar_respuesta("hora", "Nuestro horario es de 9 a.m. a 6 p.m., de lunes a viernes.")
insertar_respuesta("pago", "Aceptamos pago como llegue.")

# Ciclo de interacción con el usuario
print("Chatbot: ¡Hola! Soy un chatbot con base de datos. Escribe 'adiós' para salir.")
while True:
    usuario = input("Tú: ")
    
    if usuario.lower() == "adiós":
        print("Chatbot: ¡Adiós! Que tengas un buen día.")
        break
    
    respuesta = chatbot(usuario)
    print(f"Chatbot: {respuesta}")
