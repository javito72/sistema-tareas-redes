# auth.py
# Funciones de autenticación y manejo de contraseñas

import bcrypt
from database import create_user, get_user_by_username

def hash_password(password):
    """
    Hash de una contraseña usando bcrypt
    """
    # Generar salt y hashear la contraseña
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verifica si una contraseña coincide con su hash
    """
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def register_user(usuario, contraseña):
    """
    Registra un nuevo usuario con contraseña hasheada
    """
    # Validaciones básicas
    if not usuario or not contraseña:
        return False, "Usuario y contraseña son obligatorios"
    
    if len(usuario) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    
    if len(contraseña) < 4:
        return False, "La contraseña debe tener al menos 4 caracteres"
    
    # Hashear la contraseña
    contraseña_hash = hash_password(contraseña)
    
    # Intentar crear el usuario
    if create_user(usuario, contraseña_hash):
        return True, "Usuario registrado exitosamente"
    else:
        return False, "El usuario ya existe"

def authenticate_user(usuario, contraseña):
    """
    Autentica un usuario verificando sus credenciales
    """
    # Obtener usuario de la base de datos
    user_data = get_user_by_username(usuario)
    
    if not user_data:
        return False, None, "Usuario no encontrado"
    
    # Verificar contraseña
    if verify_password(contraseña, user_data['contraseña_hash']):
        return True, user_data['id'], "Autenticación exitosa"
    else:
        return False, None, "Contraseña incorrecta"
