# 🏗️ Fase 3-A (Parte 1): Definición de Arquitectura

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `docs/02_analisis.md`

---

## 1. Arquitectura Seleccionada: Layered Architecture + BaaS

### 1.1 Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│  Páginas Next.js │ Componentes React │ Estilos CSS          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                       │
│  Hooks (useNotas) │ Contexts (AuthCtx) │ Middleware         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE INFRAESTRUCTURA                  │
│  Cliente Supabase (Singleton) │ Services (Adapters)         │
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
| **Separación de responsabilidades** | UI renderiza, Aplicación coordina, Infraestructura conecta |
| **Facilidad de testing** | Cada capa se prueba aisladamente |
| **Mantenibilidad** | Cambios en una capa no afectan otras |
| **Escalabilidad didáctica** | Fácil de explicar para principiantes |
| **Compatibilidad serverless** | Sin estado entre requests |
| **Reducción de código** | Supabase provee Auth y DB como servicio |

#### ¿Por qué NO otras arquitecturas?

| Arquitectura | Razón de Exclusión |
|--------------|-------------------|
| **Microservicios** | Overkill para CRUD simple |
| **Monolito tradicional** | Requiere backend propio |
| **Hexagonal/Clean** | Demasiado abstracto para MVP |
| **Event-Driven** | Sin eventos complejos |
| **MVC clásico** | Next.js App Router no lo usa |

---

## 2. Estructura de Archivos Propuesta

```
src/
├── app/                    # CAPA PRESENTACIÓN
│   ├── layout.js
│   ├── page.js
│   ├── login/
│   │   └── page.js
│   └── notas/
│       ├── page.js
│       ├── nueva/
│       │   └── page.js
│       └── [id]/
│           └── page.js
│
├── components/             # CAPA PRESENTACIÓN
│   ├── AuthForm.js
│   ├── NotaCard.js
│   ├── NotaForm.js
│   └── LogoutButton.js
│
├── context/                # CAPA APLICACIÓN
│   └── AuthContext.js
│
├── hooks/                  # CAPA APLICACIÓN (Facade)
│   ├── useAuth.js
│   └── useNotas.js
│
├── lib/                    # CAPA INFRAESTRUCTURA
│   ├── supabase.js         # Singleton
│   └── services/
│       ├── authService.js  # Adapter
│       └── notasService.js # Adapter
│
├── styles/
│   └── globals.css
│
└── middleware.js           # CAPA APLICACIÓN
```

---

> **Continúa en:** `03_a_2_patrones.md`
