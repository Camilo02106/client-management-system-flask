# Sistema de Administración de Clientes y Facturación

Aplicación web desarrollada con **Python y Flask** que permite la gestión de clientes y administradores mediante un sistema de autenticación segura, control de roles y manejo de base de datos.

El sistema está diseñado con una **arquitectura modular**, separando rutas, lógica de negocio y vistas para facilitar el mantenimiento y escalabilidad.

---

# Características principales

* Autenticación de administradores mediante login seguro
* Contraseñas cifradas utilizando **bcrypt**
* Sistema de **roles (superadmin y admin)**
* Registro de nuevos administradores (solo superadmin)
* Gestión de clientes
* Edición de información de clientes
* Eliminación de clientes
* Panel administrativo (dashboard)
* Control de acceso a funcionalidades según permisos
* Manejo de sesiones de usuario
* Filtros de búsqueda de clientes
* Integración con base de datos **MySQL**

---

# Tecnologías utilizadas

* **Python**
* **Flask**
* **MySQL**
* **HTML**
* **CSS**
* **JavaScript**
* **bcrypt** (cifrado de contraseñas)

---

# Arquitectura del proyecto

El sistema está organizado siguiendo una arquitectura por capas: