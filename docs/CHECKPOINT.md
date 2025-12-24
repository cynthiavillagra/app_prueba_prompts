# 📍 CHECKPOINT - Estado del Proyecto

> **Última Actualización:** 2025-12-23T22:22:00-03:00  
> **Proyecto:** CRUD Didáctico con Supabase

---

## 🎯 Estado Actual

| Aspecto | Valor |
|---------|-------|
| **Fase Actual** | Fase 3-C (API y Dinámica) - En Revisión |
| **Próxima Fase** | Fase 4 - Implementación |
| **% Completado** | 45% |

---

## 📚 Stack Definido

```
Frontend:     Next.js 14 (App Router) + React 18
Backend:      Supabase (PostgreSQL + Auth)
Hosting:      Vercel (Serverless)
Estilos:      CSS Vanilla
Lenguaje:     JavaScript (ES6+)
```

---

## 📄 Documentos Generados

| Fase | Archivo | Estado | Fecha |
|------|---------|--------|-------|
| 1 | `docs/01_planificacion.md` | ✅ Completo | 2025-12-23 |
| 2 | `docs/02_analisis.md` | ✅ Completo | 2025-12-23 |
| 3-A | `docs/03_a_1_arquitectura.md` | ✅ Completo | 2025-12-23 |
| 3-A | `docs/03_a_2_patrones.md` | ✅ Completo | 2025-12-23 |
| 3-A | `docs/03_a_3_stateless.md` | ✅ Completo | 2025-12-23 |
| 3-B | `docs/03_b_modelado_datos.md` | ✅ Completo | 2025-12-23 |
| 3-C | `docs/03_c_api_dinamica.md` | ⏳ En revisión | 2025-12-23 |
| - | `docs/CHECKPOINT.md` | ✅ Activo | 2025-12-23 |

---

## 🔌 Endpoints Definidos (Fase 3-C)

| Método | Ruta | Módulo | HU |
|--------|------|--------|-----|
| POST | `/auth/v1/signup` | AUTH | HU-01 |
| POST | `/auth/v1/token` | AUTH | HU-02 |
| POST | `/auth/v1/logout` | AUTH | HU-03 |
| GET | `/rest/v1/notas` | NOTAS | HU-05 |
| POST | `/rest/v1/notas` | NOTAS | HU-04 |
| PATCH | `/rest/v1/notas?id=eq.{id}` | NOTAS | HU-06 |
| DELETE | `/rest/v1/notas?id=eq.{id}` | NOTAS | HU-07 |

---

## 🔒 Seguridad Definida

| Aspecto | Estrategia |
|---------|------------|
| API Keys | Variables de entorno |
| Sesión | JWT en cookies HttpOnly |
| Watchdog | 15 min inactividad → logout |
| Token expirado | Catch 401 → redirect |
| Aislamiento | Row Level Security |

---

## 📈 Historial de Cambios

| Fecha | Fase | Cambio |
|-------|------|--------|
| 2025-12-23 | 1 | Planificación |
| 2025-12-23 | 2 | Análisis |
| 2025-12-23 | 3-A | Arquitectura y patrones |
| 2025-12-23 | 3-B | Modelado de datos |
| 2025-12-23 | 3-C | API y dinámica (en revisión) |

---

## ⏸️ ESTADO: Esperando Aprobación de Fase 3-C

> **Próxima acción:** Usuario debe aprobar API y seguridad.

---

> *Este archivo se actualiza al final de cada fase.*
