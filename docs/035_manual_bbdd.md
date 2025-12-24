# 🗄️ Fase 3.5: Manual de Base de Datos (Supabase)

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Tipo de Persistencia:** PostgreSQL (Supabase)

---

## 1. Crear Proyecto en Supabase

### Paso 1: Registrarse/Iniciar Sesión

1. Ir a [https://supabase.com](https://supabase.com)
2. Click en **"Start your project"** o **"Sign In"**
3. Autenticarse con GitHub (recomendado) o email

### Paso 2: Crear Nuevo Proyecto

1. En el Dashboard, click en **"New Project"**
2. Completar:
   - **Name:** `crud-didactico` (o el nombre que prefieras)
   - **Database Password:** Generar una contraseña segura (¡GUARDARLA!)
   - **Region:** Elegir la más cercana (ej: South America - São Paulo)
3. Click en **"Create new project"**
4. Esperar ~2 minutos mientras se provisiona

```
┌───────────────────────────────────────────────────┐
│              SUPABASE DASHBOARD                   │
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  New Project                                │  │
│  ├─────────────────────────────────────────────┤  │
│  │  Name: crud-didactico                       │  │
│  │  Database Password: ●●●●●●●●●●●●            │  │
│  │  Region: South America (São Paulo)          │  │
│  │                                             │  │
│  │  [Create new project]                       │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## 2. Obtener las API Keys

### 2.1 SUPABASE_URL (Project URL)

**Ruta:** `Project Overview` → Scroll al medio → `Project API`

```
┌───────────────────────────────────────────────────┐
│  Project Overview                                 │
├───────────────────────────────────────────────────┤
│                                                   │
│  [Scroll hacia abajo...]                          │
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │  Project API                                │  │
│  ├─────────────────────────────────────────────┤  │
│  │                                             │  │
│  │  Project URL                                │  │
│  │  ┌─────────────────────────────────────┐    │  │
│  │  │ https://xxxxxxxxxxxx.supabase.co    │    │  │
│  │  └─────────────────────────────────────┘    │  │
│  │                          [Copy]             │  │
│  │                                             │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Variable:** `NEXT_PUBLIC_SUPABASE_URL`

### 2.2 SUPABASE_ANON_KEY (Publishable API Key)

**Ruta:** `Project Overview` → Scroll al medio → `Project API`

```
┌───────────────────────────────────────────────────┐
│  Project API (continuación)                       │
├───────────────────────────────────────────────────┤
│                                                   │
│  │  Publishable API Key (anon, public)         │  │
│  │  ┌─────────────────────────────────────┐    │  │
│  │  │ eyJhbGciOiJIUzI1NiIsInR5cCI6...     │    │  │
│  │  └─────────────────────────────────────┘    │  │
│  │                          [Copy] [Reveal]    │  │
│  │                                             │  │
│  │  ⚠️ Esta key es PÚBLICA y segura de        │  │
│  │     exponer en el frontend (RLS protege)   │  │
│  │                                             │  │
└───────────────────────────────────────────────────┘
```

**Variable:** `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### 2.3 JWT_SECRET (Legacy JWT Secret) - Opcional

**Ruta:** `Project Settings` (ícono engranaje) → `API` → `JWT Settings`

```
┌───────────────────────────────────────────────────┐
│  Project Settings > API                           │
├───────────────────────────────────────────────────┤
│                                                   │
│  JWT Settings                                     │
│  ─────────────                                    │
│                                                   │
│  JWT Secret                                       │
│  ┌─────────────────────────────────────┐          │
│  │ super-secret-jwt-token-with-at...   │          │
│  └─────────────────────────────────────┘          │
│                          [Copy] [Reveal]          │
│                                                   │
│  ⚠️ Esta key es SECRETA - NO exponer            │
│     Solo usar en backend/server-side             │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Variable:** `SUPABASE_JWT_SECRET` (sin NEXT_PUBLIC_)

### 2.4 SERVICE_ROLE_KEY - Solo para Admin

**Ruta:** `Project Settings` → `API` → `Project API keys`

```
⚠️ ADVERTENCIA: Esta key salta TODAS las políticas RLS
   Solo usar en operaciones de servidor confiables
   NUNCA exponer en el frontend
```

**Variable:** `SUPABASE_SERVICE_ROLE_KEY` (sin NEXT_PUBLIC_)

---

## 3. Configuración de Variables de Entorno

### 3.1 Archivo `.env.local` (Desarrollo Local)

**Ubicación:** Raíz del proyecto  
**⚠️ NUNCA subir a Git**

```env
# ============================================
# SUPABASE - Variables de Entorno (LOCAL)
# ============================================
# Este archivo contiene las credenciales reales
# NO subir a Git - está en .gitignore

# URL del proyecto Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co

# Anon Key (pública, segura para frontend)
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# JWT Secret (opcional, solo para validación server-side)
SUPABASE_JWT_SECRET=super-secret-jwt-token...

# Service Role Key (PELIGROSA - solo backend)
# SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3.2 Archivo `.env.example` (Plantilla)

**Ubicación:** Raíz del proyecto  
**✅ SÍ subir a Git** (sin valores reales)

```env
# ============================================
# SUPABASE - Variables de Entorno (PLANTILLA)
# ============================================
# Copiar este archivo como .env.local y completar con valores reales
# Obtener valores de: https://supabase.com/dashboard/project/TU_PROYECTO

# URL del proyecto Supabase
# Ruta: Project Overview > Project API > Project URL
NEXT_PUBLIC_SUPABASE_URL=tu_url_aqui

# Anon Key (pública, segura para frontend)
# Ruta: Project Overview > Project API > Publishable API Key
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key_aqui

# JWT Secret (opcional)
# Ruta: Project Settings > API > JWT Settings > JWT Secret
SUPABASE_JWT_SECRET=tu_jwt_secret_aqui
```

### 3.3 Configuración en Vercel (Deploy)

1. Ir a [vercel.com/dashboard](https://vercel.com/dashboard)
2. Seleccionar tu proyecto
3. Ir a **Settings** → **Environment Variables**
4. Agregar cada variable:

```
┌───────────────────────────────────────────────────┐
│  Vercel > Settings > Environment Variables        │
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌────────────────────────────────────────────┐   │
│  │ Name: NEXT_PUBLIC_SUPABASE_URL             │   │
│  │ Value: https://xxxx.supabase.co            │   │
│  │ Environment: ☑ Production ☑ Preview ☑ Dev │   │
│  └────────────────────────────────────────────┘   │
│                                                   │
│  ┌────────────────────────────────────────────┐   │
│  │ Name: NEXT_PUBLIC_SUPABASE_ANON_KEY        │   │
│  │ Value: eyJhbGciOiJIUzI1...                 │   │
│  │ Environment: ☑ Production ☑ Preview ☑ Dev │   │
│  └────────────────────────────────────────────┘   │
│                                                   │
│  [Save]                                           │
│                                                   │
└───────────────────────────────────────────────────┘
```

**Importante:** Después de agregar variables, hacer **Redeploy** para que tomen efecto.

---

## 4. Actualizar .gitignore

El archivo `.gitignore` debe incluir:

```gitignore
# Variables de entorno (CRÍTICO)
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
.env*.local

# NO ignorar .env.example (es la plantilla)
!.env.example
```

---

## 5. Ejecutar el Script SQL

### Paso 1: Abrir SQL Editor

1. En Supabase Dashboard, ir al menú lateral
2. Click en **"SQL Editor"**
3. Click en **"New Query"**

### Paso 2: Ejecutar init.sql

1. Copiar todo el contenido de `database/init.sql`
2. Pegarlo en el editor SQL
3. Click en **"Run"** (o Ctrl+Enter)

```
┌───────────────────────────────────────────────────┐
│  SQL Editor                                       │
├───────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────────┐  │
│  │ -- Script de inicialización...              │  │
│  │ CREATE TABLE IF NOT EXISTS public.notas...  │  │
│  │ ...                                         │  │
│  └─────────────────────────────────────────────┘  │
│                                                   │
│  [Run] ▶                                          │
│                                                   │
│  Results:                                         │
│  ✓ Success. No rows returned.                    │
│  ✓ 4 policies created                            │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Paso 3: Verificar en Table Editor

1. Ir a **"Table Editor"** en el menú lateral
2. Debería aparecer la tabla **"notas"**
3. Verificar las columnas: id, user_id, title, content, created_at, updated_at

---

## 6. Verificar RLS (Row Level Security)

### Verificar que RLS está activo

1. Ir a **"Authentication"** → **"Policies"**
2. Seleccionar tabla **"notas"**
3. Deberían aparecer 4 políticas:

| Política | Operación | Estado |
|----------|-----------|--------|
| Users can view own notas | SELECT | ✅ Activa |
| Users can insert own notas | INSERT | ✅ Activa |
| Users can update own notas | UPDATE | ✅ Activa |
| Users can delete own notas | DELETE | ✅ Activa |

### Test de Seguridad (Sin Autenticación)

Desde SQL Editor, ejecutar:

```sql
-- Esto debería devolver 0 filas (RLS bloquea)
SELECT * FROM public.notas;
```

Si devuelve 0 filas aunque haya datos, **RLS está funcionando correctamente**.

---

## 7. Resumen de Variables

| Variable | Tipo | Dónde obtener | Uso |
|----------|------|---------------|-----|
| `NEXT_PUBLIC_SUPABASE_URL` | Pública | Project Overview > Project API | Cliente JS |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Pública | Project Overview > Project API | Cliente JS |
| `SUPABASE_JWT_SECRET` | Secreta | Settings > API > JWT | Validación servidor |
| `SUPABASE_SERVICE_ROLE_KEY` | Secreta | Settings > API > Project API keys | Admin bypass RLS |

---

## 8. Troubleshooting

### Error: "relation notas does not exist"
- Ejecutar el script `database/init.sql` en SQL Editor

### Error: "new row violates row-level security"
- Verificar que el `user_id` enviado coincide con `auth.uid()`
- Verificar que el usuario está autenticado

### Error: "JWT expired"
- El token de sesión expiró
- El cliente debe hacer refresh o re-login

### Las variables de entorno no funcionan
- Verificar que el archivo se llama `.env.local` (no `.env`)
- Reiniciar el servidor de desarrollo (`npm run dev`)
- En Vercel: hacer Redeploy después de cambiar variables

---

> **Documento generado:** 2025-12-23  
> **Script SQL:** `database/init.sql`
