# 🏗️ Fase 3-A (Parte 3): Estrategia Stateless

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `03_a_2_patrones.md`

---

## 1. El Problema: Memoria Volátil en Serverless

```
SERVERLESS (Vercel):

Request 1 ──► [Función Instancia A] ──► Respuesta
                     │ muere
                     ▼
              (memoria borrada)

Request 2 ──► [Función Instancia B] ──► Respuesta (¡DIFERENTE!)

PROBLEMA: Lo guardado en RAM en Request 1 NO existe en Request 2.
```

---

## 2. Reglas Stateless (LEY ABSOLUTA)

### 🚫 TERMINANTEMENTE PROHIBIDO

```javascript
// ❌ Variable global mutable
let sessions = {}
let currentUser = null
let cache = new Map()

// ❌ Almacenar estado en módulo
const store = { user: null, notas: [] }

// ❌ Caché en memoria del servidor
const notasCache = []
function getNotas() {
  if (notasCache.length) return notasCache  // ❌ No persistirá
}
```

### ✅ PERMITIDO Y OBLIGATORIO

```javascript
// ✅ Estado en cliente (React state, Context)
const [user, setUser] = useState(null)

// ✅ Estado en cookies (JWT)
cookies().set('session', jwt, { httpOnly: true })

// ✅ Estado en base de datos (Supabase)
await supabase.from('notas').insert({ ... })

// ✅ Estado en localStorage (solo cliente)
localStorage.setItem('theme', 'dark')
```

---

## 3. Estrategia por Tipo de Estado

| Tipo de Estado | Dónde Almacenar | Cómo |
|----------------|-----------------|------|
| Sesión de usuario | Cookie HttpOnly | Supabase Auth automático |
| Datos de notas | PostgreSQL | Supabase Database |
| Estado de UI (loading) | React State | useState, useContext |
| Preferencias (tema) | localStorage | Solo en cliente |

---

## 4. Flujo de Autenticación Stateless

```
1. LOGIN
   Usuario ──► POST (email, password)
          ──► Supabase Auth valida
          ◄── Devuelve JWT
          ──► Se guarda en cookie HttpOnly

2. REQUEST AUTENTICADO
   Usuario ──► GET /notas
          ──► Cookie JWT viaja automáticamente
          ──► Middleware valida JWT
          ──► RLS filtra por auth.uid()
          ◄── Solo notas del usuario

3. LOGOUT
   Usuario ──► POST /logout
          ──► Elimina cookies
          ──► Invalida refresh_token
```

---

## 5. Watchdog de Inactividad (15 minutos)

### Configuración Supabase
- access_token expira en 15 minutos
- refresh_token solo si hay actividad

### Implementación Cliente

```javascript
// Detectar inactividad
let lastActivity = Date.now()

// Eventos que resetean timer
['click', 'keydown', 'scroll'].forEach(event => {
  document.addEventListener(event, () => {
    lastActivity = Date.now()
  })
})

// Verificar cada minuto
setInterval(() => {
  const inactiveMinutes = (Date.now() - lastActivity) / 60000
  if (inactiveMinutes >= 15) {
    supabase.auth.signOut()
    redirect('/login?reason=inactivity')
  }
}, 60000)
```

---

## 6. Estrategia de Integración APIs

### APIs en el Proyecto

| API | Tipo | Uso |
|-----|------|-----|
| Supabase Auth | BaaS | Autenticación JWT |
| Supabase Database | BaaS | PostgreSQL + RLS |

### Principio de Aislamiento

```javascript
// ❌ PROHIBIDO: Llamar Supabase desde componentes
function MiComponente() {
  const { data } = await supabase.from('notas').select('*')
}

// ✅ CORRECTO: Usar servicios como intermediario
function MiComponente() {
  const { notas } = useNotas()  // Hook usa servicio internamente
}
```

---

## 7. Resumen de Decisiones Arquitectónicas

| ID | Decisión | Patrón | Ubicación |
|----|----------|--------|-----------|
| ADR-06 | Cliente único | Singleton | `lib/supabase.js` |
| ADR-07 | Clientes por contexto | Factory | `lib/supabase.js` |
| ADR-08 | Servicios desacoplados | Adapter | `lib/services/*.js` |
| ADR-09 | Auth extensible | Strategy | `context/AuthContext.js` |
| ADR-10 | Hooks como facade | Facade | `hooks/*.js` |
| ADR-11 | Estado reactivo | Observer | `onAuthStateChange` |
| ADR-12 | Cero variables globales | Stateless | Todo el proyecto |
| ADR-13 | JWT en cookies | Stateless | Supabase Auth |
| ADR-14 | Watchdog 15 min | Seguridad | Componente raíz |

---

## 8. Próximos Pasos

1. ✅ **Fase 3-A Completada:** Arquitectura y Patrones
2. 🔜 **Fase 3-B Pendiente:** Modelado de Datos

---

> **Documento generado:** 2025-12-23
