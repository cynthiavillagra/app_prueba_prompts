# 📋 Fase 1: Planificación

> **Proyecto:** CRUD Didáctico con Supabase  
> **Versión:** 1.0.0  
> **Fecha:** 2025-12-23  
> **Autor:** Equipo de Desarrollo  

---

## 1. Resumen Ejecutivo

### 1.1 Definición del Proyecto

Este proyecto es una **aplicación web CRUD (Create, Read, Update, Delete)** de propósito didáctico, diseñada para enseñar la integración entre un frontend moderno (Next.js), una base de datos en la nube (Supabase PostgreSQL) y un servicio de hosting serverless (Vercel).

La aplicación permite a usuarios autenticados gestionar una lista personal de "Notas", implementando buenas prácticas de seguridad como Row Level Security (RLS) y arquitectura 100% stateless.

### 1.2 Objetivo General

Desarrollar una aplicación web funcional que sirva como **material educativo de referencia** para entender:

1. **Integración Frontend-Backend:** Cómo conectar Next.js con Supabase.
2. **Autenticación Segura:** Implementación de login/registro con JWT.
3. **Seguridad de Datos:** Row Level Security para aislamiento multi-tenant.
4. **Despliegue Serverless:** Deploy en Vercel con variables de entorno.
5. **Metodología SDLC:** Desarrollo por fases con documentación completa.

### 1.3 Objetivos Específicos

| ID | Objetivo | Métrica de Éxito |
|----|----------|------------------|
| O1 | Implementar autenticación email/password | Login/Registro funcionando en < 3 segundos |
| O2 | Desarrollar CRUD completo de Notas | 4 operaciones (CRUD) funcionales |
| O3 | Garantizar aislamiento de datos por usuario | RLS activo, tests de seguridad pasando |
| O4 | Desplegar en Vercel | URL pública accesible |
| O5 | Documentar todo el proceso | Manual replicable en docs/ |

### 1.4 Alcance

#### ✅ Dentro del Alcance (In Scope)

| Módulo | Funcionalidades |
|--------|-----------------|
| **Autenticación** | Registro, Login, Logout, Protección de rutas |
| **Notas** | Crear, Listar, Editar, Eliminar |
| **UI** | Diseño responsive, estados de carga, mensajes de error |
| **Seguridad** | RLS, variables de entorno, JWT |
| **Deploy** | Vercel con dominio automático |
| **Documentación** | Manual completo por fases |

#### ❌ Fuera del Alcance (Out of Scope)

| Funcionalidad | Razón de Exclusión |
|---------------|-------------------|
| OAuth (Google, GitHub) | Complejidad adicional innecesaria para MVP |
| Roles y permisos avanzados | Se implementará en versión futura |
| Modo demo sin login | Baja prioridad, fase futura |
| Búsqueda y filtros avanzados | Fuera del alcance didáctico inicial |
| Notificaciones push | Requiere infraestructura adicional |
| Tests E2E automatizados | Se documentará pero no se implementará |

### 1.5 Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────┐
│                    STACK TECNOLÓGICO                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FRONTEND                                                   │
│  ├── Next.js 14 (App Router)                               │
│  ├── React 18 (Server + Client Components)                 │
│  └── CSS Vanilla (sin frameworks)                          │
│                                                             │
│  BACKEND / BaaS                                             │
│  ├── Supabase PostgreSQL (Base de datos)                   │
│  ├── Supabase Auth (Autenticación JWT)                     │
│  └── Supabase Client SDK (@supabase/supabase-js)           │
│                                                             │
│  HOSTING                                                    │
│  ├── Vercel (Serverless Functions)                         │
│  └── Vercel Edge Network (CDN global)                      │
│                                                             │
│  HERRAMIENTAS                                               │
│  ├── Git + GitHub (Control de versiones)                   │
│  ├── npm (Gestión de dependencias)                         │
│  └── VS Code (IDE recomendado)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Justificación de Tecnologías

| Tecnología | ¿Por qué SÍ? | ¿Por qué NO alternativas? |
|------------|--------------|---------------------------|
| **Next.js 14** | Zero-config con Vercel, SSR/SSG, App Router moderno | Create React App está deprecado, Vite requiere más config |
| **Supabase** | PostgreSQL real, Auth incluido, RLS nativo, free tier generoso | Firebase tiene modelo de datos NoSQL, menos didáctico |
| **Vercel** | Deploy automático desde Git, HTTPS gratis, variables de entorno fáciles | Netlify no tiene integración nativa con Next.js |
| **CSS Vanilla** | Control total, sin dependencias, más didáctico | Tailwind agrega curva de aprendizaje innecesaria |
| **JavaScript** | Menor barrera de entrada que TypeScript para principiantes | TypeScript se puede agregar después |

---

## 2. Análisis de Riesgos

