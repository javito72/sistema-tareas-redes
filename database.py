# database.py
# Configuración y manejo de la base de datos SQLite

import sqlite3
import os
from contextlib import contextmanager

# Nombre del archivo de la base de datos
DATABASE_FILE = 'tareas.db'

def init_database():
    """
    Inicializa la base de datos y crea las tablas necesarias
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña_hash TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de tareas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                completada BOOLEAN DEFAULT FALSE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        conn.commit()
        print("Base de datos inicializada correctamente")

@contextmanager
def get_db_connection():
    """
    Context manager para manejar conexiones a la base de datos
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    try:
        yield conn
    finally:
        conn.close()

def create_user(usuario, contraseña_hash):
    """
    Crea un nuevo usuario en la base de datos
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO usuarios (usuario, contraseña_hash) VALUES (?, ?)',
                (usuario, contraseña_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Usuario ya existe

def get_user_by_username(usuario):
    """
    Obtiene un usuario por su nombre de usuario
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, usuario, contraseña_hash FROM usuarios WHERE usuario = ?',
            (usuario,)
        )
        return cursor.fetchone()

def get_user_tasks(usuario_id):
    """
    Obtiene todas las tareas de un usuario
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tareas WHERE usuario_id = ? ORDER BY fecha_creacion DESC',
            (usuario_id,)
        )
        return cursor.fetchall()
