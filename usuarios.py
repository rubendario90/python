# Gestión de usuarios para el sistema de aprobaciones

class Usuario:
    """Clase para representar un usuario del sistema"""
    
    def __init__(self, id_usuario, nombre, email, rol, departamento=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.rol = rol  # 'solicitante', 'aprobador_inicial', 'aprobador_final', 'admin'
        self.departamento = departamento
        self.activo = True
    
    def __str__(self):
        return f"{self.nombre} ({self.email}) - {self.rol}"
    
    def to_dict(self):
        """Convierte el usuario a diccionario"""
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'departamento': self.departamento,
            'activo': self.activo
        }

class GestorUsuarios:
    """Gestor para manejar usuarios del sistema"""
    
    def __init__(self):
        self.usuarios = {}
        self._inicializar_usuarios_ejemplo()
    
    def _inicializar_usuarios_ejemplo(self):
        """Inicializa algunos usuarios de ejemplo"""
        usuarios_ejemplo = [
            Usuario(1, "Juan Pérez", "juan.perez@empresa.com", "aprobador_inicial", "Finanzas"),
            Usuario(2, "María García", "maria.garcia@empresa.com", "aprobador_final", "Gerencia"),
            Usuario(3, "Carlos López", "carlos.lopez@empresa.com", "solicitante", "Compras"),
            Usuario(4, "Ana Rodríguez", "ana.rodriguez@empresa.com", "solicitante", "RRHH"),
            Usuario(5, "Luis Martínez", "luis.martinez@empresa.com", "admin", "IT")
        ]
        
        for usuario in usuarios_ejemplo:
            self.usuarios[usuario.id_usuario] = usuario
    
    def agregar_usuario(self, usuario):
        """Agrega un usuario al sistema"""
        if not isinstance(usuario, Usuario):
            raise ValueError("Debe proporcionar una instancia de Usuario")
        
        self.usuarios[usuario.id_usuario] = usuario
        return True
    
    def obtener_usuario(self, id_usuario):
        """Obtiene un usuario por su ID"""
        return self.usuarios.get(id_usuario)
    
    def obtener_usuario_por_email(self, email):
        """Obtiene un usuario por su email"""
        for usuario in self.usuarios.values():
            if usuario.email == email:
                return usuario
        return None
    
    def obtener_usuarios_por_rol(self, rol):
        """Obtiene todos los usuarios con un rol específico"""
        return [usuario for usuario in self.usuarios.values() if usuario.rol == rol and usuario.activo]
    
    def obtener_aprobadores_iniciales(self):
        """Obtiene todos los aprobadores iniciales activos"""
        return self.obtener_usuarios_por_rol("aprobador_inicial")
    
    def obtener_aprobadores_finales(self):
        """Obtiene todos los aprobadores finales activos"""
        return self.obtener_usuarios_por_rol("aprobador_final")
    
    def listar_usuarios(self):
        """Lista todos los usuarios activos"""
        return [usuario for usuario in self.usuarios.values() if usuario.activo]
    
    def formatear_lista_usuarios(self, usuarios):
        """Formatea una lista de usuarios para incluir en emails"""
        if not usuarios:
            return "No hay usuarios asignados"
        
        lista = []
        for usuario in usuarios:
            lista.append(f"• {usuario.nombre} ({usuario.email}) - {usuario.rol.replace('_', ' ').title()}")
        
        return "\n".join(lista)
    
    def desactivar_usuario(self, id_usuario):
        """Desactiva un usuario"""
        usuario = self.obtener_usuario(id_usuario)
        if usuario:
            usuario.activo = False
            return True
        return False
    
    def activar_usuario(self, id_usuario):
        """Activa un usuario"""
        usuario = self.obtener_usuario(id_usuario)
        if usuario:
            usuario.activo = True
            return True
        return False

# Instancia global del gestor de usuarios
gestor_usuarios = GestorUsuarios()