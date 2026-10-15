from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
DB_NAME = 'usuarios.db'

def inicializar_db():
    # Crear tabla de usuarios si no existe
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan datos de usuario o contraseña"}), 400

    usuario = datos['usuario']
    # Hashear la contraseña antes de guardarla
    hash_pw = generate_password_hash(datos['contraseña'])

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', (usuario, hash_pw))
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    if not datos or 'usuario' not in datos or 'contraseña' not in datos:
        return jsonify({"error": "Faltan credenciales"}), 400

    usuario = datos['usuario']
    contraseña = datos['contraseña']

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT contraseña FROM usuarios WHERE usuario = ?', (usuario,))
        fila = cursor.fetchone()

    # Verificar si el usuario existe y si el hash coincide
    if fila and check_password_hash(fila[0], contraseña):
        return jsonify({"mensaje": "Inicio de sesión exitoso. Acceso permitido a /tareas"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    # Devolver HTML de bienvenida según la consigna
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
            .contenedor { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
            <p>Has accedido correctamente al panel de tareas del servidor.</p>
        </div>
    </body>
    </html>
    """
    return html_content, 200

if __name__ == '__main__':
    inicializar_db()
    print("Iniciando servidor API en http://localhost:5000...")
    app.run(host='localhost', port=5000, debug=True)