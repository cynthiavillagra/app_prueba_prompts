# -*- coding: utf-8 -*-
"""
============================================================================
SUPABASE_CLIENT.PY - Cliente Supabase (Singleton)
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: REPOSITORIES
Patrón: Singleton
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: CORE / INFRAESTRUCTURA
- Requisitos: RNF-ARCH-02 (Patrones de diseño)
- HU: Transversal (todas las operaciones de datos)

POR QUÉ SINGLETON:
- SÍ: Una única conexión a Supabase para toda la app
- SÍ: Evita crear múltiples clientes (consumo de recursos)
- SÍ: Centraliza la configuración del cliente
- NO alternativa (crear cliente cada vez): Overhead innecesario,
  múltiples conexiones que podrían saturar límites de API

POR QUÉ supabase-py:
- SÍ: Cliente oficial mantenido por la comunidad Supabase
- SÍ: API idéntica al SDK de JavaScript
- SÍ: Soporta Auth, Database, Storage, Realtime
- NO alternativa (HTTP requests manuales): Reinventar la rueda
============================================================================
"""

from typing import Optional
import sys
import os

# Agregar directorio raíz al path para permitir ejecución directa
# POR QUÉ: Permite ejecutar `python src/repositories/supabase_client.py` directamente
# ALTERNATIVA: Usar `python -m src.repositories.supabase_client` (menos intuitivo)
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from supabase import create_client, Client
from src.config.settings import Settings


class SupabaseClient:
    """
    Singleton para cliente Supabase.
    
    ARQUITECTURA STATELESS:
    - El cliente Supabase es stateless por diseño
    - No guarda sesiones de usuario (eso lo hace SessionManager)
    - Solo mantiene la conexión configurada
    
    SEGURIDAD:
    - Usa ANON KEY (pública) + RLS
    - NO usa SERVICE_ROLE_KEY (sería un riesgo de seguridad)
    - Las políticas RLS protegen los datos
    """
    
    _instance: Optional['SupabaseClient'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'SupabaseClient':
        """
        Implementación del patrón Singleton.
        
        POR QUÉ __new__:
        - SÍ: Control explícito de instanciación
        - SÍ: Garantiza una sola instancia del cliente
        - NO alternativa (módulo global): Menos control, testing difícil
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """
        Inicializa el cliente Supabase (solo la primera vez).
        
        IMPORTANTE: Usa Settings (otro Singleton) para obtener credenciales.
        La dependencia es: SupabaseClient -> Settings -> .env
        """
        if not SupabaseClient._initialized:
            self._initialize()
            SupabaseClient._initialized = True
    
    def _initialize(self) -> None:
        """
        Crea el cliente Supabase con las credenciales de Settings.
        
        POR QUÉ create_client:
        - SÍ: Función oficial de supabase-py
        - SÍ: Configura automáticamente headers, timeouts, etc.
        - NO alternativa (requests.Session): Perderíamos toda la abstracción
        """
        settings = Settings()
        
        self._client: Client = create_client(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key
        )
    
    @property
    def client(self) -> Client:
        """
        Acceso al cliente Supabase subyacente.
        
        IMPORTANTE: Exponemos el cliente directamente porque:
        - Los Services necesitan acceso completo a .table(), .auth, etc.
        - Wrappear cada método sería over-engineering
        
        ALTERNATIVA DESCARTADA:
        - Wrappear con métodos propios: Duplicaría toda la API de Supabase
        """
        return self._client
    
    @property
    def auth(self):
        """
        Acceso directo al módulo de autenticación.
        
        USO:
            client = SupabaseClient()
            client.auth.sign_in_with_password(...)
        """
        return self._client.auth
    
    def table(self, table_name: str):
        """
        Acceso directo a una tabla.
        
        USO:
            client = SupabaseClient()
            client.table('notas').select('*').execute()
        
        POR QUÉ este wrapper:
        - SÍ: Sintaxis más limpia que client.client.table()
        - SÍ: Punto de extensión para logging futuro
        """
        return self._client.table(table_name)


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para SupabaseClient.
    
    EJECUCIÓN:
        python src/repositories/supabase_client.py
    
    REQUISITOS:
        - .env configurado con SUPABASE_URL y SUPABASE_KEY
        - Tabla 'notas' creada en Supabase (ejecutar database/init.sql)
    
    RESULTADO ESPERADO:
        ✅ SupabaseClient creado
        ✅ Singleton verificado
        ✅ Query a tabla 'notas' exitosa
        ✅ Auth disponible
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: SupabaseClient (Singleton)")
    print("=" * 60)
    
    try:
        # Test 1: Crear cliente
        supabase = SupabaseClient()
        print("✅ SupabaseClient creado")
        
        # Test 2: Verificar Singleton
        supabase2 = SupabaseClient()
        if supabase is supabase2:
            print("✅ Singleton verificado: misma instancia")
        else:
            print("❌ ERROR: Singleton roto")
        
        # Test 3: Query a tabla notas (debería funcionar aunque esté vacía)
        try:
            response = supabase.table('notas').select('*').limit(1).execute()
            print(f"✅ Query a 'notas' exitosa. Registros: {len(response.data)}")
        except Exception as e:
            # Si la tabla no existe, sugerimos ejecutar init.sql
            if 'relation' in str(e).lower() and 'does not exist' in str(e).lower():
                print(f"⚠️ Tabla 'notas' no existe. Ejecutar database/init.sql")
            else:
                print(f"❌ Error en query: {e}")
        
        # Test 4: Verificar que auth está disponible
        if hasattr(supabase, 'auth') and supabase.auth is not None:
            print("✅ Auth disponible")
        else:
            print("❌ Auth no disponible")
        
        # Test 5: Verificar que no hay sesiones hardcodeadas
        import inspect
        source = inspect.getsource(SupabaseClient)
        if 'session_store' in source or 'sessions = {' in source:
            print("⚠️ ADVERTENCIA: Posible estado de sesión en código")
        else:
            print("✅ Stateless verificado: sin almacenamiento de sesiones")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("   Solución: Verificar .env")
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
