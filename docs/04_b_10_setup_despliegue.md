# 📘 Manual de Despliegue: Setup y Entornos

> **Archivo:** `docs/04_b_10_setup_despliegue.md`  
> **Tipo:** Guía de Infraestructura  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

Este documento explica cómo ejecutar la aplicación en diferentes entornos: Local (CLI), Local (API), Vercel (Serverless), y Docker.

---

## 2. Entry Points

### 2.1 Entry Points Disponibles

| Entry Point | Archivo | Uso |
|-------------|---------|-----|
| CLI Local | `main.py` | Menú interactivo en terminal |
| API Local | `api/index.py` | Servidor HTTP en puerto 8000 |
| Vercel | `api/index.py` | Automático (serverless) |
| Docker | `api/index.py` | Contenedor |

### 2.2 Regla Crítica: load_dotenv() AL PRINCIPIO

```python
# ✅ CORRECTO - en main.py y api/index.py
from dotenv import load_dotenv
load_dotenv()  # ANTES de imports de src/

from src.ui.menu import Menu  # Ahora Settings ya tiene las variables

# ❌ INCORRECTO
from src.ui.menu import Menu  # Settings se inicializa sin variables
from dotenv import load_dotenv
load_dotenv()  # Demasiado tarde
```

---

## 3. Ejecución Local

### 3.1 CLI Interactivo

```powershell
# Desde la raíz del proyecto (venv activado)
python main.py
```

**Resultado:** Menú interactivo con login/registro y CRUD de notas.

### 3.2 API HTTP Local

```powershell
# Inicia servidor en http://localhost:8000
python api/index.py
```

**Endpoints disponibles:**
```
GET  http://localhost:8000/api/health     - Health check
POST http://localhost:8000/api/auth/login  - Login
GET  http://localhost:8000/api/notas       - Listar notas
POST http://localhost:8000/api/notas       - Crear nota
DELETE http://localhost:8000/api/notas?id=xxx - Eliminar
```

**Ejemplo con curl:**
```bash
# Health check
curl http://localhost:8000/api/health

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Listar notas (requiere sesión activa)
curl http://localhost:8000/api/notas
```

---

## 4. Despliegue en Vercel

### 4.1 Prerrequisitos

1. Cuenta en [vercel.com](https://vercel.com)
2. Repositorio en GitHub conectado
3. Variables de entorno configuradas en Vercel Dashboard

### 4.2 Configuración (vercel.json)

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

### 4.3 Variables de Entorno en Vercel

1. Ir a Vercel Dashboard → Proyecto → Settings → Environment Variables
2. Agregar:
   - `SUPABASE_URL` = tu URL de Supabase
   - `SUPABASE_KEY` = tu Anon Key
3. Deploy (automático con cada push)

### 4.4 VercelBridge Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    VERCEL BRIDGE PATTERN                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Request HTTP (Vercel)                                     │
│        │                                                    │
│        ▼                                                    │
│   api/index.py                                              │
│        │                                                    │
│        ▼                                                    │
│   VercelBridge.handle_request(method, path, body)          │
│        │                                                    │
│        ▼                                                    │
│   ┌─────────────┬─────────────┬─────────────┐              │
│   │ AuthService │ NotasService│ (otros...)  │              │
│   └─────────────┴─────────────┴─────────────┘              │
│        │                                                    │
│        ▼                                                    │
│   Response JSON                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Despliegue con Docker

### 5.1 Construir Imagen

```bash
# Desde la raíz del proyecto
docker build -t crud-notas .
```

### 5.2 Ejecutar Contenedor

```bash
# API Server (puerto 8000)
docker run -p 8000:8000 \
  -e SUPABASE_URL=https://xxx.supabase.co \
  -e SUPABASE_KEY=eyJhbGciOi... \
  crud-notas

# CLI Interactivo
docker run -it \
  -e SUPABASE_URL=https://xxx.supabase.co \
  -e SUPABASE_KEY=eyJhbGciOi... \
  crud-notas python main.py
```

### 5.3 Dockerfile Explicado

```dockerfile
FROM python:3.11-slim          # Imagen base ligera

ENV PYTHONPATH=/app            # Para imports de src/

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt  # Instalar deps

COPY . .                       # Copiar código

EXPOSE 8000                    # Puerto
CMD ["python", "api/index.py"] # Comando por defecto
```

---

## 6. Despliegue en Heroku

### 6.1 Procfile

```
web: python api/index.py
```

### 6.2 Comandos

```bash
# Login
heroku login

# Crear app
heroku create mi-crud-notas

# Configurar variables
heroku config:set SUPABASE_URL=https://xxx.supabase.co
heroku config:set SUPABASE_KEY=eyJhbGciOi...

# Deploy
git push heroku main
```

---

## 7. Comparativa de Entornos

| Aspecto | Local CLI | Local API | Vercel | Docker |
|---------|-----------|-----------|--------|--------|
| Entry Point | main.py | api/index.py | api/index.py | api/index.py |
| Variables | .env | .env | Dashboard | -e flags |
| Interactivo | ✅ | ❌ | ❌ | ✅ (con -it) |
| Persistencia | Durante sesión | Por request | Por request | Durante container |
| Timeout | SessionManager | Por implementar | JWT | Por implementar |

---

## 8. Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `Variables faltantes` | .env no existe | Copiar .env.example |
| `ModuleNotFoundError: src` | PYTHONPATH incorrecto | Ejecutar desde raíz |
| `Connection refused` | Puerto ocupado | Cambiar PORT |
| `401 No autenticado` | Sin login previo | Llamar a /api/auth/login |

---

## 9. Seguridad en Producción

⚠️ **IMPORTANTE:**

Este proyecto es **DIDÁCTICO** y NO está diseñado para producción real.

| Riesgo | Mitigación Sugerida |
|--------|---------------------|
| HTTP sin HTTPS | Usar reverse proxy (nginx) |
| Sin rate limiting | Implementar middleware |
| Tokens en memoria | Usar cookies HttpOnly |
| Sin logging | Implementar logging |

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `README.md`
