from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
DATABASE = 'chatbot.bd'

def init_db():
    """Crea la tabla respuestas si no existe."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respuestas (
            palabra_clave TEXT PRIMARY KEY,
            respuesta TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa la base de datos
init_db()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT respuesta FROM respuestas WHERE palabra_clave = ?", (user_input,))
        result = cursor.fetchone()
        conn.close()
        if result:
            response = result[0]
        else:
            response = "Lo siento, no entiendo esa palabra clave."
        return render_template('chat.html', user_input=user_input, response=response)
    return render_template('chat.html')

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':
        palabra_clave = request.form.get('palabra_clave')
        respuesta = request.form.get('respuesta')
        if 'add' in request.form:
            cursor.execute("INSERT OR IGNORE INTO respuestas (palabra_clave, respuesta) VALUES (?, ?)", 
                           (palabra_clave, respuesta))
        elif 'delete' in request.form:
            cursor.execute("DELETE FROM respuestas WHERE palabra_clave = ?", (palabra_clave,))
        elif 'update' in request.form:
            cursor.execute("UPDATE respuestas SET respuesta = ? WHERE palabra_clave = ?", 
                           (respuesta, palabra_clave))
        conn.commit()

    cursor.execute("SELECT * FROM respuestas")
    respuestas = cursor.fetchall()
    conn.close()

    return render_template('configuracion.html', respuestas=respuestas)

if __name__ == '__main__':
    app.run(debug=True)
