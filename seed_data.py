import sqlite3

# Nombre de la base de datos
DATABASE = 'chatbot.bd'

# Datos de ejemplo a insertar en la tabla respuestas
datos_ejemplo = [
    ('hola', '¡Hola! ¿En qué puedo ayudarte?'),
    ('adios', '¡Adiós! Que tengas un excelente día.'),
    ('ayuda', 'Claro, dime en qué necesitas ayuda.'),
    ('gracias', 'De nada, estoy aquí para ayudarte.'),
    ('problema', '¿Qué problema tienes? Intentaré ayudarte a solucionarlo.'),
    ('chatbot', 'Soy un chatbot y estoy aquí para responder tus preguntas.'),
    ('python', 'Python es un lenguaje de programación muy poderoso y flexible.'),
    ('flask', 'Flask es un framework ligero para construir aplicaciones web en Python.')
]

# Función para agregar los datos
def seed_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Crea la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            palabra_clave TEXT PRIMARY KEY,
            respuesta TEXT NOT NULL
        )
    ''')
    
    # Inserta los datos de ejemplo
    for palabra_clave, respuesta in datos_ejemplo:
        cursor.execute("INSERT OR IGNORE INTO respuestas (palabra_clave, respuesta) VALUES (?, ?)", 
                       (palabra_clave, respuesta))
    
    # Confirma los cambios y cierra la conexión
    conn.commit()
    conn.close()
    print("Datos de ejemplo insertados correctamente.")

# Ejecuta la función
if __name__ == '__main__':
    seed_data()
