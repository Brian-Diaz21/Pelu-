from flask import Flask, render_template

app = Flask(__name__)

# Catálogo de servicios de peluquería
catalogo = [
    {
        "nombre": "Corte de Cabello",
        "descripcion": "Corte profesional para damas y caballeros.",
        "precio": "$15"
    },
    {
        "nombre": "Peinado",
        "descripcion": "Peinados para eventos especiales.",
        "precio": "$20"
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

@app.route("/")
def landing():
    return render_template("landing.html", catalogo=catalogo)

if __name__ == "__main__":
    app.run(debug=True)
