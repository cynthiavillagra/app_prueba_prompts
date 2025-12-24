# 📘 Manual Técnico: menu.py

> **Archivo:** `src/ui/menu.py`  
> **Tipo:** CLI Controller  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `menu.py` implementa la interfaz de línea de comandos (CLI) que permite al usuario interactuar con el sistema de notas.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | UI |
| **Requisitos** | RF-10 a RF-14 |
| **Historia de Usuario** | Todas (punto de interacción) |
| **Criterio de Aceptación** | Menú intuitivo, feedback claro |
| **Caso de Uso** | CU-01, CU-02 |
| **Escenario** | Login, Registro, CRUD completo |

---

## 2. Estrategia de Construcción

### Flujo de Menús

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE MENÚS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   INICIO                                                    │
│     │                                                       │
│     ▼                                                       │
│   ┌─────────────────┐                                       │
│   │ MENÚ AUTH       │                                       │
│   │ 1. Login        │──────────────────┐                    │
│   │ 2. Registro     │                  │                    │
│   │ 0. Salir        │                  │                    │
│   └────────┬────────┘                  │                    │
│            │                           │                    │
│            │ Login exitoso             │                    │
│            ▼                           │                    │
│   ┌─────────────────┐                  │                    │
│   │ MENÚ NOTAS      │                  │                    │
│   │ 1. Listar       │                  │                    │
│   │ 2. Crear        │                  │                    │
│   │ 3. Editar       │◄─────────────────┤                    │
│   │ 4. Eliminar     │  Sesión expirada │                    │
│   │ 5. Logout       │──────────────────┘                    │
│   └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Aclaración Metodológica

### 3.1 Manejo de Sesión Expirada

```python
# En run():
try:
    if self._auth.is_authenticated():
        self._menu_notas()  # Puede lanzar PermissionError
except PermissionError as e:
    print(f"⚠️ {e}")
    print("Redirigiendo al login...")
    # Vuelve al bucle → muestra menú auth
```

### 3.2 Confirmación de Eliminación (RF-14)

```python
# En _eliminar_nota():
print(f"⚠️ ¿Eliminar '{nota.title}'?")
confirma = input("Escriba 'SI' para confirmar: ").upper()
if confirma != "SI":
    print("Operación cancelada.")
    return
```

---

## 4. Código Fuente

### Ubicación

```
src/
└── ui/
    ├── __init__.py
    └── menu.py    ◄── Este archivo
```

### Métodos

| Método | Visibilidad | Descripción |
|--------|-------------|-------------|
| `run()` | público | Bucle principal |
| `_menu_auth()` | privado | Menú login/registro |
| `_menu_notas()` | privado | Menú CRUD |
| `_login()` | privado | Flujo de login |
| `_registro()` | privado | Flujo de registro |
| `_listar_notas()` | privado | Mostrar notas |
| `_crear_nota()` | privado | Crear nota |
| `_editar_nota()` | privado | Editar nota |
| `_eliminar_nota()` | privado | Eliminar con confirmación |
| `_logout()` | privado | Cerrar sesión |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/ui/menu.py
```

### 5.2 Resultado Esperado

```
============================================================
PRUEBA DE FUEGO: Menu (CLI)
============================================================
✅ Menu creado correctamente
✅ Servicios inicializados
✅ Métodos de menú disponibles
✅ Estado inicial: no autenticado
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================

Para usar el menú completo, ejecutar:
   python main.py
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| CLI puro | Sin dependencias externas |
| Bucle while True | Mantiene la app corriendo |
| Métodos privados `_` | Encapsulación |
| KeyboardInterrupt | Ctrl+C graceful |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Framework web (Flask) | Requisito: sin frameworks |
| Librería CLI (click) | Dependencia extra |
| Menú gráfico (tkinter) | Fuera de alcance |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| KeyboardInterrupt | Ctrl+C | Comportamiento esperado |
| PermissionError en operación | Sesión expirada | Re-login automático |
| Nota no encontrada | ID incorrecto | Verificar ID |

### 7.2 Requisitos Cubiertos

| RF | Descripción | Método |
|----|-------------|--------|
| RF-10 | Validación de inputs | En cada método |
| RF-11 | Estados de carga | Mensajes "Creando..." |
| RF-12 | Mensajes de feedback | ✅ / ❌ / ⚠️ |
| RF-13 | Interfaz clara | Menús numerados |
| RF-14 | Confirmación eliminación | `_eliminar_nota()` |

---

## 8. Uso

### Ejecución completa

```powershell
# Desde raíz del proyecto
python main.py
```

### Ejemplo de sesión

```
==================================================
   📝 CRUD DIDÁCTICO DE NOTAS
   Proyecto con Supabase + Python POO
==================================================

--- MENÚ DE AUTENTICACIÓN ---
1. Iniciar sesión
2. Registrarse
0. Salir

Seleccione una opción: 1

--- INICIAR SESIÓN ---
Email: usuario@test.com
Contraseña: ********

✅ ¡Bienvenido/a, usuario@test.com!
   Sesión válida por 15 minutos de inactividad

--- MENÚ DE NOTAS ---
Usuario: usuario@test.com | Sesión: 14:59 restantes
----------------------------------------
1. 📋 Listar notas
2. ➕ Crear nota
...
```

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `main.py`