### 2.1 Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Nivel | Mitigación |
|----|--------|--------------|---------|-------|------------|
| R1 | **Memoria Volátil (Serverless)** - Pérdida de estado entre requests | Alta | Crítico | 🔴 Alto | Arquitectura 100% stateless, JWT en cookies, cero variables globales |
| R2 | **Exposición de Credenciales** - Claves hardcodeadas en código | Media | Crítico | 🔴 Alto | `.env.local` + `.gitignore`, validación pre-commit |
| R3 | **Fuga de Datos entre Usuarios** - Usuario A ve datos de Usuario B | Baja | Crítico | 🟡 Medio | RLS obligatorio desde día 1, tests de aislamiento |
| R4 | **Token JWT Expirado** - Sesión inválida sin aviso | Media | Medio | 🟡 Medio | Refresh automático de Supabase, UI de error clara |
| R5 | **Límites Free Tier** - Superación de cuotas gratuitas | Baja | Bajo | 🟢 Bajo | Monitoreo de uso, alertas de Supabase |
| R6 | **Dependencias Desactualizadas** - Vulnerabilidades de seguridad | Media | Medio | 🟡 Medio | `npm audit` periódico, Dependabot en GitHub |
| R7 | **Pérdida de Código Local** - Sin backup remoto | Media | Alto | 🟡 Medio | Push a GitHub después de cada fase |

### 2.2 Plan de Mitigación Detallado

#### R1: Memoria Volátil (Serverless)

```
PROHIBIDO en arquitectura serverless:
❌ let session = {}  // Variable global mutable
❌ const cache = new Map()  // Caché en memoria
❌ app.use(session({ store: MemoryStore }))  // Sesiones en RAM

PERMITIDO:
✅ Cookies firmadas (httpOnly, secure)
✅ JWT tokens (stateless por diseño)
✅ Base de datos para cualquier estado persistente
✅ localStorage/sessionStorage en cliente (para UI state)
```

#### R2: Exposición de Credenciales

```
Estructura de archivos:

.env.local          # ← Secretos reales (NUNCA se sube)
.env.example        # ← Plantilla sin valores (SÍ se sube)
.gitignore          # ← Debe incluir .env*

Contenido de .env.example:
NEXT_PUBLIC_SUPABASE_URL=tu_url_aqui
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_key_aqui
```

#### R3: Fuga de Datos entre Usuarios

```sql
-- SIEMPRE activar RLS en tablas con datos de usuario
ALTER TABLE notas ENABLE ROW LEVEL SECURITY;

-- SIEMPRE crear política que filtre por user_id
CREATE POLICY "isolation" ON notas
    FOR ALL USING (auth.uid() = user_id);
    
-- TEST de verificación (debe fallar sin auth):
-- SELECT * FROM notas; -- Error: RLS violation
```

---

## 3. Plan de Trabajo (Sprints)

### 3.1 Metodología

- **Enfoque:** Iterativo incremental (mini-sprints de 1-2 horas)
- **Entregable por Sprint:** Funcionalidad probada + documentación
- **Validación:** Manual de pruebas + checkpoint en docs/

### 3.2 Roadmap de Sprints

