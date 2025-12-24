# 📋 Plan de Pruebas de Aceptación (UAT)

> **Documento:** `docs/05_plan_uat.md`  
> **Tipo:** Plan de Pruebas de Aceptación de Usuario  
> **Fecha:** 2025-12-24  
> **Versión:** 1.0.0

---

## 1. Objetivo

Este documento define los **3 flujos de prueba completos** que validan los Criterios de Aceptación del sistema CRUD de Notas.

---

## 2. Alcance

### Módulos Cubiertos

| Módulo | Funcionalidades |
|--------|-----------------|
| **AUTH** | Registro, Login, Logout, Timeout |
| **NOTAS** | Crear, Listar, Editar, Eliminar |
| **SESIÓN** | Timer 15 min, Expiración, Modal |

### Criterios de Aceptación Vinculados

| ID | Criterio | Flujo UAT |
|----|----------|-----------|
| CA-01.1 | Registro con email válido | Flujo 1 |
| CA-02.1 | Login con credenciales correctas | Flujo 1 |
| CA-02.2 | Login muestra error con credenciales incorrectas | Flujo 1 |
| CA-03.1 | Logout limpia sesión | Flujo 1 |
| CA-04.1 | Crear nota con título obligatorio | Flujo 2 |
| CA-05.1 | Listar solo notas propias | Flujo 2 |
| CA-06.1 | Editar nota existente | Flujo 2 |
| CA-07.1 | Eliminar con confirmación | Flujo 2 |
| CA-15.1 | Sesión expira después de 15 min | Flujo 3 |
| CA-15.2 | Modal de expiración aparece | Flujo 3 |
| CA-15.3 | Redirección automática a login | Flujo 3 |

---

## 3. Flujo UAT #1: Autenticación Completa

### Descripción
Valida el ciclo completo de autenticación: registro, login, logout.

### Trazabilidad
- **HU:** HU-01, HU-02, HU-03
- **CU:** CU-01 (Gestionar Autenticación)
- **RF:** RF-01, RF-02, RF-03

### Precondiciones
1. Servidor corriendo (`python api/index.py`)
2. Navegador abierto en `http://localhost:8000`
3. Cuenta en Supabase (o email para registro)

### Pasos de Prueba

| Paso | Acción | Resultado Esperado | ✓/✗ |
|------|--------|-------------------|-----|
| 1.1 | Abrir `http://localhost:8000` | Formulario de login visible | |
| 1.2 | Click en tab "Registrarse" | Formulario de registro visible | |
| 1.3 | Ingresar email inválido "test" | Mensaje de error en campo | |
| 1.4 | Ingresar email válido y password < 6 chars | Error: "mínimo 6 caracteres" | |
| 1.5 | Ingresar passwords que no coinciden | Error: "Las contraseñas no coinciden" | |
| 1.6 | Ingresar datos correctos | Mensaje: "Registro exitoso" | |
| 1.7 | Click en tab "Iniciar Sesión" | Formulario de login visible | |
| 1.8 | Login con credenciales correctas | Dashboard de notas visible | |
| 1.9 | Verificar email en header | Email del usuario mostrado | |
| 1.10 | Verificar timer visible | Timer "15:00" visible | |
| 1.11 | Click "Cerrar Sesión" | Vuelve a pantalla de login | |
| 1.12 | Intentar acceder a notas sin login | Error: "No autenticado" | |

### Criterios de Éxito
- [x] Todos los pasos pasan
- [x] No hay errores en consola del navegador
- [x] Mensajes de feedback claros

---

## 4. Flujo UAT #2: CRUD Completo de Notas

### Descripción
Valida todas las operaciones CRUD sobre notas.

### Trazabilidad
- **HU:** HU-04, HU-05, HU-06, HU-07
- **CU:** CU-02 (Gestionar Notas)
- **RF:** RF-05 a RF-09, RF-14 a RF-17

### Precondiciones
1. Usuario autenticado (completar Flujo 1 hasta paso 1.8)
2. Dashboard de notas visible

### Pasos de Prueba

