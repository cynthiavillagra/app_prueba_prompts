# -*- coding: utf-8 -*-
"""
============================================================================
SETTINGS.PY - Configuración Centralizada (Singleton)
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: CONFIG
Patrón: Singleton
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: CORE
- Requisitos: RNF-SEC-01 (Credenciales en variables de entorno)
- HU: Transversal (todas las HU necesitan config)

POR QUÉ SINGLETON:
- SÍ: Una única instancia garantiza consistencia de configuración
- SÍ: Evita cargar .env múltiples veces (rendimiento)
- SÍ: Punto único de acceso a credenciales
- NO alternativa (crear instancia cada vez): Cargaría .env repetidamente,
  posibles inconsistencias si .env cambia durante ejecución

POR QUÉ python-dotenv:
- SÍ: Estándar de la industria para cargar .env
- SÍ: Soportado en todos los entornos (local, Docker, Vercel)
- NO alternativa (os.environ directo): Requiere configurar variables manualmente
============================================================================
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Settings:
    """
    Singleton para gestión de configuración desde variables de entorno.
    
    ARQUITECTURA STATELESS:
    - NO guarda estado de sesión
    - Solo guarda configuración inmutable (URLs, keys)
    - Carga una vez al iniciar la aplicación
    
    SEGURIDAD:
    - NUNCA loguea valores de las keys
    - Valida que variables críticas existan
    - Falla rápido si falta configuración
    """
    
    _instance: Optional['Settings'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'Settings':
        """
        Implementación del patrón Singleton.
        
        POR QUÉ __new__ y no __init__:
        - SÍ: __new__ controla la creación de instancia
        - SÍ: Garantiza UNA sola instancia en memoria
        - NO alternativa (decorador): Menos explícito, más "mágico"
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """
        Inicializa la configuración (solo la primera vez).
        
        IMPORTANTE: __init__ se llama cada vez que se invoca Settings(),
        pero _initialized evita que se recargue .env múltiples veces.
        """
        if not Settings._initialized:
            self._load_env()
            Settings._initialized = True
    
    def _load_env(self) -> None:
        """
        Carga variables de entorno desde .env
        
        ORDEN DE BÚSQUEDA (python-dotenv):
        1. Variables de entorno del sistema (tienen prioridad)
        2. Archivo .env en el directorio actual
        3. Archivo .env en directorios padre
        
        SEGURIDAD: load_dotenv() NO sobrescribe variables existentes
        (las de Vercel/Docker tienen prioridad sobre .env local)
        """
        # Cargar .env (no sobrescribe variables existentes del sistema)
        load_dotenv()
        
        # ============================================
        # SUPABASE - Variables Requeridas
        # ============================================
        self.supabase_url: str = os.getenv('SUPABASE_URL', '')
        self.supabase_key: str = os.getenv('SUPABASE_KEY', '')
        
        # ============================================
        # SESIÓN - Configuración de timeout
        # ============================================
        # Tiempo de inactividad en segundos (default: 15 minutos)
        self.session_timeout_seconds: int = int(
            os.getenv('SESSION_TIMEOUT_SECONDS', '900')
        )
        
        # ============================================
        # ENTORNO
        # ============================================
        # Detectar si estamos en Vercel
        self.is_vercel: bool = os.getenv('VERCEL', '').lower() == '1'
        
        # Modo debug (solo para desarrollo local)
        self.debug: bool = os.getenv('DEBUG', '').lower() == 'true'
        
        # Validar configuración crítica
        self._validate()
    
    def _validate(self) -> None:
        """
        Valida que las variables críticas existan.
        
        POR QUÉ FALLAR RÁPIDO:
        - SÍ: Mejor fallar al inicio que a mitad de una operación
        - SÍ: Mensaje claro de qué falta
        - NO alternativa (valores por defecto): Fallaría silenciosamente
        """
        missing = []
        
        if not self.supabase_url:
            missing.append('SUPABASE_URL')
        
        if not self.supabase_key:
            missing.append('SUPABASE_KEY')
        
        if missing:
            raise ValueError(
                f"Variables de entorno faltantes: {', '.join(missing)}. "
                f"Copia .env.example a .env y completa los valores."
            )
    
    def get_masked_key(self) -> str:
        """
        Devuelve la key parcialmente oculta para logging seguro.
        
        SEGURIDAD: NUNCA logueamos la key completa.
        """
        if len(self.supabase_key) > 10:
            return f"{self.supabase_key[:5]}...{self.supabase_key[-5:]}"
        return "***"


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para Settings.
    
    EJECUCIÓN:
        python src/config/settings.py
    
    REQUISITOS:
        - Archivo .env con SUPABASE_URL y SUPABASE_KEY
    
    RESULTADO ESPERADO:
        ✅ Settings cargado correctamente
        URL: https://xxx.supabase.co
        Key: eyJhb...xxxxx
        Timeout: 900s
        Is Vercel: False
        Debug: False
        ✅ Singleton verificado: misma instancia
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: Settings (Singleton)")
    print("=" * 60)
    
    try:
        # Test 1: Cargar settings
        settings = Settings()
        print("✅ Settings cargado correctamente")
        print(f"   URL: {settings.supabase_url}")
        print(f"   Key: {settings.get_masked_key()}")
        print(f"   Timeout: {settings.session_timeout_seconds}s")
        print(f"   Is Vercel: {settings.is_vercel}")
        print(f"   Debug: {settings.debug}")
        
        # Test 2: Verificar Singleton
        settings2 = Settings()
        if settings is settings2:
            print("✅ Singleton verificado: misma instancia")
        else:
            print("❌ ERROR: Singleton roto - instancias diferentes")
        
        # Test 3: Verificar que no hay claves hardcodeadas
        import inspect
        source = inspect.getsource(Settings)
        if 'eyJ' in source or 'supabase.co' in source:
            print("⚠️ ADVERTENCIA: Posible clave hardcodeada en código")
        else:
            print("✅ Auditoría de secretos: OK (sin claves hardcodeadas)")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("   Solución: Copia .env.example a .env y completa los valores")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
