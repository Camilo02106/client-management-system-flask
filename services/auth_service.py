from repositories.auth_repository import AuthRepository
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:

    def __init__(self):
        self.repo = AuthRepository()


    def autenticar(self, correo, clave):

        admin = self.repo.obtener_por_correo(correo)

        if not admin:
            return {"success": False, "mensaje": "Usuario no existe"}

        id_admin, correo_db, clave_hash, rol = admin

        if not check_password_hash(clave_hash, clave):
            return {"success": False, "mensaje": "Contraseña incorrecta"}

        return {
            "success": True,
            "id_admin": id_admin,
            "correo": correo_db,
            "rol": rol
        }


    def registrar_admin(self, datos):

        existe = self.repo.obtener_por_correo(datos["correo"])

        if existe:
            return {
                "success": False,
                "mensaje": "El correo ya está registrado"
            }

        datos["clave"] = generate_password_hash(datos["clave"])

        creado = self.repo.crear_admin(datos)

        if creado:
            return {"success": True}

        return {
            "success": False,
            "mensaje": "Error al registrar"
        }