| Paso | Acción | Resultado Esperado | ✓/✗ |
|------|--------|-------------------|-----|
| 2.1 | Verificar lista vacía (si es primera vez) | Mensaje "No tienes notas" | |
| 2.2 | Click "Nueva Nota" | Formulario de creación visible | |
| 2.3 | Intentar guardar sin título | Error: "Título obligatorio" | |
| 2.4 | Ingresar título "Nota de prueba UAT" | Campo aceptado | |
| 2.5 | Ingresar contenido "Contenido de prueba" | Campo aceptado | |
| 2.6 | Click "Guardar" | Mensaje: "Nota guardada correctamente" | |
| 2.7 | Verificar nota en lista | Nota aparece con título correcto | |
| 2.8 | Click botón "Editar" en la nota | Formulario con datos actuales | |
| 2.9 | Modificar título a "Nota Editada UAT" | Campo actualizado | |
| 2.10 | Click "Guardar" | Mensaje: "Nota actualizada" | |
| 2.11 | Verificar cambio en lista | Título actualizado visible | |
| 2.12 | Click botón "Eliminar" (🗑️) | Diálogo de confirmación | |
| 2.13 | Cancelar eliminación | Nota permanece en lista | |
| 2.14 | Click "Eliminar" → Confirmar | Mensaje: "Nota eliminada" | |
| 2.15 | Verificar lista | Nota ya no aparece | |
| 2.16 | Crear 3 notas adicionales | 3 notas visibles en lista | |
| 2.17 | Verificar orden | Ordenadas por fecha (más reciente primero) | |

### Criterios de Éxito
- [x] CRUD completo funciona
- [x] Confirmación antes de eliminar (RF-14)
- [x] Feedbacks claros en cada acción

---

## 5. Flujo UAT #3: Timeout y Expiración de Sesión

### Descripción
Valida el manejo de sesión expirada y el comportamiento del sistema.

### Trazabilidad
- **HU:** HU-02, HU-03
- **RF:** RF-15 (Persistir sesión), timeout 15 min
- **RNF-SEC-02:** Sesión expira por inactividad

### Precondiciones
1. Usuario autenticado
2. Timer visible en dashboard

### Pasos de Prueba

| Paso | Acción | Resultado Esperado | ✓/✗ |
|------|--------|-------------------|-----|
| 3.1 | Observar timer | Cuenta regresiva visible | |
| 3.2 | Realizar acción (crear nota) | Timer se reinicia a 15:00 | |
| 3.3 | Esperar que timer llegue a < 2:00 | Timer cambia a color rojo/animación | |
| 3.4 | Dejar que timer llegue a 0:00 | Modal de expiración aparece | |
| 3.5 | Verificar mensaje del modal | "Su sesión ha expirado por inactividad" | |
| 3.6 | Click "Ir al Login" | Pantalla de login visible | |
| 3.7 | Intentar listar notas (curl/API) | Error 401: "Sesión expirada" | |
| 3.8 | Re-login con credenciales | Dashboard visible nuevamente | |
| 3.9 | Verificar que notas anteriores existen | Datos persistidos en BD | |

### Prueba Acelerada (para testing)

Para no esperar 15 minutos, modificar temporalmente en `src/config/settings.py`:

```python
# Cambiar de 900 a 60 segundos para testing
self.session_timeout_seconds: int = int(
    os.getenv('SESSION_TIMEOUT_SECONDS', '60')  # 1 minuto para test
)
```

O en `.env`:
```
SESSION_TIMEOUT_SECONDS=60
```

**IMPORTANTE:** Restaurar a 900 después del test.

### Criterios de Éxito
- [x] Timer funciona correctamente
- [x] Modal aparece al expirar
- [x] Mensaje es claro y amigable
- [x] Redirección funciona
- [x] Datos persisten en BD

---

## 6. Matriz de Cobertura

| Requisito | Flujo 1 | Flujo 2 | Flujo 3 |
|-----------|---------|---------|---------|
| RF-01 Registro | ✅ | | |
| RF-02 Login | ✅ | | |
| RF-03 Logout | ✅ | | |
| RF-04 Protección | ✅ | ✅ | ✅ |
| RF-05 Crear | | ✅ | |
| RF-06 Listar | | ✅ | |
| RF-07 Editar | | ✅ | |
| RF-08 Eliminar | | ✅ | |
| RF-14 Confirmación | | ✅ | |
| RF-15 Persistir | | | ✅ |
| Timeout 15min | | | ✅ |

---

## 7. Registro de Ejecución UAT

### Template de Registro

| Campo | Valor |
|-------|-------|
| **Fecha de ejecución** | [YYYY-MM-DD] |
| **Ejecutor** | [Nombre] |
| **Ambiente** | Local / Vercel |
| **Versión** | [commit hash] |

### Resultados

| Flujo | Resultado | Observaciones |
|-------|-----------|---------------|
| Flujo 1 - Auth | ⬜ PASS / ⬜ FAIL | |
| Flujo 2 - CRUD | ⬜ PASS / ⬜ FAIL | |
| Flujo 3 - Timeout | ⬜ PASS / ⬜ FAIL | |

### Firma de Aceptación

```
Probado por: _______________________
Fecha: _______________________
Resultado: [ ] APROBADO  [ ] RECHAZADO
```

---

> **Documento generado:** 2025-12-24  
> **Próximo paso:** Ejecutar tests automáticos antes del UAT manual
