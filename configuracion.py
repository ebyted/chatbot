from flask import Flask, render_template, request, redirect, send_file, url_for
import sqlite3

app = Flask(__name__)

# Función para conectar a la base de datos
def conectar_db():
    return sqlite3.connect("chatbot.db")

# Ruta para la página principal que muestra las respuestas
@app.route('/')
def indexconfig():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM respuestas;")
    respuestas = cursor.fetchall()
    conexion.close()
    return render_template('indexconfig.html', respuestas=respuestas)

# Ruta para agregar una nueva respuesta
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_respuesta():
    if request.method == 'POST':
        palabra_clave = request.form['palabra_clave']
        respuesta = request.form['respuesta']
        
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO respuestas (palabra_clave, respuesta) VALUES (?, ?);", (palabra_clave, respuesta))
        conexion.commit()
        conexion.close()
        
        return redirect(url_for('indexconfig'))
    
    return render_template('agregar_respuesta.html')

# Ruta para editar una respuesta
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_respuesta(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM respuestas WHERE id = ?;", (id,))
    respuesta = cursor.fetchone()
    
    if request.method == 'POST':
        nueva_respuesta = request.form['respuesta']
        cursor.execute("UPDATE respuestas SET respuesta = ? WHERE id = ?;", (nueva_respuesta, id))
        conexion.commit()
        conexion.close()
        return redirect(url_for('indexconfig'))
    
    conexion.close()
    return render_template('editar_respuesta.html', respuesta=respuesta)

# Ruta para eliminar una respuesta
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar_respuesta(id):
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM respuestas WHERE id = ?;", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('indexconfig'))



if __name__ == '__main__':
    app.run(debug=True)
