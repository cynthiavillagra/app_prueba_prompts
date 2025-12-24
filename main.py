# -*- coding: utf-8 -*-
"""
============================================================================
MAIN.PY - Entry Point para ejecución local
============================================================================
Proyecto: CRUD Didáctico con Supabase
Tipo: Entry Point / Adaptador de Infraestructura
Fecha: 2025-12-24

EJECUCIÓN:
    python main.py

POR QUÉ ENTRY POINT SEPARADO:
- SÍ: Separa configuración de lógica
- SÍ: load_dotenv() AL PRINCIPIO (antes de cualquier import)
- SÍ: Permite diferentes entry points (local vs Vercel)
- NO alternativa (todo en menu.py): Mezcla responsabilidades

ARQUITECTURA:
- main.py: Entry point local (CLI)
- api/index.py: Entry point Vercel (API)
============================================================================
"""

# ============================================================================
# IMPORTANTE: load_dotenv() DEBE ir ANTES de cualquier import de src/
# Esto garantiza que las variables de entorno estén disponibles
# cuando Settings (Singleton) se inicialice
# ============================================================================
from dotenv import load_dotenv
load_dotenv()  # Cargar ANTES de imports

import sys
import os

# Agregar directorio actual al path si no está
# (necesario para imports relativos cuando se ejecuta directamente)
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

# Ahora sí, importar la aplicación
from src.ui.menu import Menu


def main() -> None:
    """
    Función principal que inicia la aplicación CLI.
    
    RESPONSABILIDADES:
    - Iniciar el menú interactivo
    - Manejar errores fatales
    - Mostrar mensajes de despedida
    """
    try:
        menu = Menu()
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación interrumpida por el usuario.")
        sys.exit(0)
        
    except ValueError as e:
        # Errores de configuración (ej: variables de entorno faltantes)
        print(f"\n❌ Error de configuración: {e}")
        print("\nVerifique:")
        print("  1. Que existe el archivo .env")
        print("  2. Que SUPABASE_URL y SUPABASE_KEY están configurados")
        print("  3. Consulte docs/04_a_setup_local.md")
        sys.exit(1)
        
    except Exception as e:
        # Errores inesperados
        print(f"\n❌ Error inesperado: {type(e).__name__}")
        print(f"   Detalle: {e}")
        print("\nSi el problema persiste, consulte docs/CHECKPOINT.md")
        sys.exit(1)


# ============================================================================
# BLOQUE OBLIGATORIO: if __name__ == "__main__"
# ============================================================================
if __name__ == "__main__":
    """
    Punto de entrada cuando se ejecuta directamente.
    
    EJECUCIÓN:
        python main.py
    
    Este bloque garantiza que main() solo se ejecute
    cuando el archivo se ejecuta directamente, no cuando
    se importa como módulo.
    
    POR QUÉ:
    - SÍ: Estándar de Python para entry points
    - SÍ: Permite importar main() desde tests
    - NO alternativa (ejecutar sin check): Se ejecutaría al importar
    """
    main()