```
┌─────────────────────────────────────────────────────────────┐
│                      ROADMAP DEL PROYECTO                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sprint 0: Configuración ──────────────────────► [1 hora]   │
│  ├── Inicializar repo Git                                  │
│  ├── Crear proyecto Next.js                                │
│  ├── Configurar .env.example                               │
│  └── Documentar setup en README.md                         │
│                                                             │
│  Sprint 1: Supabase ───────────────────────────► [1 hora]   │
│  ├── Crear proyecto en Supabase                            │
│  ├── Crear tabla "notas" con RLS                           │
│  ├── Configurar cliente Supabase en Next.js                │
│  └── Probar conexión básica                                │
│                                                             │
│  Sprint 2: Autenticación ──────────────────────► [2 horas]  │
│  ├── Implementar registro de usuario                       │
│  ├── Implementar login                                     │
│  ├── Implementar logout                                    │
│  ├── Proteger rutas (middleware)                           │
│  └── Probar flujo completo                                 │
│                                                             │
│  Sprint 3: CRUD Notas ─────────────────────────► [2 horas]  │
│  ├── Listar notas del usuario                              │
│  ├── Crear nueva nota                                      │
│  ├── Editar nota existente                                 │
│  ├── Eliminar nota                                         │
│  └── Probar todas las operaciones                          │
│                                                             │
│  Sprint 4: UI/UX ──────────────────────────────► [1.5 horas]│
│  ├── Diseño visual atractivo                               │
│  ├── Estados de carga (loading)                            │
│  ├── Mensajes de éxito/error                               │
│  ├── Responsive design                                     │
│  └── Ocultar elementos no funcionales                      │
│                                                             │
│  Sprint 5: Deploy ─────────────────────────────► [1 hora]   │
│  ├── Configurar variables en Vercel                        │
│  ├── Deploy inicial                                        │
│  ├── Pruebas en producción                                 │
│  └── Documentar URL final                                  │
│                                                             │
│  Sprint 6: Documentación Final ────────────────► [1 hora]   │
│  ├── Completar Manual de Replicación                       │
│  ├── Actualizar CHECKPOINT.md                              │
│  ├── Revisión final de código                              │
│  └── Tag de versión v1.0.0                                 │
│                                                             │
│  TIEMPO TOTAL ESTIMADO: ~9.5 horas                         │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Detalle por Sprint

#### Sprint 0: Configuración Inicial

| Tarea | Archivo/Comando | Criterio de Éxito |
|-------|-----------------|-------------------|
| Inicializar Git | `git init` | Carpeta `.git` creada |
| Crear Next.js | `npx create-next-app@latest ./` | `npm run dev` funciona |
| Crear .env.example | `.env.example` | Plantilla documentada |
| Crear .gitignore | `.gitignore` | `.env.local` excluido |
| Documentar setup | `README.md` | Instrucciones claras |

#### Sprint 1: Supabase Setup

| Tarea | Archivo/Comando | Criterio de Éxito |
|-------|-----------------|-------------------|
| Crear proyecto Supabase | Dashboard web | URL y keys obtenidas |
| Crear tabla notas | SQL en dashboard | Tabla visible |
| Activar RLS | SQL | Policies activas |
| Instalar SDK | `npm install @supabase/supabase-js` | Package instalado |
| Crear cliente | `src/lib/supabase.js` | Import funciona |
| Test de conexión | Console.log | Datos recibidos |

#### Sprint 2: Autenticación

| Tarea | Archivo | Criterio de Éxito |
|-------|---------|-------------------|
| Formulario Login/Registro | `src/app/login/page.js` | UI visible |
| Lógica de registro | `signUp()` | Usuario creado en Supabase |
| Lógica de login | `signIn()` | Sesión activa |
| Lógica de logout | `signOut()` | Sesión destruida |
| Middleware protección | `src/middleware.js` | Redirect a login si no auth |
| Contexto de auth | `src/context/AuthContext.js` | Estado global del usuario |

#### Sprint 3: CRUD Notas

| Tarea | Archivo | Criterio de Éxito |
|-------|---------|-------------------|
| Página lista | `src/app/notas/page.js` | Muestra notas del usuario |
| Componente card | `src/components/NotaCard.js` | Renderiza una nota |
| Página crear | `src/app/notas/nueva/page.js` | Formulario funcional |
| Página editar | `src/app/notas/[id]/page.js` | Carga y guarda datos |
| Función eliminar | En NotaCard | Confirma y elimina |
| Formulario reutilizable | `src/components/NotaForm.js` | Crear y editar usan mismo form |

#### Sprint 4: UI/UX

| Tarea | Archivo | Criterio de Éxito |
|-------|---------|-------------------|
| Estilos globales | `src/styles/globals.css` | Diseño coherente |
| Loading states | Componentes | Spinner visible durante carga |
| Error handling | Componentes | Mensajes claros |
| Responsive | CSS | Mobile-friendly |
| Empty states | Componentes | "No hay notas" si lista vacía |

#### Sprint 5: Deploy

| Tarea | Plataforma | Criterio de Éxito |
|-------|------------|-------------------|
| Push a GitHub | Git | Repo público/privado |
| Conectar Vercel | Vercel Dashboard | Proyecto importado |
| Variables de entorno | Vercel Dashboard | Secrets configurados |
| Deploy | Automático | Build exitoso |
| Pruebas producción | URL pública | Login y CRUD funcionan |

#### Sprint 6: Documentación Final

| Tarea | Archivo | Criterio de Éxito |
|-------|---------|-------------------|
| Manual completo | `docs/*.md` | Todos los archivos completos |
| CHECKPOINT final | `docs/CHECKPOINT.md` | Estado "Producción" |
| Tag versión | `git tag v1.0.0` | Tag creado y pusheado |
| Review código | Todos los archivos | Comentarios claros |

---

## 4. Criterios de Aceptación Global

### 4.1 Definition of Done (DoD)

Un Sprint se considera **COMPLETADO** cuando:

- [ ] Todas las tareas del sprint están implementadas
- [ ] El código no tiene errores en consola
- [ ] La funcionalidad ha sido probada manualmente
- [ ] La documentación del sprint está completa
- [ ] El código está commiteado con mensaje descriptivo
- [ ] El CHECKPOINT.md está actualizado

### 4.2 Reglas de Calidad

| Regla | Verificación |
|-------|--------------|
| Zero hardcoded secrets | Grep por `password`, `key`, `secret` en código |
| Stateless architecture | No hay variables globales mutables |
| RLS activo | Todas las tablas tienen policies |
| Testing atómico | Cada archivo tiene forma de probarse |
| Sin placeholders | No hay Lorem Ipsum ni botones sin función |
| Código comentado | Comentarios explican el "por qué" |

---

## 5. Próximos Pasos

1. ✅ **Fase 1 Completada:** Este documento
2. ⏳ **Fase 2 En Progreso:** Análisis de Requisitos (`docs/02_analisis.md`)
3. 🔜 **Fase 3 Pendiente:** Diseño de Arquitectura

---

> **Documento generado:** 2025-12-23  
> **Próxima actualización:** Al completar Fase 2
