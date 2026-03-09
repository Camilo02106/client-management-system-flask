from flask import Flask, session, redirect, url_for, flash
from flasgger import Flasgger
from dotenv import load_dotenv
import logging
import os
from functools import wraps

# Importar blueprints
from routes.auth_routes import auth_bp
from routes.client_routes import client_bp

load_dotenv()

# Configuración
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_super_secreta_temporal")

# ✅ SWAGGER
swagger = Flasgger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Gestión de Clientes",
        "description": "API para gestionar clientes y autenticación",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"]
})

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Decorador para proteger rutas
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Por favor inicia sesión primero", "error")
            return redirect(url_for('auth.vista_login'))
        return f(*args, **kwargs)
    return decorador

# Registrar blueprints modulos
app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)

@app.route('/')
def index():
    """Ruta raíz - redirige según estado de sesión"""
    if 'admin_id' in session:
        return redirect(url_for('client.dashboard'))
    return redirect(url_for('auth.vista_login'))

@app.route('/health')
def health():
    from datetime import datetime
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }, 200

if __name__ == "__main__":
    app.run(debug=True)