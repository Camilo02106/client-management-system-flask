import pymysql
import os
import pymysql
import os
import logging

class AuthRepository:

    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = int(os.getenv("DB_PORT", 3306))
        self.database = "admin_app"

    def _conectar(self):
        try:
            return pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
                autocommit=True
            )
        except pymysql.Error as e:
            logging.error(f"Error conexión BD: {e}")
            raise

    def obtener_por_correo(self, correo):

        conexion = None
        cursor = None

        try:
            conexion = self._conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "SELECT idAdmin, correo, clave, rol FROM admin_users WHERE correo=%s",
                (correo,)
            )

            return cursor.fetchone()

        except pymysql.Error as e:
            logging.error(f"Error obteniendo admin: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()


    def crear_admin(self, datos):

        conexion = None
        cursor = None

        try:
            conexion = self._conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO admin_users
                (correo, clave, nombre, apellido, cargo, telefono, identificacion)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                datos["correo"],
                datos["clave"],
                datos["nombre"],
                datos["apellido"],
                datos["cargo"],
                datos["telefono"],
                datos["identificacion"]
            ))

            return True

        except pymysql.Error as e:
            logging.error(f"Error creando admin: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()