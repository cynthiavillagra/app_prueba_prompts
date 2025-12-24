# 🏗️ Fase 3-A (Parte 1): Definición de Arquitectura

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `docs/02_analisis.md`  
> **Stack:** Python POO (sin frameworks)

---

## 1. Arquitectura Seleccionada: Layered Architecture + BaaS

### 1.1 Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│           CLI (Menu interactivo) o Web estática             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                       │
│      Services (AuthService, NotasService) + Controllers     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE DOMINIO                          │
│          Modelos POO (User, Nota) + Reglas de negocio       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE INFRAESTRUCTURA                  │
│       SupabaseClient (Singleton) + Repositories             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICIOS EXTERNOS (BaaS)                │
│               SUPABASE: Auth + PostgreSQL + RLS             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Justificación

#### ¿Por qué SÍ Layered Architecture + BaaS?

| Aspecto | Justificación |
|---------|---------------|
| **Separación de responsabilidades** | UI presenta, Services coordinan, Modelos encapsulan |
| **Facilidad de testing** | Cada capa se prueba aisladamente con `if __name__` |
| **Principios POO claros** | Clases con responsabilidades definidas |
| **Mantenibilidad** | Cambios en una capa no afectan otras |
| **Escalabilidad didáctica** | Fácil de explicar para principiantes |
| **Reducción de código** | Supabase provee Auth y DB como servicio |

#### ¿Por qué NO otras arquitecturas?

| Arquitectura | Razón de Exclusión |
|--------------|-------------------|
| **Microservicios** | Overkill para CRUD simple |
| **Django/Flask** | Oculta la POO, menos didáctico |
| **Hexagonal/Clean** | Demasiado abstracto para MVP |
| **Event-Driven** | Sin eventos complejos |
| **MVC Web** | No queremos framework web |

---

## 2. Estructura de Archivos Propuesta

```
proyecto/
├── .env                    # Variables de entorno (NO subir)
├── .env.example            # Plantilla
├── .gitignore
├── requirements.txt        # Dependencias Python
├── README.md
│
├── docs/                   # Documentación SDLC
│   └── *.md
│
├── database/
│   └── init.sql            # Script SQL para Supabase
│
├── src/                    # Código fuente Python
│   ├── __init__.py
│   ├── main.py             # Punto de entrada (CLI)
│   │
│   ├── config/             # CONFIGURACIÓN
│   │   ├── __init__.py
│   │   └── settings.py     # Carga de .env (Singleton)
│   │
│   ├── models/             # CAPA DOMINIO (Entidades POO)
│   │   ├── __init__.py
│   │   ├── user.py         # Clase User
│   │   └── nota.py         # Clase Nota
│   │
│   ├── services/           # CAPA APLICACIÓN (Lógica)
│   │   ├── __init__.py
│   │   ├── auth_service.py # AuthService (Strategy)
│   │   └── notas_service.py # NotasService (Adapter)
│   │
│   ├── repositories/       # CAPA INFRAESTRUCTURA
│   │   ├── __init__.py
│   │   └── supabase_client.py  # SupabaseClient (Singleton)
│   │
│   └── ui/                 # CAPA PRESENTACIÓN
│       ├── __init__.py
│       └── menu.py         # Menú CLI interactivo
│
└── tests/                  # Tests unitarios
    ├── __init__.py
    ├── test_models.py
    └── test_services.py
```

---

## 3. Mapeo Capas → Archivos

| Capa | Directorio | Archivos |
|------|------------|----------|
| Presentación | `src/ui/` | `menu.py` |
| Aplicación | `src/services/` | `auth_service.py`, `notas_service.py` |
| Dominio | `src/models/` | `user.py`, `nota.py` |
| Infraestructura | `src/repositories/` | `supabase_client.py` |
| Configuración | `src/config/` | `settings.py` |

---

> **Continúa en:** `03_a_2_patrones.md`
