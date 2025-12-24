# -*- coding: utf-8 -*-
"""
============================================================================
TEST_SERVICES.PY - Tests para Servicios
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: TESTS / SERVICES
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: AUTH, NOTAS
- Prueba: SessionManager, AuthService, NotasService

SEGURIDAD:
- Sin credenciales reales (Mocks)
- Sin llamadas a Supabase real
- Fechas con timezone.utc
============================================================================
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, MagicMock, patch

import pytest

# Agregar directorio raíz al path
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

# Verificar si supabase está instalado
try:
    import supabase
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# Marker para tests que requieren supabase
requires_supabase = pytest.mark.skipif(
    not SUPABASE_AVAILABLE,
    reason="supabase package not installed"
)


# ============================================================================
# TESTS: SESSION MANAGER
# ============================================================================

@requires_supabase
class TestSessionManager:
    """Tests para SessionManager (Singleton)."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self, mock_env_vars):
        """Reset de todos los singletons antes de cada test."""
        from src.services.session_manager import SessionManager
        from src.config.settings import Settings
        
        SessionManager._instance = None
        SessionManager._initialized = False
        Settings._instance = None
        Settings._initialized = False
        
        yield
        
        # Cleanup
        SessionManager._instance = None
        SessionManager._initialized = False
        Settings._instance = None
        Settings._initialized = False
    
    @pytest.mark.unit
    def test_singleton_pattern(self, mock_env_vars):
        """Test: Singleton retorna misma instancia."""
        from src.services.session_manager import SessionManager
        
        session1 = SessionManager()
        session2 = SessionManager()
        
        assert session1 is session2
    
    @pytest.mark.unit
    def test_initial_state_not_authenticated(self, mock_env_vars):
        """Test: Estado inicial no autenticado."""
        from src.services.session_manager import SessionManager
        
        session = SessionManager()
        
        assert not session.is_authenticated()
        assert session.current_user is None
    
    @pytest.mark.unit
    def test_set_session(self, mock_env_vars, sample_user_data):
        """Test: Establecer sesión correctamente."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        
        session.set_session(
            user=user,
            access_token='test-token'
        )
        
        assert session.is_authenticated()
        assert session.current_user.email == sample_user_data['email']
    
    @pytest.mark.unit
    def test_clear_session(self, mock_env_vars, sample_user_data):
        """Test: Limpiar sesión."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        session.clear()
        
        assert not session.is_authenticated()
        assert session.current_user is None
        assert session.access_token is None
    
    @pytest.mark.unit
    def test_session_valid_not_expired(self, mock_env_vars, sample_user_data):
        """Test: Sesión válida cuando no ha expirado."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        assert session.is_session_valid()
    
    @pytest.mark.unit
    def test_session_invalid_after_timeout(self, mock_env_vars, sample_user_data):
        """Test: Sesión inválida después del timeout."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        # Simular timeout
        session._timeout_seconds = 1
        session._last_activity = datetime.now() - timedelta(seconds=5)
        
        assert not session.is_session_valid()
    
    @pytest.mark.unit
    def test_require_auth_raises_when_not_authenticated(self, mock_env_vars):
        """Test: require_auth lanza excepción sin autenticar."""
        from src.services.session_manager import SessionManager
        
        session = SessionManager()
        
        with pytest.raises(PermissionError) as exc_info:
            session.require_auth()
        
        assert 'autenticado' in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_require_auth_raises_when_expired(self, mock_env_vars, sample_user_data):
        """Test: require_auth lanza excepción cuando expiró."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        # Simular expiración
        session._timeout_seconds = 1
        session._last_activity = datetime.now() - timedelta(seconds=5)
        
        with pytest.raises(PermissionError) as exc_info:
            session.require_auth()
        
        assert 'expirad' in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_get_remaining_time(self, mock_env_vars, sample_user_data):
        """Test: Tiempo restante calculado correctamente."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        remaining = session.get_remaining_time()
        
        # Debe ser cercano al timeout (con margen de 5 segundos)
        assert remaining > session._timeout_seconds - 5
    
    @pytest.mark.unit
    def test_update_activity_resets_timer(self, mock_env_vars, sample_user_data):
        """Test: update_activity resetea el timer."""
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        session = SessionManager()
        user = User.from_dict(sample_user_data)
        session.set_session(user=user, access_token='test-token')
        
        # Simular paso del tiempo
        session._last_activity = datetime.now() - timedelta(seconds=60)
        remaining_before = session.get_remaining_time()
        
        # Actualizar actividad
        session.update_activity()
        remaining_after = session.get_remaining_time()
        
        # Debe haber reseteado
        assert remaining_after > remaining_before


# ============================================================================
# TESTS: AUTH SERVICE (con Mocks)
# ============================================================================

