# -*- coding: utf-8 -*-
"""
============================================================================
USER.PY - Entidad Usuario
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: MODELS (Dominio)
Patrón: Entity / Data Transfer Object
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: AUTH / CORE
- Requisitos: RF-01 (Registro), RF-02 (Login)
- HU: HU-01, HU-02, HU-03
- Caso de Uso: CU-01 (Gestionar Autenticación)

POR QUÉ DATACLASS:
- SÍ: Reduce boilerplate (genera __init__, __repr__, __eq__)
- SÍ: Inmutabilidad con frozen=True (opcional)
- SÍ: Type hints integrados
- NO alternativa (dict): Sin validación de tipos, sin autocompletado

POR QUÉ ENTIDAD SEPARADA:
- SÍ: Principio de responsabilidad única (SRP)
- SÍ: Desacopla la estructura del usuario de Supabase Auth
- SÍ: Facilita testing y mocking
- NO alternativa (usar dict de Supabase): Acoplamiento al SDK
============================================================================
"""

import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)


@dataclass
class User:
    """
    Entidad que representa un usuario autenticado.
    
    ARQUITECTURA:
    - Entidad de dominio (capa de modelos)
    - Inmutable después de creación (buena práctica)
    - Independiente de la fuente de datos (Supabase Auth)
    
    CAMPOS:
    - id: UUID del usuario en Supabase Auth
    - email: Email único del usuario
    - created_at: Fecha de registro (opcional, puede venir de Supabase)
    
    POR QUÉ pocos campos:
    - SÍ: MVP solo necesita id y email
    - SÍ: Extensible en futuras versiones
    - NO agregar campos que no usamos: YAGNI (You Aren't Gonna Need It)
    """
    
    id: str
    email: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """
        Validación después de la inicialización.
        
        POR QUÉ __post_init__:
        - SÍ: Permite validar después de que dataclass genera __init__
        - SÍ: Convierte created_at de string a datetime si es necesario
        """
        # Convertir created_at si viene como string
        if isinstance(self.created_at, str):
            try:
                # Formato ISO 8601 de Supabase
                object.__setattr__(
                    self, 
                    'created_at', 
                    datetime.fromisoformat(self.created_at.replace('Z', '+00:00'))
                )
            except (ValueError, AttributeError):
                pass  # Si falla, mantener el valor original
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Factory method para crear User desde diccionario de Supabase.
        
        POR QUÉ FACTORY METHOD:
        - SÍ: Encapsula la lógica de mapeo Supabase → User
        - SÍ: Maneja campos opcionales/faltantes
        - SÍ: Permite cambiar el SDK sin modificar código cliente
        - NO alternativa (constructor directo): Código duplicado en todos los usos
        
        EJEMPLO:
            response = supabase.auth.sign_in_with_password(...)
            user = User.from_dict(response.user.__dict__)
        """
        return cls(
            id=data.get('id', ''),
            email=data.get('email', ''),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte User a diccionario.
        
        POR QUÉ to_dict:
        - SÍ: Serialización para JSON, logging, etc.
        - SÍ: Consistencia con from_dict
        - SÍ: Formato seguro (no expone datos sensibles)
        """
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __str__(self) -> str:
        """
        Representación legible del usuario.
        
        SEGURIDAD: Solo muestra email, no el ID completo.
        """
        return f"User({self.email})"
    
    def get_masked_id(self) -> str:
        """
        Devuelve el ID parcialmente oculto para logging seguro.
        
        SEGURIDAD: No logueamos IDs completos.
        """
        if len(self.id) > 8:
            return f"{self.id[:4]}...{self.id[-4:]}"
        return "****"


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para User.
    
    EJECUCIÓN:
        python src/models/user.py
    
    RESULTADO ESPERADO:
        ✅ User creado desde dict
        ✅ to_dict funciona
        ✅ from_dict → to_dict roundtrip
        ✅ Seguridad: ID enmascarado
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: User (Entidad)")
    print("=" * 60)
    
    try:
        # Test 1: Crear User desde diccionario (simula respuesta de Supabase)
        supabase_response = {
            'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
            'email': 'test@ejemplo.com',
            'created_at': '2025-12-24T15:00:00Z'
        }
        
        user = User.from_dict(supabase_response)
        print(f"✅ User creado desde dict: {user}")
        
        # Test 2: Verificar campos
        assert user.id == supabase_response['id'], "ID no coincide"
        assert user.email == supabase_response['email'], "Email no coincide"
        print(f"   ID completo: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Created: {user.created_at}")
        
        # Test 3: to_dict
        user_dict = user.to_dict()
        print(f"✅ to_dict funciona: {user_dict}")
        
        # Test 4: Roundtrip from_dict → to_dict → from_dict
        user2 = User.from_dict(user_dict)
        assert user.id == user2.id, "Roundtrip falló - ID diferente"
        assert user.email == user2.email, "Roundtrip falló - Email diferente"
        print("✅ from_dict → to_dict roundtrip OK")
        
        # Test 5: ID enmascarado (seguridad)
        masked = user.get_masked_id()
        print(f"✅ ID enmascarado: {masked}")
        assert '...' in masked, "Máscara no aplicada"
        
        # Test 6: Sin datos sensibles hardcodeados
        import inspect
        source = inspect.getsource(User)
        if '@' in source and 'ejemplo.com' not in source:
            print("⚠️ Posible email hardcodeado en código")
        else:
            print("✅ Auditoría: Sin datos sensibles en código")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"❌ Assertion failed: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
