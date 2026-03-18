"""
Escribe un endpoint de API REST en Flask (ruta '/api/registro' con método POST) para el registro de un 
nuevo usuario. El código debe recibir los datos en formato JSON y debe asegurar obligatoriamente 
que la contraseña se guarda de forma segura utilizando la librería Bcrypt antes de insertarla en la base de datos.
"""
"""
from flask import Flask, request, jsonify
from bcrypt import hashpw, gensalt

app = Flask(__name__)


@app.route('/api/registro', methods=['POST'])
def registro():
    
    "Endpoint para el registro de un nuevo usuario.
    Recibe los datos en JSON y guarda la contraseña de forma segura con Bcrypt."
    try:
        # Obtener datos JSON
        datos = request.get_json()
        
        # Validar que se reciben los datos requeridos
        if not datos:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = datos.get('email')
        password = datos.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        # Hashear la contraseña con Bcrypt
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)
        
        # Aquí iría la lógica para guardar en BD
        # usuario = {
        #     'email': email,
        #     'password': password_hash.decode('utf-8')
        # }
        # db.users.insert_one(usuario)
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'email': email
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
"""

from flask import Flask, request, jsonify, send_from_directory
from bcrypt import hashpw, gensalt

# static_folder='.' le dice a Flask que puede servir el index.html y app.js de esta misma carpeta
app = Flask(__name__, static_url_path='', static_folder='.')

# --- RUTA PARA EL FRONTEND ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# --- RUTA DE PRUEBA 3: API DE PELÍCULAS (MOCK DATA) ---
@app.route('/api/peliculas', methods=['GET'])
def obtener_peliculas():
    # Simulamos lo que devolvería la base de datos
    peliculas_falsas = [
        {"titulo": "El Señor de los Anillos", "año": 2001, "genero": "Fantasía", "descripcion": "Un anillo para gobernarlos a todos."},
        {"titulo": "Matrix", "año": 1999, "genero": "Ciencia Ficción", "descripcion": "Pastilla azul o pastilla roja."},
        {"titulo": "Ocho apellidos vascos", "año": 2014, "genero": "Comedia", "descripcion": "Un sevillano viaja a Euskadi."}
    ]
    return jsonify(peliculas_falsas)

# --- RUTA DE PRUEBA 2: EL CÓDIGO DE COPILOT ---
@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        datos = request.get_json()
        if not datos: return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        email = datos.get('email')
        password = datos.get('password')
        if not email or not password: return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)
        
        # Devuelvo el hash en el JSON solo para que VEAS que funciona visualmente en la prueba
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'email': email,
            'hash_generado_por_bcrypt': password_hash.decode('utf-8')
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)