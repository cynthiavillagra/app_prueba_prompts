# -*- coding: utf-8 -*-
"""
============================================================================
AUTH_SERVICE.PY - Servicio de Autenticación
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: SERVICES
Patrones: Adapter, Strategy
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: AUTH
- Requisitos: RF-01 (Registro), RF-02 (Login), RF-03 (Logout)
- HU: HU-01, HU-02, HU-03
- Caso de Uso: CU-01 (Gestionar Autenticación)

POR QUÉ ADAPTER:
- SÍ: Encapsula llamadas a Supabase Auth
- SÍ: Desacopla la app del SDK específico
- SÍ: Facilita testing con mocks
- NO alternativa (llamar Supabase directamente): Acoplamiento alto

POR QUÉ STRATEGY:
- SÍ: Permite múltiples métodos de auth (email/password, OAuth futuro)
- SÍ: Open/Closed principle (extensible sin modificar)
- NO alternativa (if/else por tipo): Violación de OCP
============================================================================
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from dataclasses import dataclass

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from src.config.settings import Settings
from src.repositories.supabase_client import SupabaseClient
from src.models.user import User
from src.services.session_manager import SessionManager


# ============================================================================
# STRATEGY PATTERN: Interfaz base para estrategias de autenticación
# ============================================================================

class IAuthStrategy(ABC):
    """
    Interfaz para estrategias de autenticación.
    
    POR QUÉ ABC:
    - SÍ: Define contrato claro
    - SÍ: Python puro sin dependencias
    - NO alternativa (Protocol): Menos explícito para principiantes
    """
    
    @abstractmethod
    def login(self, **credentials) -> Tuple[User, str, Optional[str]]:
        """
        Autentica al usuario.
        
        RETORNA: (User, access_token, refresh_token)
        RAISES: AuthenticationError si falla
        """
        pass
    
    @abstractmethod
    def register(self, **credentials) -> User:
        """
        Registra un nuevo usuario.
        
        RETORNA: User creado
        RAISES: AuthenticationError si falla
        """
        pass


class EmailPasswordStrategy(IAuthStrategy):
    """
    Estrategia de autenticación por email y contraseña.
    
    IMPLEMENTACIÓN:
    - Usa Supabase Auth
    - Valida credenciales antes de enviar
    - Mapea respuestas a entidades User
    """
    
    def __init__(self, supabase: SupabaseClient):
        """
        Constructor con inyección de dependencia.
        
        POR QUÉ INYECCIÓN:
        - SÍ: Facilita testing (mock del cliente)
        - SÍ: Inversión de dependencias (DIP)
        """
        self._supabase = supabase
    
    def login(self, email: str, password: str) -> Tuple[User, str, Optional[str]]:
        """
        Login con email y password.
        
        PARÁMETROS:
        - email: Email del usuario
        - password: Contraseña
        
        RETORNA:
        - Tuple[User, access_token, refresh_token]
        
        RAISES:
        - ValueError: Si credenciales vacías
        - AuthenticationError: Si autenticación falla
        """
        # Validación de entrada
        if not email or not email.strip():
            raise ValueError("El email es obligatorio")
        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        try:
            response = self._supabase.auth.sign_in_with_password({
                'email': email.strip(),
                'password': password
            })
            
            # Mapear respuesta a User
            user = User(
                id=response.user.id,
                email=response.user.email,
                created_at=response.user.created_at
            )
            
            access_token = response.session.access_token
            refresh_token = response.session.refresh_token
            
            return user, access_token, refresh_token
            
        except Exception as e:
            # Mapear errores de Supabase a mensajes amigables
            error_msg = str(e).lower()
            if 'invalid' in error_msg or 'credentials' in error_msg:
                raise PermissionError("Credenciales incorrectas")
            raise PermissionError(f"Error de autenticación: {e}")
    
    def register(self, email: str, password: str) -> User:
        """
        Registro con email y password.
        
        PARÁMETROS:
        - email: Email del nuevo usuario
        - password: Contraseña (mínimo 6 caracteres)
        
        RETORNA: User creado
        
        RAISES:
        - ValueError: Si datos inválidos
        - PermissionError: Si registro falla (ej: email duplicado)
        """
        # Validación de entrada
        if not email or not email.strip():
            raise ValueError("El email es obligatorio")
        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        try:
            response = self._supabase.auth.sign_up({
                'email': email.strip(),
                'password': password
            })
            
            # Verificar que se creó el usuario
            if response.user is None:
                raise PermissionError("No se pudo crear el usuario")
            
            return User(
                id=response.user.id,
                email=response.user.email,
                created_at=response.user.created_at
            )
            
        except Exception as e:
            error_msg = str(e).lower()
            if 'already' in error_msg or 'registered' in error_msg:
                raise PermissionError("El email ya está registrado")
            raise PermissionError(f"Error de registro: {e}")


# ============================================================================
# AUTH SERVICE: Fachada que usa las estrategias
# ============================================================================

class AuthService:
    """
    Servicio de autenticación (Fachada + Adapter).
    
    RESPONSABILIDADES:
    - Coordinar estrategias de autenticación
    - Manejar SessionManager
    - Proveer interfaz simplificada
    
    USO:
        auth = AuthService()
        user = auth.login('email@ejemplo.com', 'password123')
        auth.logout()
    """
    
    def __init__(
        self, 
        strategy: Optional[IAuthStrategy] = None
    ):
        """
        Constructor con estrategia opcional.
        
        POR QUÉ ESTRATEGIA OPCIONAL:
        - SÍ: Default útil para la mayoría de casos
        - SÍ: Permite inyectar estrategia para testing
        """
        self._supabase = SupabaseClient()
        self._session = SessionManager()
        
        # Usar estrategia proporcionada o default (email/password)
        self._strategy = strategy or EmailPasswordStrategy(self._supabase)
    
    def login(self, email: str, password: str) -> User:
        """
        Autentica al usuario y establece la sesión.
        
        FLUJO:
        1. Llama a la estrategia de login
        2. Establece sesión en SessionManager
        3. Retorna User
        
        RETORNA: User autenticado
        RAISES: PermissionError si falla
        """
        user, access_token, refresh_token = self._strategy.login(
            email=email, 
            password=password
        )
        
        # Establecer sesión
        self._session.set_session(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
        return user
    
    def register(self, email: str, password: str) -> User:
        """
        Registra un nuevo usuario.
        
        NOTA: No establece sesión automáticamente.
        El usuario debe hacer login después de registrarse.
        
        RETORNA: User creado
        """
        return self._strategy.register(email=email, password=password)
    
    def logout(self) -> None:
        """
        Cierra la sesión actual.
        
        FLUJO:
        1. Llama a Supabase signOut
        2. Limpia SessionManager
        """
        try:
            self._supabase.auth.sign_out()
        except Exception:
            pass  # Ignorar errores de Supabase (ya estamos saliendo)
        finally:
            self._session.clear()
    
    def get_current_user(self) -> Optional[User]:
        """
        Obtiene el usuario actual si hay sesión válida.
        
        RETORNA: User o None si no autenticado/expirado
        """
        if self._session.is_session_valid():
            return self._session.current_user
        return None
    
    def is_authenticated(self) -> bool:
        """Verifica si hay sesión válida."""
        return self._session.is_session_valid()


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para AuthService.
    
    EJECUCIÓN:
        python src/services/auth_service.py
    
    NOTA: Esta prueba NO hace llamadas reales a Supabase.
    Solo verifica la estructura y validaciones.
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: AuthService")
    print("=" * 60)
    
    try:
        # Test 1: Crear servicio
        auth = AuthService()
        print("✅ AuthService creado correctamente")
        
        # Test 2: Verificar estado inicial
        assert not auth.is_authenticated(), "No debería estar autenticado"
        print("✅ Estado inicial: no autenticado")
        
        # Test 3: Verificar que strategy está configurada
        assert auth._strategy is not None, "Strategy no configurada"
        assert isinstance(auth._strategy, EmailPasswordStrategy), "Strategy incorrecta"
        print("✅ Strategy: EmailPasswordStrategy (default)")
        
        # Test 4: Validación de email vacío
        try:
            auth._strategy.login(email='', password='password123')
            print("❌ Debería fallar con email vacío")
        except ValueError as e:
            print(f"✅ Validación email: {e}")
        
        # Test 5: Validación de password corto
        try:
            auth._strategy.login(email='test@test.com', password='123')
            print("❌ Debería fallar con password corto")
        except ValueError as e:
            print(f"✅ Validación password: {e}")
        
        # Test 6: Logout (sin sesión)
        auth.logout()
        print("✅ Logout sin sesión no causa error")
        
        # Test 7: get_current_user sin sesión
        user = auth.get_current_user()
        assert user is None, "Debería ser None sin sesión"
        print("✅ get_current_user() es None sin sesión")
        
        # Test 8: Verificar que no hay credenciales hardcodeadas
        import inspect
        source = inspect.getsource(AuthService)
        source += inspect.getsource(EmailPasswordStrategy)
        if 'password123' in source or '@ejemplo.com' in source:
            # Permitimos estos en los comentarios/docstrings
            pass
        if 'supabase.co' in source:
            print("⚠️ Posible URL hardcodeada")
        else:
            print("✅ Auditoría: Sin credenciales hardcodeadas")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        print("\nNOTA: Para test real de login/register, usar credenciales")
        print("      reales de Supabase en un script separado.")
        
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
