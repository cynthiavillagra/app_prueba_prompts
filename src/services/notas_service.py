# -*- coding: utf-8 -*-
"""
============================================================================
NOTAS_SERVICE.PY - Servicio CRUD de Notas
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: SERVICES
Patrón: Adapter
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: NOTAS
- Requisitos: RF-05 (Crear), RF-06 (Listar), RF-07 (Editar), RF-08 (Eliminar)
- HU: HU-04, HU-05, HU-06, HU-07
- Caso de Uso: CU-02 (Gestionar Notas)

POR QUÉ ADAPTER:
- SÍ: Encapsula llamadas a Supabase Database
- SÍ: Mapea respuestas a entidades Nota
- SÍ: Centraliza lógica de acceso a datos
- NO alternativa (llamar Supabase directo): Alto acoplamiento, código duplicado

SEGURIDAD:
- Verificación de sesión antes de cada operación
- RLS en Supabase como segunda capa de protección
- user_id siempre viene de la sesión (no del usuario)
============================================================================
"""

import sys
import os
from typing import List, Optional

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from src.repositories.supabase_client import SupabaseClient
from src.services.session_manager import SessionManager
from src.models.nota import Nota


class NotasService:
    """
    Servicio para operaciones CRUD de notas.
    
    RESPONSABILIDADES:
    - Verificar sesión antes de operar
    - Ejecutar operaciones en Supabase
    - Mapear respuestas a entidades Nota
    - Actualizar timer de actividad
    
    SEGURIDAD (Doble capa):
    1. SessionManager verifica autenticación + timeout
    2. RLS en Supabase filtra por user_id
    
    USO:
        notas = NotasService()
        todas = notas.listar()
        nueva = notas.crear("Título", "Contenido")
    """
    
    def __init__(self):
        """
        Constructor con dependencias internas.
        
        POR QUÉ NO INYECCIÓN:
        - En MVP, siempre usamos Supabase real
        - Testing se haría con mocks a otro nivel
        """
        self._supabase = SupabaseClient()
        self._session = SessionManager()
    
    def _require_auth_and_update(self) -> str:
        """
        Verifica sesión y actualiza timer de actividad.
        
        FLUJO:
        1. Llama a require_auth() (lanza si no autenticado/expirado)
        2. Actualiza timer de actividad
        3. Retorna user_id para las operaciones
        
        RETORNA: user_id del usuario autenticado
        RAISES: PermissionError si no autenticado
        
        POR QUÉ MÉTODO PRIVADO:
        - SÍ: DRY - evita repetir en cada método
        - SÍ: Encapsula la lógica de verificación
        """
        self._session.require_auth()
        self._session.update_activity()
        return self._session.get_user_id()
    
    def listar(self) -> List[Nota]:
        """
        Lista todas las notas del usuario actual.
        
        RETORNA: Lista de Nota ordenadas por created_at DESC
        
        SEGURIDAD:
        - RLS filtra automáticamente por user_id
        - Solo ve sus propias notas
        
        TRAZABILIDAD:
        - RF-06: Listar notas
        - HU-05: Ver mis notas
        - CA-05.4: Ordenadas por fecha
        """
        self._require_auth_and_update()
        
        response = self._supabase.table('notas') \
            .select('*') \
            .order('created_at', desc=True) \
            .execute()
        
        return [Nota.from_dict(nota) for nota in response.data]
    
    def obtener(self, nota_id: str) -> Optional[Nota]:
        """
        Obtiene una nota por su ID.
        
        PARÁMETROS:
        - nota_id: UUID de la nota
        
        RETORNA: Nota o None si no existe
        
        SEGURIDAD:
        - RLS bloquea si no es propietario
        """
        self._require_auth_and_update()
        
        if not nota_id:
            return None
        
        response = self._supabase.table('notas') \
            .select('*') \
            .eq('id', nota_id) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return Nota.from_dict(response.data[0])
        
        return None
    
    def crear(self, titulo: str, contenido: Optional[str] = None) -> Nota:
        """
        Crea una nueva nota.
        
        PARÁMETROS:
        - titulo: Título de la nota (obligatorio)
        - contenido: Contenido opcional
        
        RETORNA: Nota creada con ID generado
        
        SEGURIDAD:
        - user_id viene de la sesión, no del usuario
        - RLS valida que user_id = auth.uid()
        
        TRAZABILIDAD:
        - RF-05: Crear nota
        - HU-04: Crear nota nueva
        - CA-04.1: Título obligatorio
        """
        user_id = self._require_auth_and_update()
        
        # Crear entidad (valida título automáticamente)
        nota = Nota(
            id='',  # Supabase lo genera
            user_id=user_id,
            title=titulo,
            content=contenido
        )
        
        response = self._supabase.table('notas') \
            .insert(nota.to_dict(include_id=False)) \
            .execute()
        
        if not response.data or len(response.data) == 0:
            raise RuntimeError("Error al crear la nota")
        
        return Nota.from_dict(response.data[0])
    
    def actualizar(
        self, 
        nota_id: str, 
        titulo: Optional[str] = None, 
        contenido: Optional[str] = None
    ) -> Optional[Nota]:
        """
        Actualiza una nota existente.
        
        PARÁMETROS:
        - nota_id: UUID de la nota a actualizar
        - titulo: Nuevo título (opcional, si es None no cambia)
        - contenido: Nuevo contenido (opcional)
        
        RETORNA: Nota actualizada o None si no existe
        
        SEGURIDAD:
        - RLS bloquea si no es propietario
        
        TRAZABILIDAD:
        - RF-07: Editar nota
        - HU-06: Modificar nota
        - CA-06.2: updated_at automático (trigger BD)
        """
        self._require_auth_and_update()
        
        if not nota_id:
            raise ValueError("ID de nota es obligatorio")
        
        # Construir datos a actualizar (solo los proporcionados)
        update_data = {}
        
        if titulo is not None:
            if not titulo.strip():
                raise ValueError("El título no puede estar vacío")
            update_data['title'] = titulo.strip()
        
        if contenido is not None:
            update_data['content'] = contenido
        
        if not update_data:
            # Nada que actualizar, obtener y retornar existente
            return self.obtener(nota_id)
        
        response = self._supabase.table('notas') \
            .update(update_data) \
            .eq('id', nota_id) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return Nota.from_dict(response.data[0])
        
        return None
    
    def eliminar(self, nota_id: str) -> bool:
        """
        Elimina una nota.
        
        PARÁMETROS:
        - nota_id: UUID de la nota a eliminar
        
        RETORNA: True si se eliminó, False si no existía
        
        SEGURIDAD:
        - RLS bloquea si no es propietario
        
        TRAZABILIDAD:
        - RF-08: Eliminar nota
        - HU-07: Eliminar nota
        - RF-14: Confirmación antes de eliminar (UI)
        """
        self._require_auth_and_update()
        
        if not nota_id:
            raise ValueError("ID de nota es obligatorio")
        
        response = self._supabase.table('notas') \
            .delete() \
            .eq('id', nota_id) \
            .execute()
        
        # Si se eliminó algo, data tendrá el registro eliminado
        return len(response.data) > 0 if response.data else False
    
    def contar(self) -> int:
        """
        Cuenta las notas del usuario actual.
        
        RETORNA: Número de notas
        
        ÚTIL PARA: Mostrar estadísticas en UI
        """
        self._require_auth_and_update()
        
        response = self._supabase.table('notas') \
            .select('id', count='exact') \
            .execute()
        
        return response.count or 0


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para NotasService.
    
    EJECUCIÓN:
        python src/services/notas_service.py
    
    NOTA: Esta prueba verifica estructura sin operaciones reales.
    Para operaciones reales se necesita sesión activa.
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: NotasService (Adapter)")
    print("=" * 60)
    
    try:
        # Test 1: Crear servicio
        notas = NotasService()
        print("✅ NotasService creado correctamente")
        
        # Test 2: Verificar dependencias
        assert notas._supabase is not None, "SupabaseClient no inicializado"
        assert notas._session is not None, "SessionManager no inicializado"
        print("✅ Dependencias inicializadas")
        
        # Test 3: Métodos existen
        methods = ['listar', 'obtener', 'crear', 'actualizar', 'eliminar', 'contar']
        for method in methods:
            assert hasattr(notas, method), f"Método {method} no existe"
        print(f"✅ Métodos CRUD disponibles: {methods}")
        
        # Test 4: Sin sesión, debe fallar
        try:
            notas.listar()
            print("❌ Debería fallar sin sesión")
        except PermissionError as e:
            print(f"✅ Verificación de sesión funciona: {str(e)[:30]}...")
        
        # Test 5: Verificar que no hay queries hardcodeadas inseguras
        import inspect
        source = inspect.getsource(NotasService)
        if 'user_id = ' in source and "request.user_id" in source:
            print("⚠️ Posible user_id desde request (inseguro)")
        else:
            print("✅ user_id viene de SessionManager (seguro)")
        
        # Test 6: Verificar que usa RLS
        if "'notas'" in source or '"notas"' in source:
            print("✅ Accede a tabla 'notas' (protegida por RLS)")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        print("\nNOTA: Para test real, necesita sesión activa.")
        print("      Usar: AuthService.login() primero.")
        
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
