# -*- coding: utf-8 -*-
"""
============================================================================
NOTA.PY - Entidad Nota
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: MODELS (Dominio)
Patrón: Entity / Data Transfer Object
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: NOTAS
- Requisitos: RF-05 (Crear), RF-06 (Listar), RF-07 (Editar), RF-08 (Eliminar)
- HU: HU-04, HU-05, HU-06, HU-07
- Caso de Uso: CU-02 (Gestionar Notas)

POR QUÉ DATACLASS:
- SÍ: Consistencia con User (mismo patrón)
- SÍ: Reduce boilerplate
- SÍ: Type hints integrados
- NO alternativa (NamedTuple): No soporta valores por defecto fácilmente
============================================================================
"""

import sys
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)


@dataclass
class Nota:
    """
    Entidad que representa una nota del usuario.
    
    ARQUITECTURA:
    - Entidad de dominio (capa de modelos)
    - Mapeada a tabla `notas` en Supabase
    - RLS asegura que user_id = auth.uid()
    
    CAMPOS:
    - id: UUID de la nota (generado por Supabase)
    - user_id: UUID del propietario (FK a auth.users)
    - title: Título obligatorio
    - content: Contenido opcional
    - created_at: Fecha de creación
    - updated_at: Fecha de última modificación
    
    SEGURIDAD:
    - RLS en Supabase filtra por user_id automáticamente
    - Nunca se puede acceder a notas de otro usuario
    """
    
    id: str
    user_id: str
    title: str
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """
        Validación y conversión después de la inicialización.
        
        VALIDACIONES:
        - title no puede estar vacío
        - Conversión de strings ISO a datetime
        """
        # Validar título obligatorio
        if not self.title or not self.title.strip():
            raise ValueError("El título de la nota no puede estar vacío")
        
        # Limpiar título (trim)
        object.__setattr__(self, 'title', self.title.strip())
        
        # Convertir fechas si vienen como string
        for field_name in ['created_at', 'updated_at']:
            value = getattr(self, field_name)
            if isinstance(value, str):
                try:
                    converted = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    object.__setattr__(self, field_name, converted)
                except (ValueError, AttributeError):
                    pass
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Nota':
        """
        Factory method para crear Nota desde diccionario de Supabase.
        
        POR QUÉ FACTORY METHOD:
        - SÍ: Encapsula mapeo Supabase → Nota
        - SÍ: Maneja campos opcionales
        - SÍ: Punto único de creación
        
        EJEMPLO:
            response = supabase.table('notas').select('*').execute()
            notas = [Nota.from_dict(n) for n in response.data]
        """
        return cls(
            id=data.get('id', ''),
            user_id=data.get('user_id', ''),
            title=data.get('title', 'Sin título'),
            content=data.get('content'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self, include_id: bool = True) -> Dict[str, Any]:
        """
        Convierte Nota a diccionario.
        
        PARÁMETROS:
        - include_id: Si es False, omite id (para INSERT en Supabase)
        
        POR QUÉ include_id opcional:
        - SÍ: Para INSERT, Supabase genera el id
        - SÍ: Para UPDATE, necesitamos el id
        
        EJEMPLO:
            # Para crear nueva nota
            supabase.table('notas').insert(nota.to_dict(include_id=False))
            
            # Para actualizar
            supabase.table('notas').update(nota.to_dict())
        """
        result = {
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content
        }
        
        if include_id and self.id:
            result['id'] = self.id
        
        # No incluimos created_at/updated_at porque Supabase los maneja
        return result
    
    def to_display_dict(self) -> Dict[str, Any]:
        """
        Versión para mostrar en UI (con fechas formateadas).
        
        POR QUÉ método separado:
        - SÍ: to_dict es para persistencia
        - SÍ: to_display_dict es para presentación
        - NO mezclar responsabilidades
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content or '(Sin contenido)',
            'created_at': self._format_date(self.created_at),
            'updated_at': self._format_date(self.updated_at)
        }
    
    def _format_date(self, dt: Optional[datetime]) -> str:
        """Formatea fecha para display."""
        if dt is None:
            return 'N/A'
        return dt.strftime('%d/%m/%Y %H:%M')
    
    def __str__(self) -> str:
        """
        Representación legible de la nota.
        
        FORMATO: [id_corto] título
        """
        short_id = self.id[:8] if len(self.id) >= 8 else self.id
        return f"[{short_id}] {self.title}"
    
    def get_preview(self, max_length: int = 50) -> str:
        """
        Obtiene preview del contenido (truncado).
        
        POR QUÉ:
        - SÍ: Para listas donde no queremos texto completo
        - SÍ: Mejora UX en CLI
        """
        if not self.content:
            return "(Sin contenido)"
        
        if len(self.content) <= max_length:
            return self.content
        
        return self.content[:max_length].rsplit(' ', 1)[0] + "..."


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para Nota.
    
    EJECUCIÓN:
        python src/models/nota.py
    
    RESULTADO ESPERADO:
        ✅ Nota creada desde dict
        ✅ Validación de título funciona
        ✅ to_dict funciona
        ✅ Preview funciona
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: Nota (Entidad)")
    print("=" * 60)
    
    try:
        # Test 1: Crear Nota desde diccionario (simula respuesta de Supabase)
        supabase_response = {
            'id': 'nota-1234-5678-abcd-ef1234567890',
            'user_id': 'user-1111-2222-3333-444455556666',
            'title': '  Mi primera nota  ',  # Con espacios para test de trim
            'content': 'Este es el contenido de mi nota de prueba para verificar que todo funciona correctamente.',
            'created_at': '2025-12-24T15:00:00Z',
            'updated_at': '2025-12-24T15:30:00Z'
        }
        
        nota = Nota.from_dict(supabase_response)
        print(f"✅ Nota creada desde dict: {nota}")
        
        # Test 2: Verificar trim del título
        assert nota.title == 'Mi primera nota', f"Título no limpio: '{nota.title}'"
        print(f"✅ Título limpiado (trim): '{nota.title}'")
        
        # Test 3: Validación de título vacío
        try:
            nota_invalida = Nota(id='x', user_id='x', title='   ')
            print("❌ ERROR: Debería fallar con título vacío")
        except ValueError as e:
            print(f"✅ Validación de título funciona: {e}")
        
        # Test 4: to_dict sin id (para INSERT)
        dict_insert = nota.to_dict(include_id=False)
        assert 'id' not in dict_insert, "ID no debería estar en dict para INSERT"
        print(f"✅ to_dict(include_id=False) funciona: {list(dict_insert.keys())}")
        
        # Test 5: to_dict con id (para UPDATE)
        dict_update = nota.to_dict(include_id=True)
        assert 'id' in dict_update, "ID debería estar en dict para UPDATE"
        print(f"✅ to_dict(include_id=True) funciona: {list(dict_update.keys())}")
        
        # Test 6: Preview
        preview = nota.get_preview(30)
        assert len(preview) <= 33, f"Preview muy largo: {len(preview)}"  # 30 + "..."
        print(f"✅ Preview funciona: '{preview}'")
        
        # Test 7: to_display_dict
        display = nota.to_display_dict()
        assert 'created_at' in display, "Falta created_at en display"
        print(f"✅ to_display_dict funciona: fecha = {display['created_at']}")
        
        # Test 8: Roundtrip
        nota2 = Nota.from_dict(nota.to_dict())
        assert nota.title == nota2.title, "Roundtrip falló"
        print("✅ Roundtrip from_dict → to_dict OK")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"❌ Assertion failed: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
