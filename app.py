from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Conexión a la base de datos de Render
DATABASE_URL = "postgresql://registro_usuarios_ib02_user:pxi96oz6qnB7Rixx5ASYeHvqu1DBsXAE@dpg-d1srsuruibrs738jeki0-a.oregon-postgres.render.com/registro_usuarios_ib02"
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

if __name__ == "__main__":
    app.run(debug=True)
