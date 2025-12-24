# 📘 Manual del Servidor Web API

> **Archivo:** `docs/04_b_11_manual_servidor_web.md`  
> **Tipo:** Guía de Uso del Servidor HTTP  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

Este manual explica cómo iniciar, usar y probar el servidor web HTTP local que expone la API REST del CRUD de notas.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | INFRAESTRUCTURA / API |
| **Requisitos** | RNF-ARCH-01, RNF-ARCH-02 |
| **Entry Point** | `api/index.py` |
| **Patrón** | VercelBridge (Adapter WSGI manual) |
| **Puerto** | 8000 (configurable) |

---

## 2. Iniciar el Servidor

### 2.1 Prerrequisitos

```powershell
# 1. Estar en la raíz del proyecto
cd "c:\Users\Cynthia\OneDrive\Escritorio\EDUCACION\00 Pedagogia\app_prueba_prompts"

# 2. Activar entorno virtual
venv\Scripts\activate

# 3. Verificar que .env existe con credenciales
type .env
# Debe mostrar SUPABASE_URL y SUPABASE_KEY
```

### 2.2 Comando de Inicio

```powershell
python api/index.py
```

### 2.3 Salida Esperada

```
============================================================
SERVIDOR API LOCAL - CRUD Didáctico
============================================================
Servidor iniciado en: http://localhost:8000

Endpoints disponibles:
  GET  /api/health     - Health check
  POST /api/auth/login - Login
  GET  /api/notas      - Listar notas
  POST /api/notas      - Crear nota

Presione Ctrl+C para detener
============================================================
```

### 2.4 Detener el Servidor

Presionar `Ctrl+C` en la terminal donde está corriendo.

---

## 3. Endpoints Disponibles

### 3.1 Tabla de Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `GET` | `/api/health` | Health check | No |
| `GET` | `/` | Health check (alias) | No |
| `POST` | `/api/auth/login` | Iniciar sesión | No |
| `POST` | `/api/auth/logout` | Cerrar sesión | Sí |
| `GET` | `/api/notas` | Listar notas | Sí |
| `POST` | `/api/notas` | Crear nota | Sí |
| `DELETE` | `/api/notas?id=xxx` | Eliminar nota | Sí |

### 3.2 Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| `200` | OK - Operación exitosa |
| `201` | Created - Recurso creado |
| `400` | Bad Request - Datos inválidos |
| `401` | Unauthorized - No autenticado / Sesión expirada |
| `404` | Not Found - Recurso no encontrado |
| `500` | Server Error - Error interno |

---

## 4. Pruebas con Curl

### ⚠️ Nota para PowerShell

En PowerShell, `curl` es un alias de `Invoke-WebRequest`. Para usar curl real:

```powershell
# Opción 1: Usar Invoke-RestMethod (recomendado en PowerShell)
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# Opción 2: Usar curl.exe directamente
curl.exe http://localhost:8000/api/health

# Opción 3: Usar Invoke-WebRequest con parsing básico
Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing
```

### 4.1 Health Check

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# Bash/CMD con curl.exe
curl.exe http://localhost:8000/api/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "message": "CRUD Didáctico con Supabase - API funcionando",
  "version": "1.0.0"
}
```

### 4.2 Login

```powershell
# PowerShell
$body = @{
    email = "tu_email@ejemplo.com"
    password = "tu_password"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Bash/CMD con curl.exe
curl.exe -X POST http://localhost:8000/api/auth/login ^
    -H "Content-Type: application/json" ^
    -d "{\"email\":\"tu_email@ejemplo.com\",\"password\":\"tu_password\"}"
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "user": {
    "id": "uuid-del-usuario",
    "email": "tu_email@ejemplo.com"
  }
}
```

**Respuesta error (credenciales incorrectas):**
```json
{
  "error": "Credenciales incorrectas"
}
```

### 4.3 Listar Notas (requiere login previo)

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/notas"

# curl.exe
curl.exe http://localhost:8000/api/notas
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": [
    {
      "id": "nota-uuid",
      "user_id": "user-uuid",
      "title": "Mi nota",
      "content": "Contenido..."
    }
  ],
  "count": 1
}
```

**Respuesta error (sin login):**
```json
{
  "error": "No autenticado. Debe iniciar sesión primero."
}
```

### 4.4 Crear Nota

```powershell
# PowerShell
$body = @{
    titulo = "Nueva nota desde API"
    contenido = "Este es el contenido"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/notas" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# curl.exe
curl.exe -X POST http://localhost:8000/api/notas ^
    -H "Content-Type: application/json" ^
    -d "{\"titulo\":\"Nueva nota\",\"contenido\":\"Contenido aqui\"}"
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": {
    "id": "nueva-nota-uuid",
    "user_id": "user-uuid",
    "title": "Nueva nota desde API",
    "content": "Este es el contenido"
  }
}
```

