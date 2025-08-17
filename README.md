# App de registro de usuarios

Aplicación web sencilla hecha con **Python y Flask** que permite registrar usuarios (nombre, correo y contraseña), almacenar los datos en una **base de datos SQLite**, y listar los usuarios registrados. Incluye validación de correo, mensajes de error/éxito, hash de contraseñas y una interfaz sencilla.

---

##  Funcionalidades

- Registro de usuarios con:
  - Nombre
  - Correo electrónico (validado con expresión regular)
  - Contraseña (almacenada de forma segura con hashing)
- Validación:
  - Todos los campos son obligatorios
  - Validación de formato de correo
  - Verificación de correos duplicados
- Mensajes flash para errores y confirmaciones
- Listado de usuarios registrados
- Logging de registros en archivo

---

##  Arquitectura de la Aplicación

La aplicación sigue una estructura típica de Flask:

├── app.py # Archivo principal de la aplicación Flask
├── instance/
│ └── usuarios.db # Base de datos SQLite
├── static/
│ ├── css/
│ │ ├── style.css # CSS para registro
│ │ └── usuarios.css # CSS para listado de usuarios
│ └── images/
│ └── NOKOTAN.png # Logo de la app
├── templates/
│ ├── registro.html # Formulario de registro
│ └── usuarios.html # Listado de usuarios
└── usuarios.log # Log de eventos (registro de usuarios)
