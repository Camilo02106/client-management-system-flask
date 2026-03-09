import logging
import re
import subprocess
import os
from repositories.client_repository import ClientRepository

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class ClientService:
    """Lógica de creación y gestión de clientes"""
    
    def __init__(self):
        self.client_repo = ClientRepository()
    
    def obtener_clientes_filtrados(self, filtros: dict) -> dict:
        """
        Obtiene clientes con filtros aplicados
        
        Args:
            filtros: dict con los filtros (nombre, correo, plan, empresa, capacidad_usada)
            
        Returns:
            dict: {'success': bool, 'clientes': list, 'mensaje': str}
        """
        try:
            clientes = self.client_repo.obtener_con_filtros(filtros)
            
            return {
                'success': True,
                'clientes': clientes,
                'mensaje': 'Clientes obtenidos exitosamente'
            }
        except Exception as e:
            logging.error(f"Error obteniendo clientes: {str(e)}")
            return {
                'success': False,
                'clientes': [],
                'mensaje': 'Error al obtener clientes'
            }
    
    def obtener_cliente_por_id(self, cliente_id: int) -> dict:
        """
        Obtiene un cliente específico
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            dict: {'success': bool, 'cliente': dict, 'mensaje': str}
        """
        try:
            cliente = self.client_repo.obtener_por_id(cliente_id)
            
            if not cliente:
                return {
                    'success': False,
                    'cliente': None,
                    'mensaje': 'Cliente no encontrado'
                }
            
            return {
                'success': True,
                'cliente': cliente,
                'mensaje': 'Cliente obtenido exitosamente'
            }
        except Exception as e:
            logging.error(f"Error obteniendo cliente: {str(e)}")
            return {
                'success': False,
                'cliente': None,
                'mensaje': 'Error al obtener cliente'
            }
    
    def actualizar_cliente(self, cliente_id: int, datos: dict) -> dict:
        """
        Actualiza un cliente
        
        Args:
            cliente_id: ID del cliente
            datos: dict con los datos a actualizar
            
        Returns:
            dict: {'success': bool, 'mensaje': str}
        """
        try:
            success = self.client_repo.actualizar(cliente_id, datos)
            
            if success:
                logging.info(f"Cliente {cliente_id} actualizado")
                return {
                    'success': True,
                    'mensaje': 'Cliente actualizado exitosamente'
                }
            else:
                return {
                    'success': False,
                    'mensaje': 'Error al actualizar cliente'
                }
        except Exception as e:
            logging.error(f"Error actualizando cliente: {str(e)}")
            return {
                'success': False,
                'mensaje': 'Error interno del servidor'
            }
    
    def eliminar_cliente(self, cliente_id: int) -> dict:
        """
        Elimina un cliente
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            dict: {'success': bool, 'mensaje': str}
        """
        try:
            success = self.client_repo.eliminar(cliente_id)
            
            if success:
                logging.info(f"Cliente {cliente_id} eliminado")
                return {
                    'success': True,
                    'mensaje': 'Cliente eliminado exitosamente'
                }
            else:
                return {
                    'success': False,
                    'mensaje': 'Error al eliminar cliente'
                }
        except Exception as e:
            logging.error(f"Error eliminando cliente: {str(e)}")
            return {
                'success': False,
                'mensaje': 'Error interno del servidor'
            }
    
    def crear_cliente(self, datos: dict) -> dict:
        """
        Crea un nuevo cliente con su base de datos
        
        Args:
            datos: dict con los datos del cliente
            
        Returns:
            dict: {'success': bool, 'mensaje': str}
        """
        # Validaciones
        validacion = self._validar_datos(datos)
        if not validacion['valido']:
            return {
                'success': False,
                'mensaje': validacion['error']
            }
        
        try:
            # Verificar si el cliente ya existe
            if self.client_repo.existe_cliente(datos['correo']):
                return {
                    'success': False,
                    'mensaje': 'Este correo ya está registrado'
                }
            
            # Crear base de datos
            contador = self.client_repo.obtener_siguiente_contador()
            nombre_bd = self._construir_nombre_bd(
                datos['correo'],
                datos['empresa'],
                contador
            )
            
            self.client_repo.crear_base_datos(nombre_bd)
            
            # Insertar registro del cliente
            contacto = f"{datos['primer_nombre']} {datos['segundo_nombre']}"
            self.client_repo.insertar_cliente({
                'correo': datos['correo'],
                'empresa': datos['empresa'],
                'contacto': contacto,
                'pais': datos['pais'],
                'contrasena': datos['contrasena'],
                'nombre_bd': nombre_bd,
                'plan': 'BASICO'
            })
            
            # Ejecutar script de creación de tablas
            subprocess.run([
                "python", "crear_tablas.py",
                nombre_bd, datos['correo'], datos['pais'],
                datos['empresa'], contacto, datos['contrasena'],
                os.getenv("DB_PORT", "3306")
            ], check=True)
            
            logging.info(f"Cliente creado exitosamente: {nombre_bd}")
            
            return {
                'success': True,
                'mensaje': 'Base de datos creada exitosamente'
            }
        
        except Exception as e:
            logging.error(f"Error al crear cliente: {str(e)}")
            return {
                'success': False,
                'mensaje': 'Error interno del servidor'
            }
    
    def _validar_datos(self, datos: dict) -> dict:
        """Valida los datos ingresados"""
        campos_requeridos = [
            'primer_nombre', 'segundo_nombre', 'correo',
            'pais', 'empresa', 'contrasena'
        ]
        
        if not all(datos.get(campo) for campo in campos_requeridos):
            return {
                'valido': False,
                'error': 'Por favor complete todos los campos obligatorios'
            }
        
        if not re.match(EMAIL_REGEX, datos['correo']):
            return {
                'valido': False,
                'error': 'Por favor ingrese un correo válido'
            }
        
        return {'valido': True}
    
    def _construir_nombre_bd(self, correo: str, empresa: str, contador: int) -> str:
        """Construye el nombre de la base de datos"""
        dominio = self._extraer_dominio(correo)
        empresa_limpia = self._limpiar_texto(empresa)
        return f"bd_{contador:03d}_{dominio}_{empresa_limpia}"
    
    def _extraer_dominio(self, correo: str) -> str:
        """Extrae el dominio del correo"""
        match = re.search(r'@([^.]+)\.', correo)
        return self._limpiar_texto(match.group(1)) if match else 'default'
    
    def _limpiar_texto(self, texto: str) -> str:
        """Limpia el texto para usar en nombres de BD"""
        texto = texto.replace(" ", "")
        texto = re.sub(r'[^a-zA-Z0-9_]', '', texto)
        return texto.lower()