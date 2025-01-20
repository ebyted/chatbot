import sqlite3

# Ruta de la base de datos
DATABASE = 'chatbot.bd'

def ver_respuestas():
    """Ver todas las respuestas en la tabla 'respuestas'."""
    # Conectar a la base de datos
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener todas las respuestas
    cursor.execute("SELECT * FROM respuestas")
    respuestas = cursor.fetchall()

    # Mostrar las respuestas
    print("Contenido de la tabla 'respuestas':")
    for respuesta in respuestas:
        print(f"Palabra clave: {respuesta[0]}, Respuesta: {respuesta[1]}")

    # Cerrar la conexión
    conn.close()

# Llamar a la función para ver las respuestas
ver_respuestas()
