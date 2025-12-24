# 📘 Manual Técnico: auth_service.py

> **Archivo:** `src/services/auth_service.py`  
> **Tipo:** Service con Strategy Pattern  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `auth_service.py` implementa el servicio de autenticación usando el **patrón Strategy**, permitiendo extensibilidad para múltiples métodos de autenticación.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | AUTH |
| **Requisitos** | RF-01, RF-02, RF-03, RF-04 |
| **Historia de Usuario** | HU-01, HU-02, HU-03 |
| **Criterio de Aceptación** | Login/Register/Logout funcionales |
| **Caso de Uso** | CU-01 (Gestionar Autenticación) |
| **Escenario** | Registro, Login, Logout |

---

## 2. Estrategia de Construcción

### Patrón Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    PATRÓN STRATEGY                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   IAuthStrategy <<interface>>                               │
│   ├── login(**credentials) → (User, token, refresh)        │
│   └── register(**credentials) → User                        │
│              ▲                                              │
│              │                                              │
│   ┌──────────┴──────────┐                                   │
│   │                     │                                   │
│   ▼                     ▼                                   │
│   EmailPasswordStrategy  (OAuthStrategy - futuro)           │
│                                                             │
│   AuthService                                               │
│   ├── _strategy: IAuthStrategy                              │
│   ├── login() ──► _strategy.login()                         │
│   ├── register() ──► _strategy.register()                   │
│   └── logout() ──► clear session                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Login

```
User Input                  AuthService                 Strategy                Supabase
    │                           │                          │                       │
    │ email, password           │                          │                       │
    ├──────────────────────────►│                          │                       │
    │                           │ login(email, pwd)        │                       │
    │                           ├─────────────────────────►│                       │
    │                           │                          │ sign_in_with_password │
    │                           │                          ├──────────────────────►│
    │                           │                          │        response       │
    │                           │                          │◄──────────────────────┤
    │                           │ (User, token)            │                       │
    │                           │◄─────────────────────────┤                       │
    │                           │                          │                       │
    │                           │ set_session(user, token) │                       │
    │                           ├─────────────────────────►SessionManager          │
    │           User            │                          │                       │
    │◄──────────────────────────┤                          │                       │
```

---

## 3. Aclaración Metodológica

### 3.1 Validaciones

| Campo | Validación | Error |
|-------|------------|-------|
| `email` | No vacío | ValueError |
| `password` | Mínimo 6 caracteres | ValueError |
| Credenciales | Supabase Auth | PermissionError |

### 3.2 Rol del Bloque Main

La prueba atómica verifica:
- Creación del servicio
- Estrategia por defecto configurada
- Validaciones de entrada
- Logout sin sesión no causa error
- Sin credenciales hardcodeadas

---

## 4. Código Fuente

### Ubicación

```
src/
└── services/
    ├── __init__.py
    ├── session_manager.py
    └── auth_service.py    ◄── Este archivo
```

### Clases

| Clase | Tipo | Descripción |
|-------|------|-------------|
| `IAuthStrategy` | ABC | Interfaz para estrategias |
| `EmailPasswordStrategy` | Concrete Strategy | Login con email/password |
| `AuthService` | Facade | Servicio principal |

### Métodos de AuthService

| Método | Retorno | Descripción |
|--------|---------|-------------|
| `login(email, password)` | User | Autentica y establece sesión |
| `register(email, password)` | User | Registra nuevo usuario |
| `logout()` | void | Cierra sesión |
| `get_current_user()` | User/None | Usuario actual |
| `is_authenticated()` | bool | ¿Hay sesión válida? |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/services/auth_service.py
```

### 5.2 Resultado Esperado

```
============================================================
PRUEBA DE FUEGO: AuthService
============================================================
✅ AuthService creado correctamente
✅ Estado inicial: no autenticado
✅ Strategy: EmailPasswordStrategy (default)
✅ Validación email: El email es obligatorio
✅ Validación password: La contraseña debe tener al menos 6 caracteres
✅ Logout sin sesión no causa error
✅ get_current_user() es None sin sesión
✅ Auditoría: Sin credenciales hardcodeadas
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| Strategy Pattern | Extensible para OAuth, magic link, etc. |
| Inyección de dependencias | Facilita testing |
| Validación antes de llamar API | Fail-fast, menos requests |
| Mapeo de errores | Mensajes amigables al usuario |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Llamar Supabase directamente | Alto acoplamiento |
| If/else por tipo de auth | Viola Open/Closed |
| Excepciones genéricas | Menos informativas |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: email obligatorio` | Email vacío | Validar input |
| `ValueError: 6 caracteres` | Password muy corto | Mínimo 6 chars |
| `PermissionError: Credenciales` | Login incorrecto | Verificar datos |
| `PermissionError: ya registrado` | Email duplicado | Usar otro email |

### 7.2 Extender con OAuth

```python
# Ejemplo: Agregar OAuth en el futuro
class GoogleOAuthStrategy(IAuthStrategy):
    def login(self, token: str):
        # Implementar OAuth con Google
        pass
    
    def register(self, token: str):
        # OAuth puede registrar automáticamente
        pass

# Uso
auth = AuthService(strategy=GoogleOAuthStrategy(supabase))
```

---

## 8. Seguridad

| Check | Estado |
|-------|--------|
| Validación de entrada | ✅ |
| Sin credenciales hardcodeadas | ✅ |
| Errores genéricos al usuario | ✅ |
| Limpieza de sesión en logout | ✅ |

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/services/notas_service.py`
