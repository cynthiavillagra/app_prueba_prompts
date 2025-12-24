# 📘 Manual Técnico: Frontend (index.html)

> **Archivo:** `public/index.html`  
> **Tipo:** Frontend HTML/CSS/JS  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `public/index.html` implementa el frontend completo de la aplicación, incluyendo:
- Formulario de Login/Registro
- Dashboard de notas con CRUD
- Modal de expiración de sesión
- Timer visual de sesión

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | UI / FRONTEND |
| **Requisitos** | RF-10 a RF-14 |
| **Historia de Usuario** | Todas |
| **Caso de Uso** | CU-01 (Auth), CU-02 (Notas) |
| **Patrones UI** | SPA-like (Single Page Application) |

---

## 2. Estrategia de Construcción

### Arquitectura Frontend

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA FRONTEND                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   HTML (Estructura)                                         │
│   ├── Modal Expiración                                      │
│   ├── Vista Login/Registro (tabs)                           │
│   └── Vista Notas (dashboard)                               │
│                                                             │
│   CSS (Estilos)                                             │
│   ├── Variables CSS (Design System)                         │
│   ├── Componentes (botones, inputs, alertas)                │
│   └── Animaciones (modal, timer)                            │
│                                                             │
│   JavaScript (Lógica)                                       │
│   ├── Estado (state object)                                 │
│   ├── API Calls (fetch wrapper)                             │
│   ├── Timer de sesión                                       │
│   └── CRUD handlers                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Reglas Implementadas

| Regla | Implementación |
|-------|----------------|
| **CERO PLACEHOLDERS** | Todo botón visible tiene handler |
| **AVISO EXPIRACIÓN** | Modal estético `#sessionExpiredModal` |
| **REDIRECCIÓN AUTOMÁTICA** | Listener en botón "Ir al Login" |
| **TIMER VISUAL** | Actualización cada segundo con warning |

---

## 3. Aclaración Metodológica

### 3.1 Flujo de Autenticación

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   LOGIN      │────►│   API CALL   │────►│  SET STATE   │
│   FORM       │     │ /api/login   │     │  user, timer │
└──────────────┘     └──────────────┘     └──────────────┘
                                                │
                                                ▼
                                          ┌──────────────┐
                                          │  SHOW NOTAS  │
                                          │   DASHBOARD  │
                                          └──────────────┘
```

### 3.2 Flujo de Expiración

```
Timer = 0           Modal Expiración        Click "Ir al Login"
    │                     │                        │
    ▼                     ▼                        ▼
┌────────┐          ┌────────────┐          ┌────────────┐
│TIMEOUT │─────────►│   SHOW     │─────────►│   CLEAR    │
│        │          │   MODAL    │          │   STATE    │
└────────┘          └────────────┘          │  SHOW LOGIN│
                                            └────────────┘
```

---

## 4. Código Fuente

### Ubicación

```
proyecto/
├── public/
│   └── index.html    ◄── Este archivo
├── api/
│   └── index.py      (sirve el frontend)
```

### Componentes Principales

| Componente | ID | Descripción |
|------------|-----|-------------|
| Modal Expiración | `#sessionExpiredModal` | Aviso de sesión expirada |
| Vista Login | `#viewLogin` | Formularios login/registro |
| Vista Notas | `#viewNotas` | Dashboard CRUD |
| Timer | `#sessionTimer` | Contador regresivo |
| Lista Notas | `#notesList` | Contenedor de notas |

### Funciones JavaScript

| Función | Descripción |
|---------|-------------|
| `handleLogin(event)` | Procesa login |
| `handleRegister(event)` | Procesa registro |
| `handleLogout()` | Cierra sesión |
| `loadNotas()` | Carga notas del API |
| `handleSaveNota(event)` | Crea/edita nota |
| `deleteNota(id, title)` | Elimina con confirmación |
| `showSessionExpiredModal()` | Muestra modal |
| `startSessionTimer()` | Inicia contador |
| `apiCall(endpoint, options)` | Wrapper de fetch |

---

## 5. Prueba de Fuego

### 5.1 Iniciar Servidor

```powershell
# Terminal 1 - Iniciar servidor
python api/index.py
```

### 5.2 Abrir Frontend

```powershell
# Terminal 2 - Abrir navegador
Start-Process "http://localhost:8000"
```

O abrir manualmente: `http://localhost:8000`

### 5.3 Pruebas Manuales

| Test | Pasos | Resultado Esperado |
|------|-------|-------------------|
| **Login** | Email + Password → Click "Iniciar Sesión" | Muestra dashboard |
| **Timer** | Observar timer | Cuenta regresiva 15:00 → 0:00 |
| **Crear Nota** | Click "Nueva Nota" → Llenar → "Guardar" | Nota aparece en lista |
| **Eliminar** | Click 🗑️ → Confirmar | Nota desaparece |
| **Expiración** | Esperar timeout (o modificar timer) | Modal aparece |
| **Logout** | Click "Cerrar Sesión" | Vuelve a login |

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| HTML/CSS/JS puro | Sin frameworks = sin dependencias |
| CSS Variables | Design system mantenible |
| Single file | Didáctico, fácil de entender |
| Timer en frontend | UX - usuario ve tiempo restante |
| Modal nativo | Sin librerías de modales |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| React/Vue | Requisito: sin frameworks |
| Tailwind | Dependencia de build |
| Archivos separados | Más complejo para demo |
| WebSockets | Overhead para MVP |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| Página en blanco | Servidor no iniciado | `python api/index.py` |
| "Error de conexión" | API no responde | Verificar servidor corriendo |
| Login falla | Credenciales incorrectas | Verificar email/password |
| Timer no aparece | No hay sesión | Hacer login primero |
| Modal no cierra | Bug JS | Recargar página |

### 7.2 Seguridad

| Check | Estado |
|-------|--------|
| Sin hardcode de URLs | ✅ Usa `window.location.origin` |
| XSS prevention | ✅ `escapeHtml()` en render |
| CORS headers | ✅ Configurado en API |
| Confirmación delete | ✅ RF-14 |

---

## 8. Endpoints Usados

| Endpoint | Método | Uso en Frontend |
|----------|--------|-----------------|
| `/api/auth/login` | POST | `handleLogin()` |
| `/api/auth/logout` | POST | `handleLogout()` |
| `/api/notas` | GET | `loadNotas()` |
| `/api/notas` | POST | `handleSaveNota()` |
| `/api/notas?id=xxx` | DELETE | `deleteNota()` |

---

## 9. Diseño Visual

### Color Palette

| Variable | Color | Uso |
|----------|-------|-----|
| `--primary` | #6366f1 | Botones principales |
| `--success` | #10b981 | Éxito, crear |
| `--danger` | #ef4444 | Eliminar, error |
| `--warning` | #f59e0b | Timer, alertas |

### Animaciones

| Animación | Uso |
|-----------|-----|
| `fadeIn` | Modal aparece |
| `scaleIn` | Contenido modal |
| `slideIn` | Alertas |
| `pulse` | Timer en warning |

---

> **Documento generado:** 2025-12-24  
> **Requiere:** Servidor corriendo en `python api/index.py`