### 4.5 Eliminar Nota

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/notas?id=nota-uuid" `
    -Method DELETE

# curl.exe
curl.exe -X DELETE "http://localhost:8000/api/notas?id=nota-uuid"
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Nota eliminada"
}
```

### 4.6 Logout

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/auth/logout" `
    -Method POST

# curl.exe
curl.exe -X POST http://localhost:8000/api/auth/logout
```

---

## 5. Flujo Completo de Prueba

### Script de Prueba PowerShell

```powershell
# ============================================
# SCRIPT DE PRUEBA COMPLETA - Servidor API
# ============================================

$baseUrl = "http://localhost:8000"

Write-Host "=== 1. Health Check ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$baseUrl/api/health"

Write-Host "`n=== 2. Login ===" -ForegroundColor Cyan
$loginBody = @{
    email = "TU_EMAIL_AQUI"
    password = "TU_PASSWORD_AQUI"
} | ConvertTo-Json

try {
    $loginResult = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" `
        -Method POST -ContentType "application/json" -Body $loginBody
    Write-Host "Login exitoso: $($loginResult.user.email)" -ForegroundColor Green
} catch {
    Write-Host "Error de login: $_" -ForegroundColor Red
    exit
}

Write-Host "`n=== 3. Listar Notas ===" -ForegroundColor Cyan
$notas = Invoke-RestMethod -Uri "$baseUrl/api/notas"
Write-Host "Notas encontradas: $($notas.count)"

Write-Host "`n=== 4. Crear Nota ===" -ForegroundColor Cyan
$nuevaNota = @{
    titulo = "Nota de prueba API $(Get-Date -Format 'HH:mm:ss')"
    contenido = "Creada desde script de prueba"
} | ConvertTo-Json

$notaCreada = Invoke-RestMethod -Uri "$baseUrl/api/notas" `
    -Method POST -ContentType "application/json" -Body $nuevaNota
Write-Host "Nota creada: $($notaCreada.data.title)" -ForegroundColor Green

Write-Host "`n=== 5. Listar Notas (actualizado) ===" -ForegroundColor Cyan
$notas = Invoke-RestMethod -Uri "$baseUrl/api/notas"
Write-Host "Notas encontradas: $($notas.count)"

Write-Host "`n=== 6. Eliminar Nota ===" -ForegroundColor Cyan
$deleteResult = Invoke-RestMethod -Uri "$baseUrl/api/notas?id=$($notaCreada.data.id)" `
    -Method DELETE
Write-Host "Resultado: $($deleteResult.message)" -ForegroundColor Green

Write-Host "`n=== 7. Logout ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "$baseUrl/api/auth/logout" -Method POST

Write-Host "`n=== PRUEBA COMPLETA ===" -ForegroundColor Green
```

---

## 6. Troubleshooting

### 6.1 Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Connection refused` | Servidor no iniciado | `python api/index.py` |
| `Variables faltantes` | .env no configurado | Verificar `.env` |
| `401 No autenticado` | Sin login previo | Llamar a `/api/auth/login` |
| `401 Sesión expirada` | Pasaron 15 min | Re-login |
| `curl no reconocido` | PowerShell alias | Usar `curl.exe` o `Invoke-RestMethod` |

### 6.2 Verificar Puerto

```powershell
# Ver si el puerto 8000 está en uso
netstat -an | findstr "8000"
```

### 6.3 Ver Logs del Servidor

El servidor muestra en consola cada request recibido:
```
127.0.0.1 - - [24/Dec/2025 16:10:00] "GET /api/health HTTP/1.1" 200 -
127.0.0.1 - - [24/Dec/2025 16:10:05] "POST /api/auth/login HTTP/1.1" 200 -
```

---

## 7. Diferencias con Vercel

| Aspecto | Local (api/index.py) | Vercel |
|---------|---------------------|--------|
| Inicio | Manual (`python api/index.py`) | Automático por request |
| Variables | Desde `.env` | Desde Dashboard Vercel |
| Sesión | SessionManager (memoria) | Por request (sin estado) |
| URL | `http://localhost:8000` | `https://tu-proyecto.vercel.app` |
| Persistencia | Mientras corra el proceso | Ninguna (stateless) |

---

## 8. Seguridad

⚠️ **IMPORTANTE - Solo para desarrollo local:**

| Aspecto | Estado |
|---------|--------|
| HTTPS | ❌ No (usar reverse proxy para prod) |
| CORS | ✅ Habilitado (`Access-Control-Allow-Origin: *`) |
| Rate Limiting | ❌ No implementado |
| Logging seguro | ⚠️ Básico |

---

> **Documento generado:** 2025-12-24  
> **Entry Point:** `api/index.py`  
> **Puerto:** 8000
