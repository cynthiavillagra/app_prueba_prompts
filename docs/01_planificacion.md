# 📋 Fase 1: Planificación

> **Proyecto:** CRUD Didáctico con Supabase  
> **Versión:** 1.0.0  
> **Fecha:** 2025-12-23  
> **Autor:** Equipo de Desarrollo  

---

## 1. Resumen Ejecutivo

### 1.1 Definición del Proyecto

Este proyecto es una **aplicación CRUD (Create, Read, Update, Delete)** de propósito didáctico, diseñada para enseñar **Programación Orientada a Objetos (POO)** en Python, integración con una base de datos en la nube (Supabase PostgreSQL) y buenas prácticas de desarrollo.

La aplicación permite a usuarios autenticados gestionar una lista personal de "Notas", implementando buenas prácticas de seguridad como Row Level Security (RLS), principios SOLID y patrones de diseño.

### 1.2 Objetivo General

Desarrollar una aplicación web funcional que sirva como **material educativo de referencia** para entender:

1. **Programación Orientada a Objetos:** Clases, herencia, encapsulamiento, polimorfismo.
2. **Patrones de Diseño:** Singleton, Factory, Adapter, Strategy aplicados en Python.
3. **Integración con BaaS:** Conexión Python con Supabase (Auth + PostgreSQL).
4. **Seguridad de Datos:** Row Level Security y manejo seguro de credenciales.
5. **Metodología SDLC:** Desarrollo por fases con documentación completa.

### 1.3 Objetivos Específicos

| ID | Objetivo | Métrica de Éxito |
|----|----------|------------------|
| O1 | Implementar autenticación email/password | Login/Registro funcionando en < 3 segundos |
| O2 | Desarrollar CRUD completo de Notas | 4 operaciones (CRUD) funcionales |
| O3 | Garantizar aislamiento de datos por usuario | RLS activo, tests de seguridad pasando |
| O4 | Ejecutar localmente sin dependencias complejas | `python main.py` funciona |
| O5 | Documentar todo el proceso | Manual replicable en docs/ |

### 1.4 Alcance

#### ✅ Dentro del Alcance (In Scope)

| Módulo | Funcionalidades |
|--------|-----------------|
| **Autenticación** | Registro, Login, Logout, Protección de rutas |
| **Notas** | Crear, Listar, Editar, Eliminar |
| **UI** | CLI interactivo o web simple (HTML/CSS/JS puro) |
| **Seguridad** | RLS, variables de entorno (.env), JWT |
| **Deploy** | Local (Python directo) |
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
│              STACK TECNOLÓGICO (PYTHON POO)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BACKEND (Python Puro - Sin Frameworks)                    │
│  ├── Python 3.11+                                          │
│  ├── supabase-py (Cliente Supabase oficial)                │
│  ├── python-dotenv (Variables de entorno)                  │
│  └── Principios POO (Clases, Herencia, Polimorfismo)       │
│                                                             │
│  FRONTEND (Opcional)                                        │
│  ├── CLI interactivo (input/print)                         │
│  └── O: HTML/CSS/JS puro servido localmente                │
│                                                             │
│  BASE DE DATOS                                              │
│  ├── Supabase PostgreSQL (Base de datos)                   │
│  ├── Supabase Auth (Autenticación JWT)                     │
│  └── Row Level Security (RLS)                              │
│                                                             │
│  HERRAMIENTAS                                               │
│  ├── Git + GitHub (Control de versiones)                   │
│  ├── pip + requirements.txt (Dependencias)                 │
│  └── VS Code / PyCharm (IDE recomendado)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Justificación de Tecnologías

| Tecnología | ¿Por qué SÍ? | ¿Por qué NO alternativas? |
|------------|--------------|---------------------------|
| **Python 3.11+** | Sintaxis clara, ideal para aprender POO, tipado opcional | Java es más verboso, C++ requiere manejo de memoria |
| **Sin frameworks** | Control total, entender cada capa, más didáctico | Flask/Django ocultan la lógica, menos educativo |
| **supabase-py** | Cliente oficial, API idéntica a JS, bien documentado | psycopg2 requiere SQL manual, más complejo |
| **python-dotenv** | Estándar para .env en Python, simple | os.environ directo es menos seguro |
| **CLI** | Sin dependencias de frontend, enfoque en backend POO | Web agrega complejidad innecesaria para MVP |

---

## 2. Análisis de Riesgos

### 2.1 Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Nivel | Mitigación |
|----|--------|--------------|---------|-------|------------|
| R1 | **Exposición de Credenciales** - Claves hardcodeadas en código | Media | Crítico | 🔴 Alto | `.env` + `.gitignore`, nunca en código |
| R2 | **Fuga de Datos entre Usuarios** - Usuario A ve datos de Usuario B | Baja | Crítico | 🟡 Medio | RLS obligatorio desde día 1, tests de aislamiento |
| R3 | **Token JWT Expirado** - Sesión inválida sin aviso | Media | Medio | 🟡 Medio | Validación de sesión antes de cada operación |
| R4 | **Límites Free Tier** - Superación de cuotas gratuitas | Baja | Bajo | 🟢 Bajo | Monitoreo de uso, alertas de Supabase |
| R5 | **Dependencias Desactualizadas** - Vulnerabilidades de seguridad | Media | Medio | 🟡 Medio | `pip audit` periódico, revisar requirements.txt |
| R6 | **Pérdida de Código Local** - Sin backup remoto | Media | Alto | 🟡 Medio | Push a GitHub después de cada fase |
| R7 | **Complejidad de POO** - Sobreingeniería para CRUD simple | Media | Bajo | 🟢 Bajo | Mantener clases simples, KISS principle |

### 2.2 Plan de Mitigación Detallado

#### R1: Exposición de Credenciales

```
Estructura de archivos:

.env                # ← Secretos reales (NUNCA se sube)
.env.example        # ← Plantilla sin valores (SÍ se sube)
.gitignore          # ← Debe incluir .env

Contenido de .env.example:
SUPABASE_URL=tu_url_aqui
SUPABASE_KEY=tu_anon_key_aqui

Carga en Python:
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('SUPABASE_URL')  # ✅ Correcto
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

#### Sprint 0: Configuración Inicial

| Tarea | Archivo/Comando | Criterio de Éxito |
|-------|-----------------|-------------------|
| Inicializar Git | `git init` | Carpeta `.git` creada |
| Crear estructura | Carpetas `src/`, `tests/` | Estructura visible |
| Crear requirements.txt | `requirements.txt` | Dependencias listadas |
| Crear .env.example | `.env.example` | Plantilla documentada |
| Crear .gitignore | `.gitignore` | `.env` excluido |
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
