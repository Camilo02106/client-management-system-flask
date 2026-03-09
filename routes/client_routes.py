from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import logging
from functools import wraps
from services.client_service import ClientService

client_bp = Blueprint('client', __name__, url_prefix='/clientes')
client_service = ClientService()

def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Por favor inicia sesión primero", "error")
            return redirect(url_for('auth.vista_login'))
        return f(*args, **kwargs)
    return decorador

@client_bp.route('/dashboard')
@login_requerido
def dashboard():
    """
    Dashboard de Clientes
    ---
    parameters:
      - name: nombre
        in: query
        type: string
        required: false
      - name: correo
        in: query
        type: string
        required: false
      - name: plan
        in: query
        type: string
        required: false
      - name: empresa
        in: query
        type: string
        required: false
      - name: capacidad_usada
        in: query
        type: string
        required: false
    responses:
      200:
        description: Dashboard cargado exitosamente
    """
    try:
        filtro_nombre = request.args.get('nombre', '')
        filtro_correo = request.args.get('correo', '')
        filtro_plan = request.args.get('plan', '')
        filtro_empresa = request.args.get('empresa', '')
        filtro_capacidad_usada = request.args.get('capacidad_usada', '')
        
        resultado = client_service.obtener_clientes_filtrados({
            'nombre': filtro_nombre,
            'correo': filtro_correo,
            'plan': filtro_plan,
            'empresa': filtro_empresa,
            'capacidad_usada': filtro_capacidad_usada
        })
        
        if resultado['success']:
            clientes = resultado['clientes']
        else:
            clientes = []
            flash(resultado['mensaje'], 'error')
        
        return render_template('dashboard.html', 
                             clientes=clientes,
                             filtro_nombre=filtro_nombre,
                             filtro_correo=filtro_correo,
                             filtro_plan=filtro_plan,
                             filtro_empresa=filtro_empresa,
                             filtro_capacidad=filtro_capacidad_usada)
    
    except Exception as e:
        logging.error(f"Error en dashboard: {str(e)}")
        flash("Error al cargar el dashboard", "error")
        return redirect(url_for('auth.vista_login'))

@client_bp.route('/editar/<int:cliente_id>', methods=['GET', 'POST'])
@login_requerido
def editar_cliente(cliente_id):
  
  if session.get("admin_rol") != "superadmin":
    flash("No tienes permisos para editar clientes", "error")
    return redirect(url_for("client.dashboard"))
  
  try:
    
        if request.method == 'GET':
            resultado = client_service.obtener_cliente_por_id(cliente_id)
            
            if not resultado['success']:
                flash("Cliente no encontrado", "error")
                return redirect(url_for('client.dashboard'))
            
            cliente = resultado['cliente']
            return render_template('editar_cliente.html', cliente=cliente)
        
        else:
            datos = {
                'contacto': request.form.get('contacto'),
                'empresa': request.form.get('empresa'),
                'pais': request.form.get('pais'),
                'plan': request.form.get('plan'),
                'capacidad_usada': request.form.get('capacidad_usada')
            }
            
            resultado = client_service.actualizar_cliente(cliente_id, datos)
            
            if resultado['success']:
                flash("Cliente actualizado exitosamente", "success")
            else:
                flash(resultado['mensaje'], "error")
            
            return redirect(url_for('client.dashboard'))
    
  except Exception as e:
      logging.error(f"Error editando cliente: {str(e)}")
      flash("Error al editar cliente", "error")
      return redirect(url_for('client.dashboard'))

@client_bp.route('/eliminar/<int:cliente_id>', methods=['POST'])
@login_requerido
def eliminar_cliente(cliente_id):
        
    if session.get("admin_rol") != "superadmin":
        flash("No tienes permisos para eliminar clientes", "error")
        return redirect(url_for("client.dashboard"))
    
    try:
        resultado = client_service.eliminar_cliente(cliente_id)
        
        if resultado['success']:
            flash("Cliente eliminado exitosamente", "success")
        else:
            flash(resultado['mensaje'], "error")
        
        return redirect(url_for('client.dashboard'))
    
    except Exception as e:
        logging.error(f"Error eliminando cliente: {str(e)}")
        flash("Error al eliminar cliente", "error")
        return redirect(url_for('client.dashboard'))