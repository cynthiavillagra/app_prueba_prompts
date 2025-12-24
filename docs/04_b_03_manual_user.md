# 📘 Manual Técnico: user.py

> **Archivo:** `src/models/user.py`  
> **Tipo:** Entidad de Dominio  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `user.py` define la entidad `User` que representa a un usuario autenticado en el sistema. Es una clase de dominio independiente de Supabase Auth.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | AUTH / CORE |
| **Requisitos** | RF-01 (Registro), RF-02 (Login), RF-03 (Logout) |
| **Historia de Usuario** | HU-01, HU-02, HU-03 |
| **Criterio de Aceptación** | Usuario puede registrarse y autenticarse |
| **Caso de Uso** | CU-01 (Gestionar Autenticación) |
| **Escenario** | Registro, Login, Logout |

---

## 2. Estrategia de Construcción

### Patrón Entity + Factory Method

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE DATOS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Supabase Auth Response (dict)                             │
│           │                                                 │
│           ▼                                                 │
│   User.from_dict(response) ──► User object                  │
│           │                                                 │
│           ▼                                                 │
│   SessionManager.set_session(user, token)                   │
│           │                                                 │
│           ▼                                                 │
│   user.to_dict() ──► Serialización para UI/logging          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Dataclass

```python
@dataclass
class User:
    id: str           # UUID de Supabase Auth
    email: str        # Email único
    created_at: Optional[datetime]  # Fecha de registro
```

---

## 3. Aclaración Metodológica

### 3.1 Rol del Bloque Main

La prueba atómica verifica:

1. **Creación desde dict** - `from_dict()` funciona correctamente
2. **Serialización** - `to_dict()` genera dict válido
3. **Roundtrip** - from_dict → to_dict → from_dict preserva datos
4. **Seguridad** - IDs enmascarados para logging

---

## 4. Código Fuente

### Ubicación

```
src/
└── models/
    ├── __init__.py
    └── user.py    ◄── Este archivo
```

### Campos

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | str | Sí | UUID del usuario en Supabase Auth |
| `email` | str | Sí | Email único del usuario |
| `created_at` | datetime | No | Fecha de registro |

### Métodos

| Método | Tipo | Retorno | Descripción |
|--------|------|---------|-------------|
| `from_dict(data)` | classmethod | User | Factory desde dict de Supabase |
| `to_dict()` | instance | dict | Serializa a diccionario |
| `get_masked_id()` | instance | str | ID parcialmente oculto |
| `__str__()` | instance | str | Representación legible |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/models/user.py
```

### 5.2 Resultado Esperado (OK)

```
============================================================
PRUEBA DE FUEGO: User (Entidad)
============================================================
✅ User creado desde dict: User(test@ejemplo.com)
   ID completo: a1b2c3d4-e5f6-7890-abcd-ef1234567890
   Email: test@ejemplo.com
   Created: 2025-12-24 15:00:00+00:00
✅ to_dict funciona: {'id': '...', 'email': '...', ...}
✅ from_dict → to_dict roundtrip OK
✅ ID enmascarado: a1b2...7890
✅ Auditoría: Sin datos sensibles en código
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| `@dataclass` | Reduce boilerplate, genera métodos mágicos |
| `from_dict()` classmethod | Factory method, desacopla de Supabase |
| `to_dict()` | Serialización consistente |
| `get_masked_id()` | Logging seguro sin exponer UUIDs |
| Pocos campos | YAGNI - solo lo que necesitamos |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Dict directamente | Sin validación, sin autocompletado |
| Clase tradicional | Más boilerplate |
| TypedDict | No soporta métodos |
| Pydantic | Dependencia adicional para MVP simple |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `KeyError: 'id'` | Dict incompleto de Supabase | Verificar respuesta de Auth |
| `TypeError: ... positional arguments` | Campos faltantes | Usar `from_dict()` |
| `AttributeError: 'NoneType'` | User no creado | Verificar autenticación |

### 7.2 Seguridad

| Check | Estado |
|-------|--------|
| No expone ID completo en `__str__` | ✅ |
| `get_masked_id()` para logs | ✅ |
| Sin datos sensibles hardcodeados | ✅ |

---

## 8. Uso en Services

```python
# Ejemplo en AuthService
from src.models import User

class AuthService:
    def login(self, email: str, password: str) -> User:
        response = self._supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        # Convertir respuesta de Supabase a entidad User
        user = User.from_dict({
            'id': response.user.id,
            'email': response.user.email,
            'created_at': response.user.created_at
        })
        
        return user
```

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/models/nota.py`
