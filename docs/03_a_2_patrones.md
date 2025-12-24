# 🏗️ Fase 3-A (Parte 2): Patrones de Diseño

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `03_a_1_arquitectura.md`

---

## 1. Catálogo de Patrones

| Tipo | Patrón | Uso en el Proyecto |
|------|--------|-------------------|
| Creacional | **Singleton** | Cliente Supabase único |
| Creacional | **Factory Method** | Clientes por contexto (browser/server) |
| Estructural | **Adapter** | Services que encapsulan Supabase |
| Estructural | **Facade** | Hooks como interfaz simple para UI |
| Comportamiento | **Strategy** | Estrategias de autenticación |
| Comportamiento | **Observer** | Estado reactivo de auth |

---

## 2. Singleton: Cliente Supabase

**Propósito:** Una única instancia del cliente en toda la app.

```
Componente A ──┐
Componente B ──┼──► [ Supabase Client ] ──► Supabase API
Componente C ──┤    (Única Instancia)
Middleware ────┘
```

**Ubicación:** `src/lib/supabase.js`

**¿Por qué SÍ?**
- Evita múltiples conexiones
- Centraliza configuración
- Fácil de mockear en tests

---

## 3. Factory Method: Clientes por Contexto

**Propósito:** Crear clientes diferentes según el contexto.

```
createClient() ──┬──► createBrowserClient() → Usa anon key
                 ├──► createServerClient()  → Lee cookies
                 └──► createAdminClient()   → Service role
```

**¿Por qué SÍ?**
- Next.js tiene múltiples entornos
- Cada entorno requiere config diferente

---

## 4. Adapter: Servicios Desacoplados

**Propósito:** Aislar la UI del SDK de Supabase.

```
[ UI Component ] ──► [ notasService ] ──► [ Supabase SDK ]
                     (Adapter)
```

**Ubicación:** `src/lib/services/notasService.js`

**¿Por qué SÍ?**
- Desacopla UI de implementación
- Facilita migración futura
- Centraliza manejo de errores

**¿Por qué NO llamar Supabase desde componentes?**
- Código duplicado
- Difícil de cambiar proveedor
- Complejo de testear

---

## 5. Facade: Hooks como Interfaz Simple

**Propósito:** Ofrecer API simple que oculta complejidad.

```
┌─ LoginPage ─┐
│ ListaPage   │ ──► useAuth() / useNotas() ──► AuthService
│ EditorPage  │     (Facade - Hooks)           NotasService
└─ NuevaPage ─┘
```

**¿Por qué SÍ?**
- Componentes React quedan limpios
- Lógica encapsulada en hooks
- Fácil de testear: mock del hook

---

## 6. Strategy: Autenticación Extensible

**Propósito:** Estrategias de auth intercambiables.

```
AuthContext ──► AuthStrategy (Interfaz)
                    ├── EmailPasswordStrategy ✅ (v1)
                    ├── GoogleOAuthStrategy   🔜 (v2)
                    └── MagicLinkStrategy     🔜 (v2)
```

**¿Por qué SÍ?**
- MVP usa email/password
- v2 puede agregar OAuth sin modificar código existente
- Cumple Open/Closed principle

---

## 7. Observer: Estado Reactivo

**Propósito:** Notificar automáticamente cambios de sesión.

```
Supabase Auth ──► onAuthStateChange() ──┬──► Navbar (re-render)
(Subject)                               ├──► Sidebar (re-render)
                                        └──► Middleware (protege)
```

**¿Por qué SÍ?**
- React Context implementa Observer naturalmente
- Componentes reaccionan automáticamente
- Sin polling manual

---

> **Continúa en:** `03_a_3_stateless.md`
