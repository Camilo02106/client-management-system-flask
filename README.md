# Flask Admin Client Management System

Aplicación web desarrollada con **Python y Flask** para la gestión de clientes y administradores mediante autenticación segura, control de roles y manejo de base de datos con MySQL.

El sistema permite administrar clientes desde un panel administrativo, registrar nuevos administradores y aplicar restricciones de acceso según permisos.
La arquitectura del proyecto separa **rutas, lógica de negocio y vistas**, facilitando el mantenimiento y escalabilidad del sistema.

---

# Características principales

* Autenticación de administradores mediante login seguro
* Contraseñas cifradas utilizando **bcrypt**
* Sistema de **roles (superadmin y admin)**
* Registro de nuevos administradores (solo superadmin)
* Panel administrativo (dashboard)
* Gestión de clientes
* Edición de información de clientes
* Eliminación de clientes
* Filtros de búsqueda de clientes
* Manejo de sesiones con Flask
* Integración con base de datos **MySQL**

---

# Tecnologías utilizadas

* Python
* Flask
* MySQL
* HTML
* CSS
* JavaScript
* bcrypt (cifrado de contraseñas)

---

# Arquitectura del proyecto

El sistema sigue una **arquitectura modular por capas**, separando responsabilidades entre rutas, servicios y vistas.

```
project/
│
├── app.py
│
├── routes/
│   ├── auth_routes.py
│   └── client_routes.py
│
├── services/
│   ├── auth_service.py
│   └── client_service.py
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── editar_cliente.html
│   └── registro_admin.html
│
├── static/
│   ├── css/
│   └── js/
│
└── README.md
```

### Descripción de carpetas

**routes**
Contiene las rutas del sistema que gestionan las peticiones HTTP.

**services**
Contiene la lógica de negocio y las operaciones sobre la base de datos.

**templates**
Contiene las vistas HTML del sistema.

**static**
Contiene archivos estáticos como hojas de estilo y scripts.

---

# Instalación

### 1. Clonar el repositorio

```
git clone https://github.com/usuario/flask-admin-client-management.git
```

### 2. Entrar al directorio del proyecto

```
cd flask-admin-client-management
```

### 3. Crear entorno virtual

```
python -m venv venv
```

### 4. Activar entorno virtual

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

### 5. Instalar dependencias

```
pip install -r requirements.txt
```

---

# Configuración de la base de datos

Crear la base de datos en MySQL:

```
CREATE DATABASE ianalitics;
```

Luego configurar las credenciales de conexión en el archivo de configuración del proyecto.

---

# Ejecutar la aplicación

```
python app.py
```

Abrir el navegador en:

```
http://127.0.0.1:5000
```

---

# Seguridad implementada

## Cifrado de contraseñas

Las contraseñas de los administradores se almacenan utilizando **bcrypt**, lo que evita guardar credenciales en texto plano.

Ejemplo de hash generado:

```
$2b$12$Ngy3A9QxJqe4R9kAbMv0xeoZ1iTSGztxuh2.SHGxKkE6N8GNqZIfa
```

Esto proporciona:

* Hash seguro de contraseñas
* Uso de **salt automático**
* Protección contra ataques de fuerza bruta

---

## Control de acceso basado en roles

El sistema implementa **RBAC (Role Based Access Control)**.

Roles disponibles:

| Rol        | Permisos                                                      |
| ---------- | ------------------------------------------------------------- |
| Superadmin | Registrar administradores, editar clientes, eliminar clientes |
| Admin      | Acceso al dashboard y consulta de información                 |

Las rutas críticas validan el rol del usuario almacenado en sesión antes de permitir la operación.

---

# Gestión de clientes

El sistema permite:

* Visualizar clientes registrados
* Editar información de clientes
* Eliminar clientes
* Filtrar clientes por diferentes criterios

Algunos campos críticos como **ID, correo y base de datos asignada** no son editables para preservar la integridad de los datos.

---

# Manejo de sesiones

El sistema utiliza **sesiones de Flask** para mantener autenticados a los administradores.

Variables de sesión utilizadas:

```
admin_id
admin_correo
admin_rol
```

---

# Posibles mejoras futuras

* Implementación de expiración automática de sesiones
* API REST para integración con otros sistemas
* Auditoría de acciones administrativas
* Implementación de autenticación con JWT
* Panel de reportes y estadísticas

---

# Autor

Proyecto desarrollado por

**Camilo Ortiz**
Ingeniero de Sistemas y Computación

---

# Licencia

Este proyecto fue desarrollado con fines **académicos y de aprendizaje**.