@requires_supabase
class TestAuthService:
    """Tests para AuthService."""
    
    @pytest.fixture(autouse=True)
    def reset_singletons(self, mock_env_vars):
        """Reset de singletons antes y después de cada test."""
        from src.services.session_manager import SessionManager
        from src.repositories.supabase_client import SupabaseClient
        from src.config.settings import Settings
        
        # Reset ANTES del test
        SessionManager._instance = None
        SessionManager._initialized = False
        SupabaseClient._instance = None
        SupabaseClient._initialized = False
        Settings._instance = None
        Settings._initialized = False  # Importante: resetear _initialized
        
        yield
        
        # Cleanup DESPUÉS del test
        SessionManager._instance = None
        SessionManager._initialized = False
        SupabaseClient._instance = None
        SupabaseClient._initialized = False
        Settings._instance = None
        Settings._initialized = False
    
    @pytest.mark.unit
    def test_auth_service_creation(self, mock_env_vars):
        """Test: AuthService se crea correctamente."""
        from src.services.auth_service import AuthService
        
        auth = AuthService()
        
        assert auth is not None
        assert auth._strategy is not None
    
    @pytest.mark.unit
    def test_initial_not_authenticated(self, mock_env_vars):
        """Test: Estado inicial no autenticado."""
        from src.services.auth_service import AuthService
        
        auth = AuthService()
        
        assert not auth.is_authenticated()
    
    @pytest.mark.unit
    def test_login_validation_empty_email(self, mock_env_vars):
        """Test: Login falla con email vacío."""
        from src.services.auth_service import EmailPasswordStrategy
        
        strategy = EmailPasswordStrategy(Mock())
        
        with pytest.raises(ValueError) as exc_info:
            strategy.login(email='', password='password123')
        
        assert 'email' in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_login_validation_short_password(self, mock_env_vars):
        """Test: Login falla con password corto."""
        from src.services.auth_service import EmailPasswordStrategy
        
        strategy = EmailPasswordStrategy(Mock())
        
        with pytest.raises(ValueError) as exc_info:
            strategy.login(email='test@test.com', password='123')
        
        assert 'caracteres' in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_logout_clears_session(self, mock_env_vars):
        """Test: Logout limpia la sesión."""
        from src.services.auth_service import AuthService
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        auth = AuthService()
        session = SessionManager()
        
        # Simular sesión activa
        user = User(id='test-id', email='test@test.com')
        session.set_session(user=user, access_token='test-token')
        
        # Logout
        auth.logout()
        
        assert not session.is_authenticated()


# ============================================================================
# TESTS: NOTAS SERVICE (con Mocks)
# ============================================================================

@requires_supabase
class TestNotasService:
    """Tests para NotasService."""
    
    @pytest.fixture(autouse=True)
    def reset_singletons(self, mock_env_vars):
        """Reset de singletons antes y después de cada test."""
        from src.services.session_manager import SessionManager
        from src.repositories.supabase_client import SupabaseClient
        from src.config.settings import Settings
        
        # Reset ANTES del test
        SessionManager._instance = None
        SessionManager._initialized = False
        SupabaseClient._instance = None
        SupabaseClient._initialized = False
        Settings._instance = None
        Settings._initialized = False
        
        yield
        
        # Cleanup DESPUÉS del test
        SessionManager._instance = None
        SessionManager._initialized = False
        SupabaseClient._instance = None
        SupabaseClient._initialized = False
        Settings._instance = None
        Settings._initialized = False
    
    @pytest.mark.unit
    def test_notas_service_creation(self, mock_env_vars):
        """Test: NotasService se crea correctamente."""
        from src.services.notas_service import NotasService
        
        notas = NotasService()
        
        assert notas is not None
        assert notas._session is not None
    
    @pytest.mark.unit
    def test_listar_requires_auth(self, mock_env_vars):
        """Test: Listar requiere autenticación."""
        from src.services.notas_service import NotasService
        
        notas = NotasService()
        
        with pytest.raises(PermissionError):
            notas.listar()
    
    @pytest.mark.unit
    def test_crear_requires_auth(self, mock_env_vars):
        """Test: Crear requiere autenticación."""
        from src.services.notas_service import NotasService
        
        notas = NotasService()
        
        with pytest.raises(PermissionError):
            notas.crear('Título', 'Contenido')
    
    @pytest.mark.unit
    def test_eliminar_requires_auth(self, mock_env_vars):
        """Test: Eliminar requiere autenticación."""
        from src.services.notas_service import NotasService
        
        notas = NotasService()
        
        with pytest.raises(PermissionError):
            notas.eliminar('nota-id')


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    """
    Ejecución directa para prueba rápida.
    
    COMANDO:
        python tests/test_services.py
    
    O con pytest:
        pytest tests/test_services.py -v
    """
    pytest.main([__file__, '-v', '--tb=short'])
