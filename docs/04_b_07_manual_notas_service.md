# 📘 Manual Técnico: notas_service.py

> **Archivo:** `src/services/notas_service.py`  
> **Tipo:** Service Adapter (CRUD)  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `notas_service.py` implementa todas las operaciones CRUD sobre la entidad Nota, con verificación de sesión y timeout antes de cada operación.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | NOTAS |
| **Requisitos** | RF-05, RF-06, RF-07, RF-08, RF-09, RF-16, RF-17 |
| **Historia de Usuario** | HU-04, HU-05, HU-06, HU-07 |
| **Criterio de Aceptación** | CRUD completo + seguridad |
| **Caso de Uso** | CU-02 (Gestionar Notas) |
| **Escenario** | Crear, Listar, Ver, Editar, Eliminar |

---

## 2. Estrategia de Construcción

### Patrón Adapter + Seguridad Doble Capa

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE OPERACIÓN                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [1] UI llama NotasService.crear()                         │
│                    │                                        │
│                    ▼                                        │
│   [2] _require_auth_and_update()                            │
│        ├── SessionManager.require_auth()                    │
│        │    └── ¿Autenticado? ¿No expirado?                │
│        │         NO → PermissionError                       │
│        │         SÍ → continuar                             │
│        └── update_activity() → resetear timer               │
│                    │                                        │
│                    ▼                                        │
│   [3] Ejecutar operación en Supabase                        │
│                    │                                        │
│                    ▼                                        │
│   [4] RLS verifica user_id = auth.uid()                     │
│        NO → 403 Forbidden                                   │
│        SÍ → Operación exitosa                               │
│                    │                                        │
│                    ▼                                        │
│   [5] Mapear respuesta → Nota entity                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Aclaración Metodológica

### 3.1 Verificación Doble Capa

| Capa | Componente | Verificación |
|------|------------|--------------|
| 1 | SessionManager | ¿Hay sesión? ¿No expiró? |
| 2 | Supabase RLS | ¿user_id = auth.uid()? |

### 3.2 Rol del Bloque Main

La prueba atómica verifica:
- Servicio se crea correctamente
- Dependencias inicializadas
- Métodos CRUD existen
- Sin sesión, falla con PermissionError
- user_id viene de SessionManager (no del request)

---

## 4. Código Fuente

### Ubicación

```
src/
└── services/
    ├── __init__.py
    ├── session_manager.py
    ├── auth_service.py
    └── notas_service.py    ◄── Este archivo
```

### Métodos CRUD

| Método | Retorno | Descripción | RF |
|--------|---------|-------------|-----|
| `listar()` | List[Nota] | Todas las notas ordenadas | RF-06 |
| `obtener(id)` | Nota/None | Una nota por ID | RF-06 |
| `crear(titulo, contenido)` | Nota | Nueva nota | RF-05 |
| `actualizar(id, titulo, contenido)` | Nota/None | Modificar nota | RF-07 |
| `eliminar(id)` | bool | Eliminar nota | RF-08 |
| `contar()` | int | Total de notas | Estadísticas |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/services/notas_service.py
```

### 5.2 Resultado Esperado

```
============================================================
PRUEBA DE FUEGO: NotasService (Adapter)
============================================================
✅ NotasService creado correctamente
✅ Dependencias inicializadas
✅ Métodos CRUD disponibles: ['listar', 'obtener', 'crear', ...]
✅ Verificación de sesión funciona: No autenticado...
✅ user_id viene de SessionManager (seguro)
✅ Accede a tabla 'notas' (protegida por RLS)
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| `_require_auth_and_update()` | DRY - verificación centralizada |
| user_id de SessionManager | Seguridad - no confiar en input |
| Mapeo a Nota entity | Desacoplamiento de Supabase |
| RLS como segunda capa | Defense in depth |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Verificar sesión solo en UI | Inseguro, bypass posible |
| user_id del request | Fácil de falsificar |
| Retornar dicts crudos | Sin validación, sin tipos |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `PermissionError: No autenticado` | Sin login | Llamar a AuthService.login() |
| `PermissionError: Sesión expirada` | Timeout 15min | Re-login |
| `ValueError: título vacío` | Crear sin título | Proporcionar título |
| `None` en obtener/actualizar | Nota no existe o de otro user | Verificar ID |

### 7.2 Seguridad

| Check | Estado |
|-------|--------|
| Verifica sesión antes de operar | ✅ |
| user_id de SessionManager | ✅ |
| RLS en Supabase | ✅ |
| Actualiza timer de actividad | ✅ |

---

## 8. Uso en UI

```python
from src.services import AuthService, NotasService

# Login primero
auth = AuthService()
auth.login('email@test.com', 'password123')

# Operar con notas
notas = NotasService()

# Crear
nueva = notas.crear("Mi nota", "Contenido...")
print(f"Creada: {nueva}")

# Listar
todas = notas.listar()
for n in todas:
    print(f"- {n}")

# Actualizar
editada = notas.actualizar(nueva.id, titulo="Título editado")

# Eliminar
eliminada = notas.eliminar(nueva.id)
print(f"Eliminada: {eliminada}")
```

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/ui/menu.py`
