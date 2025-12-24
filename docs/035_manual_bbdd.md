# 🗄️ Fase 3.5: Manual de Base de Datos (Supabase)

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Tipo de Persistencia:** PostgreSQL (Supabase)  
> **Stack:** Python POO (sin frameworks)

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

**Variable en .env:** `SUPABASE_URL`

### 2.2 SUPABASE_KEY (Publishable API Key)

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
│  │  ⚠️ Esta key es PÚBLICA y segura porque    │  │
│  │     Row Level Security (RLS) protege       │  │
│  │                                             │  │
└───────────────────────────────────────────────────┘
```

**Variable en .env:** `SUPABASE_KEY`

---

## 3. Configuración de Variables de Entorno (Python)

### 3.1 Archivo `.env` (Desarrollo Local)

**Ubicación:** Raíz del proyecto  
**⚠️ NUNCA subir a Git**

```env
# ============================================
# SUPABASE - Variables de Entorno (LOCAL)
# ============================================
# Este archivo contiene las credenciales reales
# NO subir a Git - está en .gitignore

# URL del proyecto Supabase
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co

# Anon Key (pública, segura porque RLS protege)
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3.2 Archivo `.env.example` (Plantilla)

**Ubicación:** Raíz del proyecto  
**✅ SÍ subir a Git** (sin valores reales)

```env
# ============================================
# SUPABASE - Variables de Entorno (PLANTILLA)
# ============================================
# Copiar este archivo como .env y completar con valores reales

# URL del proyecto Supabase
# Ruta: Project Overview > Project API > Project URL
SUPABASE_URL=tu_url_aqui

# Anon Key (pública, segura porque RLS protege)
# Ruta: Project Overview > Project API > Publishable API Key
SUPABASE_KEY=tu_anon_key_aqui
```

### 3.3 Cargar Variables en Python

```python
# src/config/settings.py

import os
from dotenv import load_dotenv

class Settings:
    """Singleton para configuración desde .env"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_env()
        return cls._instance
    
    def _load_env(self):
        # Cargar .env del directorio raíz
        load_dotenv()
        
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        # Validar que existen
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Faltan variables de entorno. "
                "Copia .env.example a .env y completa los valores."
            )
```

---

## 4. Instalar Dependencias Python

### 4.1 Archivo `requirements.txt`

```txt
# Cliente Supabase oficial para Python
supabase>=2.0.0

# Carga de variables de entorno desde .env
python-dotenv>=1.0.0
```

### 4.2 Instalar

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 5. Actualizar .gitignore

El archivo `.gitignore` debe incluir:

```gitignore
# Variables de entorno (CRÍTICO)
.env
.env.local

# NO ignorar .env.example (es la plantilla)
!.env.example

# Entorno virtual Python
venv/
.venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
```

---

## 6. Ejecutar el Script SQL

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

## 7. Verificar RLS (Row Level Security)

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

## 8. Resumen de Variables

| Variable | Tipo | Dónde obtener | Uso en Python |
|----------|------|---------------|---------------|
| `SUPABASE_URL` | Pública | Project Overview > Project API | `Settings().supabase_url` |
| `SUPABASE_KEY` | Pública | Project Overview > Project API | `Settings().supabase_key` |

---

## 9. Probar Conexión desde Python

```python
# test_conexion.py

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

if not url or not key:
    print("❌ Error: Falta configurar .env")
    exit(1)

client = create_client(url, key)
print(f"✅ Conectado a Supabase: {url}")

# Probar query (debería devolver lista vacía si no hay datos)
response = client.table('notas').select('*').limit(1).execute()
print(f"✅ Query exitosa. Datos: {response.data}")
```

Ejecutar:
```bash
python test_conexion.py
```

---

## 10. Troubleshooting

### Error: "relation notas does not exist"
- Ejecutar el script `database/init.sql` en SQL Editor

### Error: "new row violates row-level security"
- Verificar que el `user_id` enviado coincide con `auth.uid()`
- Verificar que el usuario está autenticado

### Error: "Invalid API key"
- Verificar que copiaste la key correctamente
- Verificar que el archivo se llama `.env` (no `.env.example`)

### ModuleNotFoundError: No module named 'supabase'
- Ejecutar `pip install -r requirements.txt`
- Verificar que el entorno virtual está activado

---

> **Documento generado:** 2025-12-23  
> **Script SQL:** `database/init.sql`
