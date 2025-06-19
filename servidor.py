# servidor.py
# API Flask principal para el sistema de gestión de tareas

from flask import Flask, request, jsonify, render_template, session
import os
from database import init_database, get_user_tasks, get_user_by_username
from auth import register_user, authenticate_user
from models import validate_user_data

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = 'tu_clave_secreta_super_segura_123'  # En producción usar variable de entorno
app.config['JSON_AS_ASCII'] = False  # Para soportar caracteres especiales

# Inicializar la base de datos al arrancar
init_database()

@app.route('/')
def home():
    """
    Endpoint principal - muestra información básica del sistema
    """
    return jsonify({
        'mensaje': 'Sistema de Gestión de Tareas API',
        'version': '1.0',
        'endpoints': {
            'registro': 'POST /registro',
            'login': 'POST /login', 
            'tareas': 'GET /tareas'
        }
    })

@app.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint para registrar nuevos usuarios
    POST /registro
    Body: {"usuario": "nombre", "contraseña": "1234"}
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        # Validar que se enviaron datos
        if not data:
            return jsonify({
                'error': 'No se enviaron datos',
                'mensaje': 'El cuerpo de la petición debe contener JSON válido'
            }), 400
        
        # Validar formato de los datos
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Intentar registrar el usuario
        success, message = register_user(data['usuario'], data['contraseña'])
        
        if success:
            return jsonify({
                'mensaje': message,
                'usuario': data['usuario']
            }), 201
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión
    POST /login
    Body: {"usuario": "nombre", "contraseña": "1234"}
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        # Validar que se enviaron datos
        if not data:
            return jsonify({
                'error': 'No se enviaron datos',
                'mensaje': 'El cuerpo de la petición debe contener JSON válido'
            }), 400
        
        # Validar formato de los datos
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Intentar autenticar el usuario
        success, user_id, message = authenticate_user(data['usuario'], data['contraseña'])
        
        if success:
            # Guardar información de sesión
            session['user_id'] = user_id
            session['usuario'] = data['usuario']
            
            return jsonify({
                'mensaje': message,
                'usuario': data['usuario'],
                'sesion_iniciada': True
            }), 200
        else:
            return jsonify({'error': message}), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

@app.route('/tareas', methods=['GET'])
def tareas():
    """
    Endpoint para mostrar la página de bienvenida con las tareas
    GET /tareas
    """
    try:
        # Verificar si hay usuario en sesión
        usuario = session.get('usuario')
        user_id = session.get('user_id')
        
        tareas_usuario = []
        
        # Si hay usuario logueado, obtener sus tareas
        if user_id:
            tareas_raw = get_user_tasks(user_id)
            # Convertir las tareas a diccionarios para el template
            tareas_usuario = []
            for tarea in tareas_raw:
                tareas_usuario.append({
                    'id': tarea['id'],
                    'titulo': tarea['titulo'],
                    'descripcion': tarea['descripcion'],
                    'completada': bool(tarea['completada']),
                    'fecha_creacion': tarea['fecha_creacion']
                })
        
        # Renderizar template HTML
        return render_template('bienvenida.html', 
                             usuario=usuario, 
                             tareas=tareas_usuario)
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

@app.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint para cerrar sesión
    POST /logout
    """
    try:
        # Limpiar sesión
        session.clear()
        
        return jsonify({
            'mensaje': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error interno del servidor',
            'detalle': str(e)
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """
    Endpoint para verificar el estado del servidor
    GET /status
    """
    return jsonify({
        'estado': 'activo',
        'mensaje': 'El servidor está funcionando correctamente',
        'sesion_usuario': session.get('usuario', 'No autenticado')
    }), 200

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'mensaje': 'La ruta solicitada no existe'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejo de métodos no permitidos"""
    return jsonify({
        'error': 'Método no permitido',
        'mensaje': 'El método HTTP usado no está permitido para esta ruta'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos"""
    return jsonify({
        'error': 'Error interno del servidor',
        'mensaje': 'Ha ocurrido un error inesperado'
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor de gestión de tareas...")
    print("📡 API disponible en: http://localhost:5000")
    print("📋 Página de tareas: http://localhost:5000/tareas")
    print("📚 Endpoints disponibles:")
    print("   POST /registro - Registrar usuario")
    print("   POST /login - Iniciar sesión")
    print("   GET /tareas - Ver página de bienvenida")
    print("   POST /logout - Cerrar sesión")
    print("   GET /status - Estado del servidor")
    
    # Ejecutar la aplicación en modo debug
    app.run(debug=True, host='0.0.0.0', port=5000)
