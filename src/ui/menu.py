# -*- coding: utf-8 -*-
"""
============================================================================
MENU.PY - Interfaz de Línea de Comandos (CLI)
============================================================================
Proyecto: CRUD Didáctico con Supabase
Módulo: UI
Fecha: 2025-12-24

TRAZABILIDAD:
- Módulo: UI
- Requisitos: RF-10 a RF-14 (Interfaz)
- HU: Todas (interfaz de interacción)

POR QUÉ CLI:
- SÍ: Didáctico - enfoque en lógica sin complejidad de UI web
- SÍ: Python puro - sin frameworks
- SÍ: Portable - funciona en cualquier terminal
- NO alternativa (web): Requeriría framework (Flask, etc.)
============================================================================
"""

import sys
import os

# Agregar directorio raíz al path para permitir ejecución directa
_root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from src.services.auth_service import AuthService
from src.services.notas_service import NotasService
from src.services.session_manager import SessionManager


class Menu:
    """
    Menú interactivo CLI para el CRUD de notas.
    
    RESPONSABILIDADES:
    - Mostrar opciones al usuario
    - Capturar input
    - Coordinar llamadas a Services
    - Mostrar resultados y errores
    
    FLUJO:
    1. Mostrar menú de login/registro
    2. Después de login, mostrar menú de notas
    3. Manejar errores de sesión expirada
    """
    
    def __init__(self):
        """Inicializa los servicios."""
        self._auth = AuthService()
        self._notas = NotasService()
        self._session = SessionManager()
    
    def run(self) -> None:
        """
        Punto de entrada principal del menú.
        
        BUCLE:
        1. Si no autenticado → menú de auth
        2. Si autenticado → menú de notas
        3. Manejar excepciones de sesión
        """
        self._print_header()
        
        while True:
            try:
                if self._auth.is_authenticated():
                    self._menu_notas()
                else:
                    if not self._menu_auth():
                        break  # Usuario eligió salir
                        
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta pronto!")
                break
            except PermissionError as e:
                # Sesión expirada u otro error de permisos
                print(f"\n⚠️ {e}")
                print("Redirigiendo al login...\n")
    
    def _print_header(self) -> None:
        """Muestra el encabezado de la aplicación."""
        print("\n" + "=" * 50)
        print("   📝 CRUD DIDÁCTICO DE NOTAS")
        print("   Proyecto con Supabase + Python POO")
        print("=" * 50)
    
    # ========================================================================
    # MENÚ DE AUTENTICACIÓN
    # ========================================================================
    
    def _menu_auth(self) -> bool:
        """
        Menú de autenticación (login/registro).
        
        RETORNA: True para continuar, False para salir
        """
        print("\n--- MENÚ DE AUTENTICACIÓN ---")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            self._login()
        elif opcion == "2":
            self._registro()
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto!")
            return False
        else:
            print("\n❌ Opción no válida")
        
        return True
    
    def _login(self) -> None:
        """Flujo de login."""
        print("\n--- INICIAR SESIÓN ---")
        
        email = input("Email: ").strip()
        password = input("Contraseña: ").strip()
        
        if not email or not password:
            print("\n❌ Email y contraseña son obligatorios")
            return
        
        try:
            user = self._auth.login(email, password)
            print(f"\n✅ ¡Bienvenido/a, {user.email}!")
            print(f"   Sesión válida por 15 minutos de inactividad")
        except ValueError as e:
            print(f"\n❌ Error de validación: {e}")
        except PermissionError as e:
            print(f"\n❌ Error de autenticación: {e}")
    
    def _registro(self) -> None:
        """Flujo de registro."""
        print("\n--- REGISTRO DE USUARIO ---")
        
        email = input("Email: ").strip()
        password = input("Contraseña (mín. 6 caracteres): ").strip()
        password_confirm = input("Confirmar contraseña: ").strip()
        
        if password != password_confirm:
            print("\n❌ Las contraseñas no coinciden")
            return
        
        try:
            user = self._auth.register(email, password)
            print(f"\n✅ Usuario registrado: {user.email}")
            print("   Ahora puede iniciar sesión")
        except ValueError as e:
            print(f"\n❌ Error de validación: {e}")
        except PermissionError as e:
            print(f"\n❌ Error de registro: {e}")
    
    # ========================================================================
    # MENÚ DE NOTAS
    # ========================================================================
    
    def _menu_notas(self) -> None:
        """
        Menú principal de notas (requiere autenticación).
        
        OPCIONES:
        1. Listar notas
        2. Crear nota
        3. Editar nota
        4. Eliminar nota
        5. Cerrar sesión
        """
        user = self._auth.get_current_user()
        remaining = self._session.get_remaining_time()
        
        print(f"\n--- MENÚ DE NOTAS ---")
        print(f"Usuario: {user.email} | Sesión: {remaining // 60}:{remaining % 60:02d} restantes")
        print("-" * 40)
        print("1. 📋 Listar notas")
        print("2. ➕ Crear nota")
        print("3. ✏️  Editar nota")
        print("4. 🗑️  Eliminar nota")
        print("5. 🚪 Cerrar sesión")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            self._listar_notas()
        elif opcion == "2":
            self._crear_nota()
        elif opcion == "3":
            self._editar_nota()
        elif opcion == "4":
            self._eliminar_nota()
        elif opcion == "5":
            self._logout()
        else:
            print("\n❌ Opción no válida")
    
    def _listar_notas(self) -> None:
        """Lista todas las notas del usuario."""
        print("\n--- MIS NOTAS ---")
        
        try:
            notas = self._notas.listar()
            
            if not notas:
                print("(No tienes notas todavía)")
                return
            
            for i, nota in enumerate(notas, 1):
                print(f"\n{i}. {nota.title}")
                print(f"   ID: {nota.id[:8]}...")
                print(f"   {nota.get_preview(60)}")
                print(f"   📅 {nota.to_display_dict()['created_at']}")
            
            print(f"\nTotal: {len(notas)} nota(s)")
            
        except PermissionError as e:
            raise e  # Re-lanzar para manejo en run()
        except Exception as e:
            print(f"\n❌ Error al listar: {e}")
    
    def _crear_nota(self) -> None:
        """Crea una nueva nota."""
        print("\n--- CREAR NOTA ---")
        
        titulo = input("Título: ").strip()
        if not titulo:
            print("\n❌ El título es obligatorio")
            return
        
        print("Contenido (Enter vacío para terminar):")
        lineas = []
        while True:
            linea = input()
            if linea == "":
                break
            lineas.append(linea)
        
        contenido = "\n".join(lineas) if lineas else None
        
        try:
            nota = self._notas.crear(titulo, contenido)
            print(f"\n✅ Nota creada: {nota}")
        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except PermissionError as e:
            raise e
        except Exception as e:
            print(f"\n❌ Error al crear: {e}")
    
    def _editar_nota(self) -> None:
        """Edita una nota existente."""
        print("\n--- EDITAR NOTA ---")
        
        # Primero listar para que el usuario vea los IDs
        self._listar_notas()
        
        nota_id = input("\nIngrese ID de la nota (primeros 8 caracteres): ").strip()
        if not nota_id:
            print("\n❌ ID es obligatorio")
            return
        
        try:
            # Buscar nota que coincida con el prefijo
            notas = self._notas.listar()
            nota_encontrada = None
            for nota in notas:
                if nota.id.startswith(nota_id):
                    nota_encontrada = nota
                    break
            
            if not nota_encontrada:
                print("\n❌ Nota no encontrada")
                return
            
            print(f"\nEditando: {nota_encontrada.title}")
            print(f"Contenido actual: {nota_encontrada.get_preview(100)}")
            
            nuevo_titulo = input("Nuevo título (Enter para mantener): ").strip()
            print("Nuevo contenido (Enter vacío para mantener):")
            
            lineas = []
            primera_linea = input()
            if primera_linea:
                lineas.append(primera_linea)
                while True:
                    linea = input()
                    if linea == "":
                        break
                    lineas.append(linea)
            
            nuevo_contenido = "\n".join(lineas) if lineas else None
            
            # Actualizar solo si hay cambios
            if nuevo_titulo or nuevo_contenido is not None:
                nota_actualizada = self._notas.actualizar(
                    nota_encontrada.id,
                    titulo=nuevo_titulo if nuevo_titulo else None,
                    contenido=nuevo_contenido
                )
                print(f"\n✅ Nota actualizada: {nota_actualizada}")
            else:
                print("\nSin cambios.")
                
        except PermissionError as e:
            raise e
        except Exception as e:
            print(f"\n❌ Error al editar: {e}")
    
    def _eliminar_nota(self) -> None:
        """Elimina una nota (con confirmación)."""
        print("\n--- ELIMINAR NOTA ---")
        
        # Primero listar
        self._listar_notas()
        
        nota_id = input("\nIngrese ID de la nota a eliminar: ").strip()
        if not nota_id:
            print("\n❌ ID es obligatorio")
            return
        
        try:
            # Buscar nota
            notas = self._notas.listar()
            nota_encontrada = None
            for nota in notas:
                if nota.id.startswith(nota_id):
                    nota_encontrada = nota
                    break
            
            if not nota_encontrada:
                print("\n❌ Nota no encontrada")
                return
            
            # Confirmación (RF-14)
            print(f"\n⚠️ ¿Eliminar '{nota_encontrada.title}'?")
            confirma = input("Escriba 'SI' para confirmar: ").strip().upper()
            
            if confirma != "SI":
                print("\nOperación cancelada.")
                return
            
            eliminada = self._notas.eliminar(nota_encontrada.id)
            
            if eliminada:
                print(f"\n✅ Nota eliminada correctamente")
            else:
                print(f"\n❌ No se pudo eliminar la nota")
                
        except PermissionError as e:
            raise e
        except Exception as e:
            print(f"\n❌ Error al eliminar: {e}")
    
    def _logout(self) -> None:
        """Cierra la sesión."""
        self._auth.logout()
        print("\n✅ Sesión cerrada correctamente")
        print("👋 ¡Hasta pronto!")


