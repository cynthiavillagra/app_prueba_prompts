# 📘 Manual Técnico: session_manager.py

> **Archivo:** `src/services/session_manager.py`  
> **Tipo:** Singleton de Sesión  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `session_manager.py` gestiona el estado de la sesión del usuario, implementando el **timeout de 15 minutos por inactividad** requerido.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | AUTH |
| **Requisitos** | RF-03, RF-04, RF-15, RNF-SEC-02 |
| **Historia de Usuario** | HU-02 (Login), HU-03 (Logout) |
| **Criterio de Aceptación** | Sesión expira tras 15 min inactividad |
| **Caso de Uso** | CU-01 (Gestionar Autenticación) |
| **Escenario** | Login, Verificación, Timeout, Logout |

---

## 2. Estrategia de Construcción

### Diagrama de Estados

```
┌─────────────────────────────────────────────────────────────┐
│                    ESTADOS DE SESIÓN                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐                                          │
│   │ NO AUTENTICADO│◄────────────────────────┐               │
│   └──────┬───────┘                          │               │
│          │ login()                          │ timeout()     │
│          ▼                                  │ logout()      │
│   ┌──────────────┐      update_activity()   │               │
│   │ AUTENTICADO  │◄─────────────────────────┤               │
│   │              │                          │               │
│   │ Timer: 15min │──────────────────────────┘               │
│   └──────────────┘                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Timeout de 15 Minutos

```
Login ──► _last_activity = now()
   │
   │  Cada acción del usuario
   ▼
update_activity() ──► _last_activity = now()
   │
   │  Verificación
   ▼
is_session_valid() ──► now() - _last_activity < 900s
   │
   │  Si >= 900s
   ▼
require_auth() ──► raise PermissionError("Sesión expirada...")
```

---

## 3. Aclaración Metodológica

### 3.1 Stateless en Serverless

| Entorno | Comportamiento |
|---------|----------------|
| **CLI Local** | Singleton persiste durante ejecución |
| **Vercel** | Singleton se recrea en cada request → usar JWT del header |
| **Docker** | Similar a local |

### 3.2 Rol del Bloque Main

La prueba atómica verifica:
1. Patrón Singleton
2. Establecer/limpiar sesión
3. Detección de timeout
4. `require_auth()` lanza excepción correcta

---

## 4. Código Fuente

### Ubicación

```
src/
└── services/
    ├── __init__.py
    └── session_manager.py    ◄── Este archivo
```

### Métodos Principales

| Método | Retorno | Descripción |
|--------|---------|-------------|
| `set_session(user, token)` | void | Establece sesión tras login |
| `clear()` | void | Limpia sesión (logout) |
| `update_activity()` | void | Resetea timer de inactividad |
| `is_authenticated()` | bool | ¿Hay usuario? |
| `is_session_valid()` | bool | ¿Hay usuario Y no expiró? |
| `require_auth()` | void/raise | Lanza si no autenticado |
| `get_remaining_time()` | int | Segundos hasta expirar |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/services/session_manager.py
```

### 5.2 Resultado Esperado

```
============================================================
PRUEBA DE FUEGO: SessionManager (Singleton)
============================================================
✅ Singleton verificado: misma instancia
✅ Estado inicial: no autenticado
✅ Sesión establecida: User(test@ejemplo.com)
✅ Sesión válida. Tiempo restante: 899s
✅ require_auth() pasó (sesión válida)
✅ Timeout funciona: sesión expirada detectada
✅ require_auth lanzó excepción correcta: Sesión expirada...
✅ clear() limpia todos los datos
✅ Stateless: sin almacenamiento de sesiones global
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| Singleton | Una sesión por ejecución |
| Timeout configurable | `SESSION_TIMEOUT_SECONDS` en .env |
| `require_auth()` con excepción | Código limpio, fail-fast |
| `update_activity()` explícito | Control granular del timer |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Variable global | Sin encapsulación |
| Cookie/LocalStorage | No hay browser en CLI |
| Verificar timeout en decorator | Menos flexibilidad |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `PermissionError: No autenticado` | Sin login | Llamar a login primero |
| `PermissionError: Sesión expirada` | Timeout | Re-login |
| Sesión se pierde entre requests | Serverless | Usar JWT del header |

### 7.2 Seguridad

| Check | Estado |
|-------|--------|
| Timeout de 15 min | ✅ |
| Limpieza en logout | ✅ |
| Sin sesiones globales hardcodeadas | ✅ |
| Token no expuesto en logs | ✅ |

### 7.3 Diferencias Local vs Nube

| Aspecto | Local (CLI) | Serverless (Vercel) |
|---------|-------------|---------------------|
| Persistencia | Durante ejecución | Por request |
| Timeout | SessionManager | JWT expiration |
| Verificación | `require_auth()` | Middleware con JWT |

---

## 8. Uso en Services

```python
from src.services import SessionManager

class NotasService:
    def __init__(self):
        self._session = SessionManager()
    
    def listar(self):
        # Verificar sesión antes de operar
        self._session.require_auth()
        self._session.update_activity()  # Resetear timer
        
        user_id = self._session.get_user_id()
        # ... operación con user_id ...
```

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/services/auth_service.py`
