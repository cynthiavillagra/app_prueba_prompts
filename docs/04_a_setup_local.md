# 🛠️ Fase 4-A: Setup Local

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-24  
> **Fase:** Implementación - Setup Local  
> **Stack:** Python 3.11+ (POO sin frameworks)

---

## 1. Prerrequisitos

### Software Requerido

| Software | Versión Mínima | Verificar |
|----------|----------------|-----------|
| Python | 3.11+ | `python --version` |
| pip | 21+ | `pip --version` |
| Git | 2.0+ | `git --version` |

### Cuenta Supabase

- [ ] Proyecto creado en [supabase.com](https://supabase.com)
- [ ] Script `database/init.sql` ejecutado
- [ ] API Keys obtenidas (ver `docs/035_manual_bbdd.md`)

---

## 2. Pasos de Setup

### Paso 1: Clonar Repositorio (si aplica)

```powershell
git clone https://github.com/tu-usuario/app_prueba_prompts.git
cd app_prueba_prompts
```

### Paso 2: Crear Entorno Virtual

```powershell
# Crear entorno virtual en carpeta 'venv'
python -m venv venv
```

**¿Por qué entorno virtual?**
- Aísla las dependencias del proyecto
- Evita conflictos con otros proyectos Python
- Facilita replicar el entorno exacto

### Paso 3: Activar Entorno Virtual

```powershell
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

**Verificar activación:** El prompt debería mostrar `(venv)` al inicio.

```
(venv) PS C:\...\app_prueba_prompts>
```

### Paso 4: Instalar Dependencias

```powershell
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed supabase-2.x.x python-dotenv-1.x.x ...
```

### Paso 5: Configurar Variables de Entorno

```powershell
# Copiar plantilla
copy .env.example .env

# Editar .env con tus credenciales
notepad .env
```

**Contenido de `.env`:**
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paso 6: Verificar Instalación

```powershell
python -c "from supabase import create_client; print('✅ Supabase instalado')"
python -c "from dotenv import load_dotenv; print('✅ python-dotenv instalado')"
```

---

## 3. Verificar Conexión a Supabase

Crear archivo temporal `test_conexion.py`:

```python
# test_conexion.py - Eliminar después de verificar

import os
from dotenv import load_dotenv
from supabase import create_client

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

# Validar que existen
if not url or not key:
    print("❌ Error: Falta configurar .env")
    print("   Copia .env.example a .env y completa los valores")
    exit(1)

# Crear cliente
try:
    client = create_client(url, key)
    print(f"✅ Conectado a Supabase")
    print(f"   URL: {url}")
    
    # Probar query (debería devolver lista vacía si no hay datos)
    response = client.table('notas').select('*').limit(1).execute()
    print(f"✅ Query exitosa. Registros: {len(response.data)}")
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
```

**Ejecutar:**
```powershell
python test_conexion.py
```

**Salida esperada:**
```
✅ Conectado a Supabase
   URL: https://xxx.supabase.co
✅ Query exitosa. Registros: 0
```

---

## 4. Estructura del Proyecto (Post-Setup)

```
app_prueba_prompts/
├── venv/                   # ← Creado en Paso 2 (NO subir a Git)
├── .env                    # ← Creado en Paso 5 (NO subir a Git)
├── .env.example            # ✓ Plantilla
├── .gitignore              # ✓ Excluye venv/ y .env
├── requirements.txt        # ✓ Dependencias
├── README.md
│
├── docs/                   # Documentación SDLC
│   ├── 01_planificacion.md
│   ├── 02_analisis.md
│   ├── 03_*.md
│   ├── 035_manual_bbdd.md
│   ├── 04_a_setup_local.md # ← Este documento
│   └── CHECKPOINT.md
│
├── database/
│   └── init.sql
│
└── src/                    # ← Se creará en Fase 4-B
    └── ...
```

---

## 5. Checklist de Verificación

| # | Verificación | Comando | Esperado |
|---|--------------|---------|----------|
| 1 | Python instalado | `python --version` | Python 3.11+ |
| 2 | Entorno creado | `dir venv` (Win) / `ls venv` | Carpeta existe |
| 3 | Entorno activo | Ver prompt | `(venv)` visible |
| 4 | Supabase instalado | `pip show supabase` | Version 2.x.x |
| 5 | dotenv instalado | `pip show python-dotenv` | Version 1.x.x |
| 6 | .env existe | `type .env` (Win) | Variables visibles |
| 7 | Conexión OK | `python test_conexion.py` | ✅ mensajes |

---

## 6. Troubleshooting

### Error: "python no se reconoce como comando"
- Verificar que Python está en el PATH
- Probar con `python3` en lugar de `python`
- Reinstalar Python y marcar "Add to PATH"

### Error: "No module named 'supabase'"
- Verificar que el entorno virtual está activado
- Ejecutar `pip install -r requirements.txt` nuevamente

### Error: "relation notas does not exist"
- Ejecutar `database/init.sql` en Supabase SQL Editor
- Ver `docs/035_manual_bbdd.md` sección 6

### Error: "Invalid API key"
- Verificar que `.env` tiene los valores correctos
- Verificar que no hay espacios extra en las variables

### Error al activar venv en PowerShell
```powershell
# Ejecutar como Administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 7. Próximos Pasos

1. ✅ **Fase 4-A Completada:** Setup Local
2. 🔜 **Fase 4-B Pendiente:** Crear estructura `src/` y clases base

---

> **Documento generado:** 2025-12-24  
> **Referencia:** Continuación de Fase 3.5
