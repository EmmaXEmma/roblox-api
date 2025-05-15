from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Guardar datos en SQLite
def guardar_dato(nombre_usuario, equipo, pais):
    conexion = sqlite3.connect("datos.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            equipo TEXT,
            pais TEXT,
            fecha_hora TEXT
        )
    """)
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO jugadores (nombre, equipo, pais, fecha_hora) VALUES (?, ?, ?, ?)",
                   (nombre_usuario, equipo, pais, fecha_hora))
    conexion.commit()
    conexion.close()

@app.route('/api/registrar', methods=['POST'])
def registrar():
    datos = request.json
    guardar_dato(datos["usuario"], datos["equipo"], datos["pais"])
    return {"mensaje": "Registrado correctamente"}

@app.route('/')
def index():
    conexion = sqlite3.connect("datos.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, equipo, pais, fecha_hora FROM jugadores ORDER BY id DESC")
    datos = cursor.fetchall()
    conexion.close()
    return render_template("index.html", datos=datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
