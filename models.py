# models.py
# Modelos de datos y estructuras

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    """
    Modelo de datos para un usuario
    """
    id: int
    usuario: str
    contraseña_hash: str
    fecha_registro: datetime
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin contraseña)"""
        return {
            'id': self.id,
            'usuario': self.usuario,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

@dataclass
class Tarea:
    """
    Modelo de datos para una tarea
    """
    id: int
    usuario_id: int
    titulo: str
    descripcion: Optional[str]
    completada: bool
    fecha_creacion: datetime
    
    def to_dict(self):
        """Convierte la tarea a diccionario"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

def validate_user_data(data):
    """
    Valida los datos de usuario para registro/login
    """
    if not isinstance(data, dict):
        return False, "Los datos deben estar en formato JSON"
    
    if 'usuario' not in data or 'contraseña' not in data:
        return False, "Se requieren campos 'usuario' y 'contraseña'"
    
    if not data['usuario'] or not data['contraseña']:
        return False, "Usuario y contraseña no pueden estar vacíos"
    
    return True, "Datos válidos"

def validate_task_data(data):
    """
    Valida los datos de una tarea
    """
    if not isinstance(data, dict):
        return False, "Los datos deben estar en formato JSON"
    
    if 'titulo' not in data:
        return False, "Se requiere el campo 'titulo'"
    
    if not data['titulo'] or not data['titulo'].strip():
        return False, "El título no puede estar vacío"
    
    return True, "Datos válidos"
