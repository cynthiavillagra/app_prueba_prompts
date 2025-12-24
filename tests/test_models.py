# -*- coding: utf-8 -*-
"""
============================================================================
TEST_MODELS.PY - Tests para Entidades/Modelos
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: TESTS / MODELS
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: NOTAS, AUTH
- Prueba: User, Nota dataclasses

SEGURIDAD:
- Sin credenciales reales
- Datos ficticios de prueba
- Fechas con timezone.utc
============================================================================
"""

import sys
import os
from datetime import datetime, timezone

import pytest

# Agregar directorio raíz al path
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from src.models.user import User
from src.models.nota import Nota


# ============================================================================
# TESTS: USER
# ============================================================================

class TestUser:
    """Tests para la entidad User."""
    
    @pytest.mark.unit
    def test_user_creation_basic(self, sample_user_data):
        """Test: Crear User con datos básicos."""
        user = User(
            id=sample_user_data['id'],
            email=sample_user_data['email']
        )
        
        assert user.id == sample_user_data['id']
        assert user.email == sample_user_data['email']
        assert user.created_at is None  # Opcional
    
    @pytest.mark.unit
    def test_user_from_dict(self, sample_user_data):
        """Test: Factory method from_dict."""
        user = User.from_dict(sample_user_data)
        
        assert user.id == sample_user_data['id']
        assert user.email == sample_user_data['email']
    
    @pytest.mark.unit
    def test_user_to_dict(self, sample_user_data):
        """Test: Serialización a diccionario."""
        user = User.from_dict(sample_user_data)
        result = user.to_dict()
        
        assert 'id' in result
        assert 'email' in result
        assert result['email'] == sample_user_data['email']
    
    @pytest.mark.unit
    def test_user_masked_id(self, sample_user_data):
        """Test: ID enmascarado para logs."""
        user = User.from_dict(sample_user_data)
        masked = user.get_masked_id()
        
        # Debe mostrar solo los primeros 8 caracteres
        assert '...' in masked
        assert len(masked) < len(user.id)
    
    @pytest.mark.unit
    def test_user_str_representation(self, sample_user_data):
        """Test: Representación string."""
        user = User.from_dict(sample_user_data)
        str_repr = str(user)
        
        assert sample_user_data['email'] in str_repr


# ============================================================================
# TESTS: NOTA
# ============================================================================

class TestNota:
    """Tests para la entidad Nota."""
    
    @pytest.mark.unit
    def test_nota_creation_basic(self, sample_nota_data):
        """Test: Crear Nota con datos básicos."""
        nota = Nota(
            id=sample_nota_data['id'],
            user_id=sample_nota_data['user_id'],
            title=sample_nota_data['title'],
            content=sample_nota_data['content']
        )
        
        assert nota.id == sample_nota_data['id']
        assert nota.title == sample_nota_data['title']
        assert nota.content == sample_nota_data['content']
    
    @pytest.mark.unit
    def test_nota_from_dict(self, sample_nota_data):
        """Test: Factory method from_dict."""
        nota = Nota.from_dict(sample_nota_data)
        
        assert nota.id == sample_nota_data['id']
        assert nota.title == sample_nota_data['title']
    
    @pytest.mark.unit
    def test_nota_validation_empty_title(self, sample_nota_data):
        """Test: Validación - título vacío lanza error."""
        with pytest.raises(ValueError) as exc_info:
            Nota(
                id=sample_nota_data['id'],
                user_id=sample_nota_data['user_id'],
                title='',  # Vacío
                content='Contenido'
            )
        
        assert 'título' in str(exc_info.value).lower() or 'title' in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_nota_validation_whitespace_title(self, sample_nota_data):
        """Test: Validación - título solo espacios lanza error."""
        with pytest.raises(ValueError):
            Nota(
                id=sample_nota_data['id'],
                user_id=sample_nota_data['user_id'],
                title='   ',  # Solo espacios
                content='Contenido'
            )
    
    @pytest.mark.unit
    def test_nota_to_dict_with_id(self, sample_nota_data):
        """Test: Serialización con ID incluido."""
        nota = Nota.from_dict(sample_nota_data)
        result = nota.to_dict(include_id=True)
        
        assert 'id' in result
        assert result['id'] == sample_nota_data['id']
    
    @pytest.mark.unit
    def test_nota_to_dict_without_id(self, sample_nota_data):
        """Test: Serialización sin ID (para INSERT)."""
        nota = Nota.from_dict(sample_nota_data)
        result = nota.to_dict(include_id=False)
        
        assert 'id' not in result
        assert 'title' in result
    
    @pytest.mark.unit
    def test_nota_get_preview_short_content(self, sample_nota_data):
        """Test: Preview con contenido corto."""
        nota = Nota.from_dict(sample_nota_data)
        preview = nota.get_preview(100)
        
        # Contenido corto no debe truncarse
        assert preview == sample_nota_data['content']
    
    @pytest.mark.unit
    def test_nota_get_preview_long_content(self):
        """Test: Preview con contenido largo se trunca."""
        long_content = "A" * 200
        nota = Nota(
            id='test-id',
            user_id='test-user',
            title='Test',
            content=long_content
        )
        
        preview = nota.get_preview(50)
        
        assert len(preview) <= 53  # 50 + "..."
        assert preview.endswith('...')
    
    @pytest.mark.unit
    def test_nota_to_display_dict(self, sample_nota_data):
        """Test: Diccionario para UI."""
        nota = Nota.from_dict(sample_nota_data)
        display = nota.to_display_dict()
        
        assert 'title' in display
        assert 'content' in display
        assert 'created_at' in display


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    """
    Ejecución directa para prueba rápida.
    
    COMANDO:
        python tests/test_models.py
    
    O con pytest:
        pytest tests/test_models.py -v
    """
    pytest.main([__file__, '-v', '--tb=short'])
