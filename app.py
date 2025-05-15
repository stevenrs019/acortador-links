from flask import Flask, request, redirect, render_template
import string, random, json, os

app = Flask(__name__)
DB_FILE = 'urls.json'

# Crear archivo si no existe
if not os.path.exists(DB_FILE):
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

def cargar_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def guardar_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def generar_codigo(longitud=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_larga = request.form['url']
        db = cargar_db()

        for codigo, url in db.items():
            if url == url_larga:
                return render_template('index.html', link=f"/{codigo}")

        codigo = generar_codigo()
        db[codigo] = url_larga
        guardar_db(db)
        return render_template('index.html', link=f"/{codigo}")
    
    return render_template('index.html')

@app.route('/<codigo>')
def redirigir(codigo):
    db = cargar_db()
    if codigo in db:
        return redirect(db[codigo])
    return "Enlace no encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)