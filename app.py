from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Leer URL de la base desde variable de entorno
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

# Crear tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL
    );
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        cur.execute("INSERT INTO registros (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        conn.commit()
        return redirect("/")
    return render_template("index.html")

# EJECUCIÓN CORRECTA PARA RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Servidor corriendo en http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
