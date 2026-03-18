"""
Escribe un endpoint de API REST en Flask (ruta '/api/registro' con método POST) para el registro de un 
nuevo usuario. El código debe recibir los datos en formato JSON y debe asegurar obligatoriamente 
que la contraseña se guarda de forma segura utilizando la librería Bcrypt antes de insertarla en la base de datos.
"""

from flask import Flask, request, jsonify
from bcrypt import hashpw, gensalt

app = Flask(__name__)


@app.route('/api/registro', methods=['POST'])
def registro():
    """
    Endpoint para el registro de un nuevo usuario.
    Recibe los datos en JSON y guarda la contraseña de forma segura con Bcrypt.
    """
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