# ============================================================================
# PRUEBA ATÓMICA - Bloque obligatorio
# ============================================================================
if __name__ == "__main__":
    """
    Prueba de fuego para Menu.
    
    EJECUCIÓN:
        python src/ui/menu.py
    
    NOTA: Esta prueba verifica que el menú se puede crear.
    Para uso real, ejecutar main.py
    """
    print("=" * 60)
    print("PRUEBA DE FUEGO: Menu (CLI)")
    print("=" * 60)
    
    try:
        # Test 1: Crear menú
        menu = Menu()
        print("✅ Menu creado correctamente")
        
        # Test 2: Verificar servicios
        assert menu._auth is not None, "AuthService no inicializado"
        assert menu._notas is not None, "NotasService no inicializado"
        assert menu._session is not None, "SessionManager no inicializado"
        print("✅ Servicios inicializados")
        
        # Test 3: Verificar métodos existen
        methods = ['run', '_menu_auth', '_menu_notas', '_login', '_registro',
                   '_listar_notas', '_crear_nota', '_editar_nota', '_eliminar_nota', '_logout']
        for method in methods:
            assert hasattr(menu, method), f"Método {method} no existe"
        print(f"✅ Métodos de menú disponibles")
        
        # Test 4: Verificar estado inicial (no autenticado)
        assert not menu._auth.is_authenticated(), "No debería estar autenticado"
        print("✅ Estado inicial: no autenticado")
        
        print("=" * 60)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("=" * 60)
        print("\nPara usar el menú completo, ejecutar:")
        print("   python main.py")
        
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
