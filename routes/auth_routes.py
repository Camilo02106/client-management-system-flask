from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import logging
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_service = AuthService()

@auth_bp.route('/login', methods=['GET', 'POST'])
def vista_login():
    """
    Login de Administrador
    ---
    parameters:
      - name: correo
        in: formData
        type: string
        required: true
        example: "admin@example.com"
      - name: clave
        in: formData
        type: string
        required: true
        example: "123456"
    responses:
      302:
        description: Redirección exitosa al dashboard
      400:
        description: Credenciales inválidas
    """
    if request.method == 'GET':
        return render_template("login.html")
    
    if request.method == 'POST':
        correo = request.form.get('correo', '').lower()
        clave = request.form.get('clave', '')

        if not correo or not clave:
            flash("Por favor complete todos los campos", "error")
            return redirect(url_for('auth.vista_login'))

        try:
            resultado = auth_service.autenticar(correo, clave)
            
            if resultado['success']:
                session['admin_id'] = resultado['id_admin']
                session['admin_correo'] = resultado['correo']
                session['admin_rol'] = resultado['rol']
                logging.info(f"Admin {correo} ha iniciado sesión")
                flash("Bienvenido al panel de administración", "success")
                return redirect(url_for('client.dashboard'))
            else:
                flash(resultado['mensaje'], "error")
                return redirect(url_for('auth.vista_login'))

        except Exception as e:
            logging.error(f"Error en login: {str(e)}")
            flash("Error interno del servidor", "error")
            return redirect(url_for('auth.vista_login'))


@auth_bp.route('/logout')
def logout():
    """
    Logout de Administrador
    ---
    responses:
      302:
        description: Sesión cerrada, redirige a login
    """
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('auth.vista_login'))
  
@auth_bp.route('/registro', methods=['GET','POST'])
def registro():

    # 🔐 SOLO SUPERADMIN PUEDE REGISTRAR ADMINS
    if session.get("admin_rol") != "superadmin":
        flash("No tienes permisos para registrar administradores", "error")
        return redirect(url_for("client.dashboard"))

    if request.method == 'GET':
        return render_template("registro_admin.html")

    try:

        datos = {
            "correo": request.form.get("correo").lower(),
            "clave": request.form.get("clave"),
            "nombre": request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "cargo": request.form.get("cargo"),
            "telefono": request.form.get("telefono"),
            "identificacion": request.form.get("identificacion")
        }

        if not all(datos.values()):
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("auth.registro"))

        resultado = auth_service.registrar_admin(datos)

        if resultado["success"]:
            flash("Registro exitoso, ahora puedes iniciar sesión", "success")
            return redirect(url_for("auth.vista_login"))

        flash(resultado["mensaje"], "error")
        return redirect(url_for("auth.registro"))

    except Exception as e:
        logging.error(f"Error en registro: {str(e)}")
        flash("Error interno del servidor", "error")
        return redirect(url_for("auth.registro"))