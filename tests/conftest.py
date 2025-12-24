# -*- coding: utf-8 -*-
"""
============================================================================
CONFTEST.PY - Configuración de Pytest
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: TESTS
Fecha: 2025-12-24

POR QUÉ CONFTEST:
- SÍ: Fixtures compartidos entre tests
- SÍ: Mocks centralizados
- SÍ: Configuración de pytest
- NO fixtures en cada test: Código duplicado
============================================================================
"""

import sys
import os
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock
from typing import Dict, Any

import pytest

# Agregar directorio raíz al path
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)


# ============================================================================
# FIXTURES DE CONFIGURACIÓN
# ============================================================================

@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Fixture que simula variables de entorno.
    
    SEGURIDAD:
    - Sin credenciales reales
    - URLs de prueba
    - Keys ficticias
    
    POR QUÉ MONKEYPATCH:
    - SÍ: Forma estándar de pytest para env vars
    - SÍ: Se limpia automáticamente después del test
    """
    monkeypatch.setenv('SUPABASE_URL', 'https://test-project.supabase.co')
    monkeypatch.setenv('SUPABASE_KEY', 'eyJ0ZXN0IjoibW9ja19rZXlfZm9yX3Rlc3RpbmcifQ==')
    monkeypatch.setenv('SESSION_TIMEOUT_SECONDS', '900')
    monkeypatch.setenv('DEBUG', 'true')


@pytest.fixture
def mock_datetime():
    """
    Fixture que proporciona datetime con timezone.
    
    REGLA: Siempre usar datetime.now(timezone.utc)
    """
    return datetime.now(timezone.utc)


# ============================================================================
# FIXTURES DE ENTIDADES
# ============================================================================

@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """
    Datos de usuario de prueba.
    
    SEGURIDAD: Email ficticio, no real.
    """
    return {
        'id': 'test-user-uuid-1234-5678',
        'email': 'test@example-test.com',
        'created_at': datetime.now(timezone.utc).isoformat()
    }


@pytest.fixture
def sample_nota_data() -> Dict[str, Any]:
    """
    Datos de nota de prueba.
    
    Incluye todos los campos del modelo.
    """
    now = datetime.now(timezone.utc)
    return {
        'id': 'test-nota-uuid-1234-5678',
        'user_id': 'test-user-uuid-1234-5678',
        'title': 'Nota de Prueba',
        'content': 'Contenido de prueba para testing',
        'created_at': now.isoformat(),
        'updated_at': now.isoformat()
    }


@pytest.fixture
def multiple_notas_data() -> list:
    """
    Lista de notas para pruebas de listado.
    """
    now = datetime.now(timezone.utc)
    return [
        {
            'id': f'nota-uuid-{i}',
            'user_id': 'test-user-uuid-1234-5678',
            'title': f'Nota de Prueba {i}',
            'content': f'Contenido {i}',
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        for i in range(1, 4)
    ]


# ============================================================================
# FIXTURES DE MOCKS - SUPABASE
# ============================================================================

@pytest.fixture
def mock_supabase_response():
    """
    Factory para crear respuestas mock de Supabase.
    
    POR QUÉ FACTORY:
    - SÍ: Flexible para diferentes respuestas
    - SÍ: Reutilizable
    """
    def _create_response(data: list = None, count: int = None, error: str = None):
        response = Mock()
        response.data = data or []
        response.count = count
        if error:
            response.error = Mock(message=error)
        else:
            response.error = None
        return response
    
    return _create_response


@pytest.fixture
def mock_supabase_client(mock_supabase_response):
    """
    Mock completo del cliente Supabase.
    
    Simula:
    - table().select().execute()
    - table().insert().execute()
    - table().update().eq().execute()
    - table().delete().eq().execute()
    - auth.sign_in_with_password()
    - auth.sign_out()
    """
    client = MagicMock()
    
    # Mock de table queries
    query_mock = MagicMock()
    query_mock.select.return_value = query_mock
    query_mock.insert.return_value = query_mock
    query_mock.update.return_value = query_mock
    query_mock.delete.return_value = query_mock
    query_mock.eq.return_value = query_mock
    query_mock.order.return_value = query_mock
    query_mock.execute.return_value = mock_supabase_response([])
    
    client.table.return_value = query_mock
    
    # Mock de auth
    auth_mock = MagicMock()
    client.auth = auth_mock
    
    return client


@pytest.fixture
def mock_auth_response(sample_user_data):
    """
    Mock de respuesta de autenticación de Supabase.
    """
    response = Mock()
    response.user = Mock()
    response.user.id = sample_user_data['id']
    response.user.email = sample_user_data['email']
    response.user.created_at = sample_user_data['created_at']
    
    response.session = Mock()
    response.session.access_token = 'mock-access-token-for-testing'
    response.session.refresh_token = 'mock-refresh-token-for-testing'
    
    return response


# ============================================================================
# FIXTURES DE SERVICIOS (CON MOCKS)
# ============================================================================

@pytest.fixture
def mock_session_manager():
    """
    SessionManager con estado controlado para tests.
    """
    from src.services.session_manager import SessionManager
    
    # Limpiar singleton para test aislado
    SessionManager._instance = None
    SessionManager._initialized = False
    
    session = SessionManager()
    
    yield session
    
    # Cleanup
    session.clear()
    SessionManager._instance = None
    SessionManager._initialized = False


# ============================================================================
# MARKERS
# ============================================================================

def pytest_configure(config):
    """Configura markers personalizados."""
    config.addinivalue_line(
        "markers", "unit: marca tests unitarios"
    )
    config.addinivalue_line(
        "markers", "integration: marca tests de integración"
    )
    config.addinivalue_line(
        "markers", "slow: marca tests que tardan más de 1 segundo"
    )
