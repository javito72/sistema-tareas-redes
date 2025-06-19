# 🚀 Sistema de Gestión de Tareas - API REST

Un sistema completo de gestión de tareas con API REST, autenticación segura y base de datos SQLite.

## 📋 Características

- ✅ **API REST** con endpoints funcionales
- 🔐 **Autenticación segura** con contraseñas hasheadas (bcrypt)
- 💾 **Base de datos SQLite** para persistencia de datos
- 🌐 **Interfaz web** de bienvenida
- 📱 **Fácil integración** con Postman o cualquier cliente HTTP

## 🛠️ Tecnologías Utilizadas

- **Python 3.7+**
- **Flask** - Framework web
- **SQLite** - Base de datos
- **bcrypt** - Hasheo seguro de contraseñas
- **HTML/CSS** - Interfaz de usuario

## 📁 Estructura del Proyecto

```
sistema-tareas/
│
├── servidor.py           # API Flask principal
├── database.py           # Configuración de base de datos
├── auth.py               # Funciones de autenticación
├── models.py             # Modelos de datos
├── templates/            # Templates HTML
│   └── bienvenida.html   # Página de bienvenida
├── screenshots/             # Capturas de pantalla de pruebas con Postman
│   ├── login_test.png
│   └── registro_test.png
├── requirements.txt      # Dependencias
└── README.md             # Explicación paso a paso del sistema implementado
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/javito72/sistema-tareas-redes.git
cd sistema-tareas-redes
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Servidor

```bash
python servidor.py
```

El servidor se iniciará en `http://localhost:5000`

## 📡 Endpoints de la API

### 1. Registro de Usuario
- **URL:** `POST /registro`
- **Body:** 
```json
{
    "usuario": "mi_usuario",
    "contraseña": "mi_contraseña"
}
```
- **Respuesta Exitosa (201):**
```json
{
    "mensaje": "Usuario registrado exitosamente",
    "usuario": "mi_usuario"
}
```

### 2. Inicio de Sesión
- **URL:** `POST /login`
- **Body:**
```json
{
    "usuario": "mi_usuario",
    "contraseña": "mi_contraseña"
}
```
- **Respuesta Exitosa (200):**
```json
{
    "mensaje": "Autenticación exitosa",
    "usuario": "mi_usuario",
    "sesion_iniciada": true
}
```

### 3. Ver Tareas (Página de Bienvenida)
- **URL:** `GET /tareas`
- **Descripción:** Muestra una página HTML de bienvenida con las tareas del usuario

### 4. Cerrar Sesión
- **URL:** `POST /logout`
- **Respuesta Exitosa (200):**
```json
{
    "mensaje": "Sesión cerrada exitosamente"
}
```

### 5. Estado del Servidor
- **URL:** `GET /status`
- **Respuesta:**
```json
{
    "estado": "activo",
    "mensaje": "El servidor está funcionando correctamente",
    "sesion_usuario": "mi_usuario"
}
```

## 🧪 Pruebas con Postman

### Configuración Inicial
1. Abrir Postman
2. Crear una nueva colección llamada "Sistema Tareas"
3. Configurar la URL base: `http://localhost:5000`

### Secuencia de Pruebas Recomendada

#### 1. Verificar Estado del Servidor
- **Método:** GET
- **URL:** `http://localhost:5000/status`
- **Headers:** Content-Type: application/json

#### 2. Registrar Usuario
- **Método:** POST
- **URL:** `http://localhost:5000/registro`
- **Headers:** Content-Type: application/json
- **Body (raw JSON):**
```json
{
    "usuario": "testuser",
    "contraseña": "1234"
}
```

#### 3. Iniciar Sesión
- **Método:** POST
- **URL:** `http://localhost:5000/login`
- **Headers:** Content-Type: application/json
- **Body (raw JSON):**
```json
{
    "usuario": "testuser",
    "contraseña": "1234"
}
```

#### 4. Ver Página de Tareas
- **Método:** GET
- **URL:** `http://localhost:5000/tareas`
- **Nota:** Este endpoint devuelve HTML, verás la página de bienvenida

#### 5. Cerrar Sesión
- **Método:** POST
- **URL:** `http://localhost:5000/logout`

### Casos de Prueba Adicionales

#### Registro con Usuario Existente
```json
{
    "usuario": "testuser",
    "contraseña": "otra_contraseña"
}
```
**Resultado esperado:** Error 400 - "El usuario ya existe"

#### Login con Credenciales Incorrectas
```json
{
    "usuario": "testuser",
    "contraseña": "contraseña_incorrecta"
}
```
**Resultado esperado:** Error 401 - "Contraseña incorrecta"

#### Datos Incompletos
```json
{
    "usuario": "test"
}
```
**Resultado esperado:** Error 400 - "Se requieren campos 'usuario' y 'contraseña'"

## 🔧 Configuración para Desarrollo

