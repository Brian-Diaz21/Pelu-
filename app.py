import sqlite3
from flask import Flask, render_template, request, redirect, flash, jsonify, g
from datetime import datetime

app = Flask(__name__)
app.secret_key = "alguna_clave_secreta"

DATABASE = "reservas.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            email TEXT,
            telefono TEXT,
            dia TEXT,
            hora TEXT
        )
    """)
    db.commit()

# Elimina o comenta el decorador y la función:
# @app.before_first_request
# def before_first_request():
#     init_db()

# Catálogo de servicios de peluquería
catalogo = [
    {
        "nombre": "Corte de Cabello",
        "descripcion": "Corte profesional para damas.",
        "precio": "$5000"
    },
    {
        "nombre": "Peinado",
        "descripcion": "Peinados para eventos especiales.",
        "precio": "$10000"
    },
    {
        "nombre": "Coloración",
        "descripcion": "Tintes y mechas de alta calidad.",
        "precio": "$30"
    },
    {
        "nombre": "Tratamiento Capilar",
        "descripcion": "Tratamientos para fortalecer y dar brillo.",
        "precio": "$25"
    }
]

# Lista en memoria para guardar reservas
reservas = []

@app.route("/")
def landing():
    return render_template("landing.html", catalogo=catalogo)

@app.route("/reservar", methods=["POST"])
def reservar():
    nombre = request.form.get("nombre")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    dia = request.form.get("dia")
    hora = request.form.get("hora")
    db = get_db()
    db.execute(
        "INSERT INTO reservas (nombre, email, telefono, dia, hora) VALUES (?, ?, ?, ?, ?)",
        (nombre, email, telefono, dia, hora)
    )
    db.commit()
    print(f"Reserva recibida: {nombre}, {email}, {telefono}, {dia}, {hora}")
    flash("¡Reserva enviada! Te contactaremos para confirmar tu turno.")
    return redirect("/")

@app.route("/horarios_ocupados", methods=["GET"])
def horarios_ocupados():
    dia = request.args.get("dia")
    db = get_db()
    rows = db.execute("SELECT hora FROM reservas WHERE dia = ?", (dia,)).fetchall()
    ocupados = [row["hora"] for row in rows]
    return jsonify(ocupados)

@app.route("/ver_reservas")
def ver_reservas():
    db = get_db()
    rows = db.execute("SELECT nombre, email, telefono, dia, hora FROM reservas ORDER BY dia, hora").fetchall()
    return render_template("ver_reservas.html", reservas=rows)

if __name__ == "__main__":
    with app.app_context():
        init_db()  # Inicializa la base de datos dentro del contexto de la app
    app.run(debug=True)


