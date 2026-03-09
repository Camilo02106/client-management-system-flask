import pymysql
import pymysql.cursors
import os
import re
import logging

class ClientRepository:
    """Acceso a datos de clientes en info_clientes"""
    
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database_clientes = 'info_clientes'
    
    def _conectar(self, database=None):
        """Crea una conexión a la BD"""
        db = database or self.database_clientes
        try:
            conexion = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=db,
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conexion
        except pymysql.Error as e:
            logging.error(f"Error de conexión a BD: {str(e)}")
            raise
    
    def obtener_con_filtros(self, filtros: dict) -> list:
        """Obtiene clientes con filtros aplicados"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            # Construir query dinámicamente
            query = "SELECT * FROM info WHERE 1=1"
            parametros = []
            
            if filtros.get('nombre'):
                query += " AND contacto LIKE %s"
                parametros.append(f"%{filtros['nombre']}%")
            
            if filtros.get('correo'):
                query += " AND correo LIKE %s"
                parametros.append(f"%{filtros['correo']}%")
            
            if filtros.get('plan'):
                query += " AND plan = %s"
                parametros.append(filtros['plan'])
            
            if filtros.get('empresa'):
                query += " AND empresa LIKE %s"
                parametros.append(f"%{filtros['empresa']}%")
            
            if filtros.get('capacidad_usada'):
                query += " AND capacidad_usada = %s"
                parametros.append(filtros['capacidad_usada'])
            
            cursor.execute(query, parametros)
            resultado = cursor.fetchall()
            return resultado if resultado else []
        
        except pymysql.Error as e:
            logging.error(f"Error obteniendo clientes: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def obtener_por_id(self, cliente_id: int) -> dict:
        """Obtiene un cliente por ID"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute("SELECT * FROM info WHERE id=%s", (cliente_id,))
            resultado = cursor.fetchone()
            return resultado if resultado else None
        
        except pymysql.Error as e:
            logging.error(f"Error obteniendo cliente: {str(e)}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def actualizar(self, cliente_id: int, datos: dict) -> bool:
        """Actualiza un cliente"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            # Construir UPDATE dinámicamente - SOLO CON VALORES NO NULOS
            campos = []
            valores = []
            
            if datos.get('contacto'):
                campos.append("`contacto`=%s")
                valores.append(datos['contacto'])
            
            if datos.get('empresa'):
                campos.append("`empresa`=%s")
                valores.append(datos['empresa'])
            
            if datos.get('pais'):
                campos.append("`pais`=%s")
                valores.append(datos['pais'])
            
            if datos.get('plan'):
                campos.append("`plan`=%s")
                valores.append(datos['plan'])
            
            # ✅ VALIDAR capacidad_usada - Solo si es un número válido
            if datos.get('capacidad_usada'):
                try:
                    capacidad = int(datos['capacidad_usada'])
                    campos.append("`capacidad_usada`=%s")
                    valores.append(capacidad)
                except (ValueError, TypeError):
                    logging.warning(f"capacidad_usada inválida: {datos['capacidad_usada']}")
                    # Si no es válido, no lo actualiza
            
            # Si no hay campos a actualizar, retorna False
            if not campos:
                logging.warning(f"No hay campos para actualizar en cliente {cliente_id}")
                return False
            
            # Agregar el ID al final
            valores.append(cliente_id)
            
            # Construir query
            query = f"UPDATE `info` SET {', '.join(campos)} WHERE `id`=%s"
            
            logging.info(f"Ejecutando query: {query} con valores: {valores}")
            
            cursor.execute(query, valores)
            
            # Verificar si realmente se actualizó
            if cursor.rowcount == 0:
                logging.warning(f"No se actualizó el cliente {cliente_id}")
                return False
            
            logging.info(f"Cliente {cliente_id} actualizado correctamente")
            return True
        
        except pymysql.Error as e:
            logging.error(f"Error actualizando cliente: {str(e)}")
            logging.error(f"Query problemática: UPDATE info SET ... WHERE id={cliente_id}")
            return False
        except Exception as e:
            logging.error(f"Error inesperado actualizando cliente: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    
    def eliminar(self, cliente_id: int) -> bool:
        """Elimina un cliente"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute("DELETE FROM info WHERE id=%s", (cliente_id,))
            
            logging.info(f"Cliente {cliente_id} eliminado")
            return True
        
        except pymysql.Error as e:
            logging.error(f"Error eliminando cliente: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def existe_cliente(self, correo: str) -> bool:
        """Verifica si el cliente ya existe"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute("SELECT 1 FROM info WHERE correo=%s", (correo,))
            resultado = cursor.fetchone()
            return resultado is not None
        except pymysql.Error as e:
            logging.error(f"Error verificando cliente: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def obtener_siguiente_contador(self) -> int:
        """Obtiene el siguiente número de contador para BD"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute("SHOW DATABASES LIKE 'bd_%'")
            bases = cursor.fetchall()
            
            contador_max = 0
            for bd in bases:
                nombre = bd[0] if isinstance(bd, tuple) else bd.get(list(bd.keys())[0])
                match = re.match(r'bd_(\d+)_', nombre)
                if match:
                    num = int(match.group(1))
                    if num > contador_max:
                        contador_max = num
            
            return contador_max + 1
        except pymysql.Error as e:
            logging.error(f"Error obteniendo contador: {str(e)}")
            return 1
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def crear_base_datos(self, nombre_bd: str) -> bool:
        """Crea una nueva base de datos"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute(f"""
                CREATE DATABASE `{nombre_bd}`
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci;
            """)
            logging.info(f"Base de datos creada: {nombre_bd}")
            return True
        except pymysql.Error as e:
            logging.error(f"Error creando BD: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    
    def insertar_cliente(self, datos: dict) -> bool:
        """Inserta un nuevo cliente"""
        conexion = None
        cursor = None
        try:
            conexion = self._conectar()
            cursor = conexion.cursor()
            
            cursor.execute("""
                INSERT INTO info 
                (correo, empresa, contacto, pais, contrasena, nombre_bd, plan) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                datos.get('correo'),
                datos.get('empresa'),
                datos.get('contacto'),
                datos.get('pais'),
                datos.get('contrasena'),
                datos.get('nombre_bd'),
                datos.get('plan')
            ))
            logging.info(f"Cliente insertado: {datos.get('correo')}")
            return True
        except pymysql.Error as e:
            logging.error(f"Error insertando cliente: {str(e)}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()