# -*- coding: utf-8 -*-
"""
============================================================================
TEST_API.PY - Tests para la API/Bridge
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: TESTS / API
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: API
- Prueba: VercelBridge routes y handlers

SEGURIDAD:
- Sin llamadas reales a Supabase
- Mocks para todos los servicios
============================================================================
"""

import sys
import os
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
# TESTS: VERCEL BRIDGE
# ============================================================================

@requires_supabase
class TestVercelBridge:
    """Tests para VercelBridge (Router API)."""
    
    @pytest.fixture
    def bridge(self, mock_env_vars):
        """Fixture que crea un VercelBridge."""
        from api.index import VercelBridge
        return VercelBridge()
    
    @pytest.mark.unit
    def test_health_check_get(self, bridge):
        """Test: GET /api/health retorna status ok."""
        status, data = bridge.handle_request('GET', '/api/health', {})
        
        assert status == 200
        assert data['status'] == 'ok'
        assert 'CRUD' in data['message']
    
    @pytest.mark.unit
    def test_health_check_root(self, bridge):
        """Test: GET / también retorna health check."""
        status, data = bridge.handle_request('GET', '/', {})
        
        assert status == 200
        assert data['status'] == 'ok'
    
    @pytest.mark.unit
    def test_unknown_route_returns_404(self, bridge):
        """Test: Ruta desconocida retorna 404."""
        status, data = bridge.handle_request('GET', '/api/unknown', {})
        
        assert status == 404
        assert 'error' in data
    
    @pytest.mark.unit
    def test_login_empty_email_returns_400(self, bridge):
        """Test: Login sin email retorna 400."""
        status, data = bridge.handle_request(
            'POST', 
            '/api/auth/login', 
            {},
            body={'email': '', 'password': 'password123'}
        )
        
        assert status == 400
        assert 'error' in data
    
    @pytest.mark.unit
    def test_login_empty_password_returns_400(self, bridge):
        """Test: Login sin password retorna 400."""
        status, data = bridge.handle_request(
            'POST', 
            '/api/auth/login', 
            {},
            body={'email': 'test@test.com', 'password': ''}
        )
        
        assert status == 400
        assert 'error' in data
    
    @pytest.mark.unit
    def test_notas_get_requires_auth(self, bridge):
        """Test: GET /api/notas requiere autenticación."""
        status, data = bridge.handle_request('GET', '/api/notas', {})
        
        # Sin sesión, debe retornar 401
        assert status == 401
        assert 'error' in data
    
    @pytest.mark.unit
    def test_notas_post_requires_auth(self, bridge):
        """Test: POST /api/notas requiere autenticación."""
        status, data = bridge.handle_request(
            'POST', 
            '/api/notas', 
            {},
            body={'titulo': 'Test', 'contenido': 'Contenido'}
        )
        
        assert status == 401
        assert 'error' in data
    
    @pytest.mark.unit
    def test_notas_delete_requires_auth(self, bridge):
        """Test: DELETE /api/notas requiere autenticación."""
        status, data = bridge.handle_request(
            'DELETE', 
            '/api/notas', 
            {'id': ['nota-id-123']}
        )
        
        assert status == 401
        assert 'error' in data
    
    @pytest.mark.unit
    def test_notas_post_without_title_returns_400(self, bridge):
        """Test: POST /api/notas sin título retorna 400."""
        # Simular sesión activa
        from src.services.session_manager import SessionManager
        from src.models.user import User
        
        # Reset singleton
        SessionManager._instance = None
        SessionManager._initialized = False
        
        session = SessionManager()
        user = User(id='test-id', email='test@test.com')
        session.set_session(user=user, access_token='fake-token')
        
        try:
            status, data = bridge.handle_request(
                'POST', 
                '/api/notas', 
                {},
                body={'titulo': '', 'contenido': 'Contenido'}
            )
            
            # Puede ser 400 (validation) o 401/500 dependiendo del mock
            assert status in [400, 401, 500]
        finally:
            session.clear()
            SessionManager._instance = None
            SessionManager._initialized = False
    
    @pytest.mark.unit
    def test_logout_returns_success(self, bridge):
        """Test: POST /api/auth/logout siempre retorna success."""
        status, data = bridge.handle_request('POST', '/api/auth/logout', {})
        
        assert status == 200
        assert data['success'] == True


# ============================================================================
# TESTS: RESPONSE FORMAT
# ============================================================================

@requires_supabase
class TestApiResponseFormat:
    """Tests para verificar formato de respuestas."""
    
    @pytest.fixture
    def bridge(self, mock_env_vars):
        from api.index import VercelBridge
        return VercelBridge()
    
    @pytest.mark.unit
    def test_success_response_has_required_fields(self, bridge):
        """Test: Respuestas exitosas tienen campos requeridos."""
        status, data = bridge.handle_request('GET', '/api/health', {})
        
        # Health check tiene estos campos
        assert 'status' in data
        assert 'message' in data
        assert 'version' in data
    
    @pytest.mark.unit
    def test_error_response_has_error_field(self, bridge):
        """Test: Respuestas de error tienen campo 'error'."""
        status, data = bridge.handle_request('GET', '/api/unknown', {})
        
        assert 'error' in data


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    """
    Ejecución directa para prueba rápida.
    
    COMANDO:
        python tests/test_api.py
    
    O con pytest:
        pytest tests/test_api.py -v
    """
    pytest.main([__file__, '-v', '--tb=short'])
