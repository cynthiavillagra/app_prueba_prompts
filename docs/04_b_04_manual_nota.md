# 📘 Manual Técnico: nota.py

> **Archivo:** `src/models/nota.py`  
> **Tipo:** Entidad de Dominio  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `nota.py` define la entidad `Nota` que representa una nota personal del usuario. Es la entidad central del módulo CRUD.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | NOTAS |
| **Requisitos** | RF-05, RF-06, RF-07, RF-08, RF-09, RF-16, RF-17 |
| **Historia de Usuario** | HU-04, HU-05, HU-06, HU-07 |
| **Criterio de Aceptación** | CRUD completo de notas |
| **Caso de Uso** | CU-02 (Gestionar Notas) |
| **Escenario** | Crear, Listar, Editar, Eliminar |

---

## 2. Estrategia de Construcción

### Mapeo a Base de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                    MAPEO ENTIDAD - TABLA                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Clase Nota (Python)          Tabla notas (PostgreSQL)    │
│   ───────────────────          ─────────────────────────    │
│   id: str              ◄─────► id: UUID (PK)                │
│   user_id: str         ◄─────► user_id: UUID (FK)           │
│   title: str           ◄─────► title: TEXT NOT NULL         │
│   content: str|None    ◄─────► content: TEXT                │
│   created_at: datetime ◄─────► created_at: TIMESTAMPTZ      │
│   updated_at: datetime ◄─────► updated_at: TIMESTAMPTZ      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Aclaración Metodológica

### 3.1 Validaciones

| Campo | Validación | Cuándo |
|-------|------------|--------|
| `title` | No vacío, trimmed | `__post_init__()` |
| `content` | Opcional | - |
| Fechas | Conversión ISO → datetime | `__post_init__()` |

### 3.2 Métodos de Serialización

| Método | Uso | Incluye ID | Incluye Fechas |
|--------|-----|------------|----------------|
| `to_dict(include_id=True)` | UPDATE | Sí | No |
| `to_dict(include_id=False)` | INSERT | No | No |
| `to_display_dict()` | UI/CLI | Sí | Sí (formateadas) |

---

## 4. Código Fuente

### Ubicación

```
src/
└── models/
    ├── __init__.py
    ├── user.py
    └── nota.py    ◄── Este archivo
```

### Campos

| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `id` | str | Sí | - | UUID de la nota |
| `user_id` | str | Sí | - | UUID del propietario |
| `title` | str | Sí | - | Título (no vacío) |
| `content` | str | No | None | Contenido |
| `created_at` | datetime | No | None | Fecha creación |
| `updated_at` | datetime | No | None | Última modificación |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
python src/models/nota.py
```

### 5.2 Resultado Esperado

```
============================================================
PRUEBA DE FUEGO: Nota (Entidad)
============================================================
✅ Nota creada desde dict: [nota-123] Mi primera nota
✅ Título limpiado (trim): 'Mi primera nota'
✅ Validación de título funciona: El título no puede estar vacío
✅ to_dict(include_id=False) funciona: ['user_id', 'title', 'content']
✅ to_dict(include_id=True) funciona: ['user_id', 'title', 'content', 'id']
✅ Preview funciona: 'Este es el contenido de mi...'
✅ to_display_dict funciona: fecha = 24/12/2025 15:00
✅ Roundtrip from_dict → to_dict OK
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| `@dataclass` | Consistencia con User |
| Validación en `__post_init__` | Falla rápido si título vacío |
| `to_dict(include_id)` | Flexibilidad para INSERT/UPDATE |
| `to_display_dict()` | Separación presentación/persistencia |
| `get_preview()` | UX mejorada en listas |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Dict directamente | Sin validación de título |
| SQLAlchemy ORM | Dependencia heavy para MVP |
| Validación en Service | Violación de responsabilidades |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: título vacío` | Nota sin título | Validar antes de crear |
| `KeyError: 'title'` | Dict incompleto | Usar `from_dict()` |
| Fechas como string | No convertidas | Verificar formato ISO |

### 7.2 Seguridad (RLS)

| Check | Responsable |
|-------|-------------|
| Solo ver propias notas | RLS en Supabase |
| user_id correcto | Service + RLS |
| No exponer user_id en UI | `to_display_dict()` |

---

## 8. Uso en Services

```python
from src.models import Nota

class NotasService:
    def crear(self, user_id: str, title: str, content: str = None) -> Nota:
        # Crear entidad (valida título)
        nota = Nota(
            id='',  # Supabase lo genera
            user_id=user_id,
            title=title,
            content=content
        )
        
        # Insertar en Supabase
        response = self._supabase.table('notas').insert(
            nota.to_dict(include_id=False)
        ).execute()
        
        # Retornar nota con ID generado
        return Nota.from_dict(response.data[0])
```

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/services/session_manager.py`
