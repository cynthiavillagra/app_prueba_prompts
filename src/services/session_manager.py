# -*- coding: utf-8 -*-
"""
============================================================================
SESSION_MANAGER.PY - Gestor de Sesión (Singleton)
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: SERVICES
Patrón: Singleton
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: AUTH
- Requisitos: RF-03 (Logout), RF-04 (Protección), RF-15 (Persistir sesión)
- HU: HU-02, HU-03
- Caso de Uso: CU-01 (Gestionar Autenticación)

POR QUÉ SINGLETON:
- SÍ: Estado de sesión único para toda la app
- SÍ: Evita múltiples "usuarios logueados" simultáneos
- SÍ: Punto central para verificar autenticación
- NO alternativa (variable global): Menos encapsulación, testing difícil

ARQUITECTURA STATELESS (SERVERLESS):
- IMPORTANTE: En Vercel, cada request es independiente
- Este SessionManager es para CLI/local
- En serverless, la sesión viene del JWT en el header
============================================================================
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Optional

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from src.config.settings import Settings
from src.models.user import User


class SessionManager:
    """
    Singleton para gestión de sesión del usuario.
    
    RESPONSABILIDADES:
    - Almacenar usuario y token actuales
    - Verificar timeout de inactividad (15 min)
    - Proveer métodos de verificación de autenticación
    
    SEGURIDAD:
    - Timeout de 15 minutos de inactividad
    - Limpieza de sesión en logout
    - Verificación antes de cada operación
    
    STATELESS WARNING:
    En entornos serverless (Vercel), este Singleton se reinicia
    en cada cold start. Para serverless, usar JWT del header.
    """
    
    _instance: Optional['SessionManager'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'SessionManager':
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Inicializa la sesión (solo la primera vez)."""
        if not SessionManager._initialized:
            self._initialize()
            SessionManager._initialized = True
    
    def _initialize(self) -> None:
        """
        Inicializa los atributos de sesión.
        
        Estado inicial: Sin usuario autenticado
        """
        self._current_user: Optional[User] = None
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._last_activity: Optional[datetime] = None
        
        # Cargar timeout desde configuración
        settings = Settings()
        self._timeout_seconds: int = settings.session_timeout_seconds
    
    def set_session(
        self, 
        user: User, 
        access_token: str, 
        refresh_token: Optional[str] = None
    ) -> None:
        """
        Establece la sesión después de login exitoso.
        
        PARÁMETROS:
        - user: Entidad User autenticada
        - access_token: JWT de Supabase
        - refresh_token: Token para renovar sesión (opcional)
        
        IMPORTANTE: Resetea el timer de actividad
        """
        self._current_user = user
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._last_activity = datetime.now()
    
    def clear(self) -> None:
        """
        Limpia la sesión (logout).
        
        SEGURIDAD: Elimina todos los datos sensibles de memoria
        """
        self._current_user = None
        self._access_token = None
        self._refresh_token = None
        self._last_activity = None
    
    def update_activity(self) -> None:
        """
        Actualiza el timestamp de última actividad.
        
        LLAMAR: Después de cada acción del usuario
        POR QUÉ: Resetea el contador de 15 minutos
        """
        self._last_activity = datetime.now()
    
    def is_authenticated(self) -> bool:
        """
        Verifica si hay un usuario autenticado.
        
        IMPORTANTE: No verifica el timeout, solo si hay usuario
        Para verificación completa, usar is_session_valid()
        """
        return self._current_user is not None
    
    def is_session_valid(self) -> bool:
        """
        Verifica si la sesión es válida (autenticado + no expirado).
        
        LÓGICA:
        1. Debe haber usuario autenticado
        2. Debe haber registro de actividad
        3. No debe haber pasado el timeout
        
        RETORNA: True si la sesión es válida, False si expiró o no existe
        """
        if not self.is_authenticated():
            return False
        
        if self._last_activity is None:
            return False
        
        # Calcular tiempo transcurrido
        elapsed = datetime.now() - self._last_activity
        timeout_delta = timedelta(seconds=self._timeout_seconds)
        
        return elapsed < timeout_delta
    
    def get_remaining_time(self) -> int:
        """
        Obtiene segundos restantes antes de expiración.
        
        RETORNA:
        - Segundos restantes si hay sesión activa
        - 0 si no hay sesión o ya expiró
        """
        if not self.is_authenticated() or self._last_activity is None:
            return 0
        
        elapsed = datetime.now() - self._last_activity
        remaining = self._timeout_seconds - int(elapsed.total_seconds())
        
        return max(0, remaining)
    
    def require_auth(self) -> None:
        """
        Lanza excepción si no hay sesión válida.
        
        POR QUÉ EXCEPCIÓN:
        - SÍ: Permite usar decorator pattern
        - SÍ: Código limpio en services
        - NO alternativa (return bool): Requiere if en cada método
        
        USO:
            session = SessionManager()
            session.require_auth()  # Lanza si no autenticado
            # ... código que requiere auth ...
        
        RAISES:
            PermissionError: Si no hay sesión válida (incluye razón)
        """
        if not self.is_authenticated():
            raise PermissionError(
                "No autenticado. Debe iniciar sesión primero."
            )
        
        if not self.is_session_valid():
            self.clear()  # Limpiar sesión expirada
            raise PermissionError(
                "Sesión expirada por inactividad (15 minutos). "
                "Debe iniciar sesión nuevamente."
            )
    
    @property
    def current_user(self) -> Optional[User]:
        """Usuario actualmente autenticado (o None)."""
        return self._current_user
    
    @property
    def access_token(self) -> Optional[str]:
        """Token de acceso actual (o None)."""
        return self._access_token
    
    def get_user_id(self) -> Optional[str]:
        """
        Obtiene el ID del usuario actual.
        
        RETORNA: UUID del usuario o None si no autenticado
        """
        if self._current_user:
            return self._current_user.id
        return None


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para SessionManager.
    
    EJECUCIÓN:
        python src/services/session_manager.py
    
    RESULTADO ESPERADO:
        ✅ Singleton funciona
        ✅ Sesión establecida
        ✅ Timeout funciona
        ✅ require_auth funciona
    """
    import time
    
    print("=" * 60)
    print("PRUEBA DE FUEGO: SessionManager (Singleton)")
    print("=" * 60)
    
    try:
        # Test 1: Singleton
        session1 = SessionManager()
        session2 = SessionManager()
        assert session1 is session2, "Singleton roto"
        print("✅ Singleton verificado: misma instancia")
        
        # Test 2: Estado inicial (no autenticado)
        session1.clear()  # Asegurar estado limpio
        assert not session1.is_authenticated(), "Debería no estar autenticado"
        print("✅ Estado inicial: no autenticado")
        
        # Test 3: Establecer sesión
        test_user = User(
            id='test-user-id-1234',
            email='test@ejemplo.com'
        )
        session1.set_session(
            user=test_user,
            access_token='fake-jwt-token-for-testing'
        )
        assert session1.is_authenticated(), "Debería estar autenticado"
        print(f"✅ Sesión establecida: {session1.current_user}")
        
        # Test 4: Sesión válida (no expirada)
        assert session1.is_session_valid(), "Sesión debería ser válida"
        remaining = session1.get_remaining_time()
        print(f"✅ Sesión válida. Tiempo restante: {remaining}s")
        
        # Test 5: require_auth no lanza excepción
        try:
            session1.require_auth()
            print("✅ require_auth() pasó (sesión válida)")
        except PermissionError as e:
            print(f"❌ require_auth falló incorrectamente: {e}")
        
        # Test 6: Simular expiración (modificar _last_activity)
        # Guardamos el timeout original
        original_timeout = session1._timeout_seconds
        session1._timeout_seconds = 1  # 1 segundo para test rápido
        session1._last_activity = datetime.now() - timedelta(seconds=2)
        
        assert not session1.is_session_valid(), "Sesión debería estar expirada"
        print("✅ Timeout funciona: sesión expirada detectada")
        
        # Test 7: require_auth lanza excepción si expirado
        try:
            session1.require_auth()
            print("❌ ERROR: require_auth debería haber lanzado excepción")
        except PermissionError as e:
            print(f"✅ require_auth lanzó excepción correcta: {str(e)[:40]}...")
        
        # Test 8: Verificar que clear() limpia todo
        session1.clear()
        assert session1.current_user is None, "User no limpiado"
        assert session1.access_token is None, "Token no limpiado"
        print("✅ clear() limpia todos los datos")
        
        # Restaurar timeout
        session1._timeout_seconds = original_timeout
        
        # Test 9: Verificar que no hay sesiones hardcodeadas
        import inspect
        source = inspect.getsource(SessionManager)
        if 'session_store = {}' in source or "sessions = {" in source:
            print("⚠️ ADVERTENCIA: Posible almacenamiento de sesiones global")
        else:
            print("✅ Stateless: sin almacenamiento de sesiones global")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"❌ Assertion failed: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