### Variables de Entorno (Opcional)
Puedes crear un archivo `.env` para configuraciones:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_super_segura_123
DATABASE_URL=tareas.db
```

### Modo Debug
El servidor ya está configurado para ejecutarse en modo debug por defecto, lo que permite:
- Recarga automática al cambiar código
- Mensajes de error detallados
- Debugging interactivo

## 📊 Base de Datos

### Estructura de Tablas

#### Tabla `usuarios`
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contraseña_hash TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Tabla `tareas`
```sql
CREATE TABLE tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    completada BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
);
```

### Gestión de la Base de Datos
- La base de datos se crea automáticamente al ejecutar el servidor
- Archivo: `tareas.db` (SQLite)
- Las contraseñas se almacenan hasheadas con bcrypt (nunca en texto plano)

## 🔒 Seguridad

### Características de Seguridad Implementadas
- ✅ **Hasheo de contraseñas** con bcrypt y salt único
- ✅ **Sesiones seguras** con Flask sessions
- ✅ **Validación de datos** de entrada
- ✅ **Manejo de errores** sin exposición de información sensible
- ✅ **Prevención de SQL injection** con consultas parametrizadas

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'bcrypt'"
```bash
pip install bcrypt
```

### Error: "Database is locked"
- Cerrar todas las conexiones a la base de datos
- Reiniciar el servidor

### Error: "Port 5000 is already in use"
- Cambiar el puerto en `servidor.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### La página de tareas no muestra datos
- Verificar que hayas iniciado sesión primero con POST /login
- Las sesiones se mantienen durante la ejecución del servidor

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado PFO2 de la materia Programación sobre redes.

---

## 📱 Capturas de Pantalla en la carpeta screenshots

### Postman - Prueba a servidor
![Servidor](screenshots/01.%20servidor_ok.PNG)

### Postman - Registro de Usuario Exitoso
![Registro](screenshots/02.%20registro_exitoso.PNG)

### Postman - Registro de Usuario no Exitoso
![Registro](screenshots/03.%20registro_no_exitoso.PNG)

### Postman - Login Exitoso
![Login](screenshots/04.%20login_exitoso.PNG)

### Página de Bienvenida
![Bienvenida](screenshots/05.%20servidor_ok_localhost.PNG)

### Postman - Login no Exitoso
![Login](screenshots/06.%20login_no_exitoso.PNG)

### Postman - Login Falla por Datos Incompletos
![Login](screenshots/07.%20login_datos_incompletos.PNG)

### Postman - Login sin Datos
![Login](screenshots/08.%20login_sin_datos.PNG)

### Postman - Logout
![Logout](screenshots/09.%20logout.PNG)

---



## 🔐 ¿Por qué hashear contraseñas?

El hasheo de contraseñas es una práctica de seguridad fundamental por varias razones críticas:

### Protección contra acceso no autorizado
Si un atacante logra acceder a la base de datos, no podrá ver las contraseñas reales de los usuarios, solo los hashes irreversibles. Esto significa que incluso con acceso completo a los datos, las contraseñas permanecen protegidas.

### Cumplimiento de principios de seguridad
Ni siquiera los desarrolladores o administradores del sistema deben poder ver las contraseñas de los usuarios. El hasheo garantiza que nadie, incluido el personal técnico, tenga acceso a las credenciales reales.

### Mitigación de riesgos de reutilización
Muchos usuarios reutilizan contraseñas en múltiples servicios. Al hashear las contraseñas, se evita que una brecha de seguridad comprometa las cuentas de los usuarios en otros sitios web.

### Funciones hash criptográficas
Se utilizan algoritmos como bcrypt, scrypt o Argon2 que incluyen "salt" automático y son computacionalmente costosos, haciendo prácticamente imposible revertir el proceso o realizar ataques de fuerza bruta eficientes.


## 💾 Ventajas de usar SQLite en este proyecto

SQLite ofrece múltiples beneficios específicos para este tipo de proyecto:

### Simplicidad de implementación
No requiere instalación ni configuración de servidor de base de datos separado. El archivo de base de datos se crea automáticamente y se integra directamente con la aplicación Python, eliminando complejidades de configuración.

### Portabilidad completa
La base de datos es un único archivo que se puede mover, respaldar o compartir fácilmente. Esto facilita el desarrollo, las pruebas y el despliegue del proyecto.

### Rendimiento adecuado
Para aplicaciones de pequeña a mediana escala como este sistema de tareas, SQLite proporciona rendimiento más que suficiente, con soporte completo para transacciones ACID y consultas SQL estándar.

### Cero mantenimiento
No requiere administración de base de datos, actualizaciones de servidor, o gestión de usuarios y permisos a nivel de base de datos. Es ideal para proyectos educativos y prototipos.

### Compatibilidad nativa
Python incluye soporte nativo para SQLite a través del módulo sqlite3, eliminando la necesidad de dependencias externas adicionales para la funcionalidad básica de base de datos.

### Escalabilidad inicial
Aunque tiene limitaciones para aplicaciones de gran escala, SQLite puede manejar miles de usuarios y transacciones, siendo perfectamente adecuado para el alcance de este proyecto práctico.