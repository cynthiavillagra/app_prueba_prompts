# 📊 Fase 2: Análisis de Requisitos

> **Proyecto:** CRUD Didáctico con Supabase  
> **Versión:** 1.0.0  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `docs/01_planificacion.md`  
> **Stack:** Python POO (sin frameworks)

---

## 1. Definición de Requisitos

### 1.1 Requisitos Funcionales (Metodología MoSCoW)

#### 🔴 MUST HAVE (Obligatorios)

| ID | Requisito | Descripción | Módulo |
|----|-----------|-------------|--------|
| RF-01 | Registro de usuario | El sistema debe permitir crear cuentas con email y contraseña | AUTH |
| RF-02 | Inicio de sesión | El sistema debe autenticar usuarios con email y contraseña | AUTH |
| RF-03 | Cierre de sesión | El sistema debe permitir cerrar la sesión activa | AUTH |
| RF-04 | Protección de rutas | Las rutas privadas deben redirigir a login si no hay sesión | AUTH |
| RF-05 | Crear nota | El usuario autenticado debe poder crear una nueva nota | NOTAS |
| RF-06 | Listar notas | El usuario debe ver únicamente sus propias notas | NOTAS |
| RF-07 | Editar nota | El usuario debe poder modificar sus notas existentes | NOTAS |
| RF-08 | Eliminar nota | El usuario debe poder eliminar sus notas con confirmación | NOTAS |
| RF-09 | Aislamiento de datos | Los usuarios NO deben ver ni modificar notas de otros | SEGURIDAD |

#### 🟡 SHOULD HAVE (Deseables)

| ID | Requisito | Descripción | Módulo |
|----|-----------|-------------|--------|
| RF-10 | Validación de inputs | Los inputs deben validar campos obligatorios antes de procesar | UI |
| RF-11 | Estados de carga | La UI debe mostrar indicadores durante operaciones | UI |
| RF-12 | Mensajes de feedback | El sistema debe mostrar mensajes de éxito o error claros | UI |
| RF-13 | Interfaz clara | La interfaz CLI debe ser intuitiva y fácil de usar | UI |
| RF-14 | Confirmación de eliminación | Solicitar confirmación antes de eliminar una nota | UI |

#### 🟢 COULD HAVE (Opcionales)

| ID | Requisito | Descripción | Módulo |
|----|-----------|-------------|--------|
| RF-15 | Persistir sesión | La sesión debe persistir mientras el programa esté en ejecución | AUTH |
| RF-16 | Ordenar notas por fecha | Las notas deben mostrarse ordenadas (más recientes primero) | NOTAS |
| RF-17 | Fecha de última edición | Mostrar cuándo fue editada cada nota | NOTAS |

#### ⚪ WON'T HAVE (Excluidos de esta versión)

| ID | Requisito | Razón de Exclusión |
|----|-----------|-------------------|
| RF-X1 | Login con Google OAuth | Complejidad adicional, se implementará en v2 |
| RF-X2 | Roles de usuario (admin) | Fuera del alcance MVP |
| RF-X3 | Búsqueda de notas | Se agregará en iteración futura |
| RF-X4 | Modo demo sin login | Baja prioridad |
| RF-X5 | Exportar notas a PDF | Feature avanzado para v2 |

---

### 1.2 Requisitos No Funcionales

#### 🔒 Seguridad (SEC)

| ID | Requisito | Especificación | Verificación |
|----|-----------|----------------|--------------|
| RNF-SEC-01 | Credenciales en variables de entorno | Cero hardcode de claves en código fuente | Grep en codebase |
| RNF-SEC-02 | Autenticación JWT | Tokens firmados, no sesiones en servidor | Inspeccionar cookies |
| RNF-SEC-03 | Row Level Security | Todas las tablas con RLS activo | Query directo a Supabase |
| RNF-SEC-04 | Conexión segura | Supabase usa HTTPS por defecto | Verificar URL |
| RNF-SEC-05 | Sanitización de inputs | Prevenir inyección SQL | Supabase SDK lo maneja |

#### ⚡ Rendimiento (PERF)

| ID | Requisito | Especificación | Verificación |
|----|-----------|----------------|--------------|
| RNF-PERF-01 | Respuesta rápida | < 2 segundos para operaciones CRUD | Medición en consola |
| RNF-PERF-02 | Sin bloqueos | Operaciones no bloquean la interfaz | Prueba manual |
| RNF-PERF-03 | Conexión eficiente | Singleton para cliente Supabase | Code review |

#### 🏗️ Arquitectura (ARCH)

| ID | Requisito | Especificación | Verificación |
|----|-----------|----------------|--------------|
| RNF-ARCH-01 | Principios POO | Clases con responsabilidades definidas | Code review |
| RNF-ARCH-02 | Patrones de diseño | Singleton, Adapter, Strategy implementados | Code review |
| RNF-ARCH-03 | Separación de responsabilidades | Código organizado por capas | Estructura de carpetas |

#### 🔄 Mantenibilidad (MAINT)

| ID | Requisito | Especificación | Verificación |
|----|-----------|----------------|--------------|
| RNF-MAINT-01 | Código comentado | Comentarios explican "por qué" | Code review |
| RNF-MAINT-02 | Documentación completa | Manual de replicación en docs/ | Archivos presentes |
| RNF-MAINT-03 | Control de versiones | Git con commits semánticos | Historial de Git |

#### 📱 Usabilidad (UX)

| ID | Requisito | Especificación | Verificación |
|----|-----------|----------------|--------------|
| RNF-UX-01 | CLI intuitivo | Menú claro con opciones numeradas | Prueba manual |
| RNF-UX-02 | Feedback inmediato | Usuario siempre sabe qué está pasando | Prueba manual |
| RNF-UX-03 | Sin opciones rotas | Toda opción del menú tiene función | Prueba manual |

---

## 2. Análisis Funcional Detallado

### 2.1 Historias de Usuario

#### HU-01: Registro de Usuario

```
COMO       usuario nuevo
QUIERO     crear una cuenta con mi email y contraseña
PARA       poder acceder a la aplicación y gestionar mis notas

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que estoy en la página de registro
  Cuando ingreso un email válido y contraseña (mínimo 6 caracteres)
  Y hago clic en "Registrarse"
  Entonces mi cuenta se crea y puedo iniciar sesión

✓ Dado que intento registrarme con un email ya usado
  Cuando hago clic en "Registrarse"
  Entonces veo un mensaje de error indicando que el email ya existe

✓ Dado que la contraseña tiene menos de 6 caracteres
  Cuando intento registrarme
  Entonces veo un mensaje de error de validación

TRAZABILIDAD:
─────────────
→ RF-01 (Registro de usuario)
→ RNF-SEC-02 (Autenticación JWT)
```

#### HU-02: Inicio de Sesión

```
COMO       usuario registrado
QUIERO     iniciar sesión con mi email y contraseña
PARA       acceder a mis notas personales

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que tengo una cuenta válida
  Cuando ingreso credenciales correctas y hago clic en "Iniciar Sesión"
  Entonces soy redirigido a la lista de mis notas

✓ Dado que ingreso credenciales incorrectas
  Cuando hago clic en "Iniciar Sesión"
  Entonces veo un mensaje de error genérico (sin revelar si el email existe)

✓ Dado que inicio sesión exitosamente
  Cuando cierro el navegador y lo vuelvo a abrir
  Entonces sigo autenticado (sesión persistente)

TRAZABILIDAD:
─────────────
→ RF-02 (Inicio de sesión)
→ RF-15 (Recordar sesión)
→ RNF-SEC-02 (Autenticación JWT)
```

#### HU-03: Cierre de Sesión

```
COMO       usuario autenticado
QUIERO     poder cerrar mi sesión
PARA       proteger mi cuenta en dispositivos compartidos

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que estoy autenticado
  Cuando hago clic en "Cerrar Sesión"
  Entonces mi sesión se destruye y soy redirigido a la página de login

✓ Dado que cerré mi sesión
  Cuando intento acceder a /notas directamente
  Entonces soy redirigido a la página de login

TRAZABILIDAD:
─────────────
→ RF-03 (Cierre de sesión)
→ RF-04 (Protección de rutas)
```

#### HU-04: Crear Nota

```
COMO       usuario autenticado
QUIERO     crear una nueva nota con título y contenido
PARA       almacenar información importante

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que estoy en la lista de notas
  Cuando hago clic en "Nueva Nota"
  Entonces veo un formulario con campos para título y contenido

✓ Dado que completo el formulario con título (obligatorio) y contenido
  Cuando hago clic en "Guardar"
  Entonces la nota se crea, aparece en mi lista, y veo un mensaje de éxito

✓ Dado que intento guardar sin título
  Cuando hago clic en "Guardar"
  Entonces veo un mensaje de error indicando que el título es obligatorio

✓ Dado que creo una nota
  Cuando otro usuario inicia sesión
  Entonces ese usuario NO puede ver mi nota

TRAZABILIDAD:
─────────────
→ RF-05 (Crear nota)
→ RF-09 (Aislamiento de datos)
→ RF-10 (Validación de formularios)
→ RNF-SEC-03 (Row Level Security)
```

#### HU-05: Listar Notas

```
COMO       usuario autenticado
QUIERO     ver todas mis notas en una lista
PARA       tener una visión general de mi información

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que tengo notas creadas
  Cuando accedo a la página de notas
  Entonces veo una lista con todas mis notas mostrando título y fecha

✓ Dado que no tengo notas
  Cuando accedo a la página de notas
  Entonces veo un mensaje "No tienes notas aún" con botón para crear

✓ Dado que otro usuario tiene notas
  Cuando accedo a mi lista
  Entonces SOLO veo mis propias notas

✓ Dado que tengo varias notas
  Cuando accedo a la lista
  Entonces las notas aparecen ordenadas por fecha (más recientes primero)

TRAZABILIDAD:
─────────────
→ RF-06 (Listar notas)
→ RF-09 (Aislamiento de datos)
→ RF-16 (Ordenar por fecha)
```

#### HU-06: Editar Nota

```
COMO       usuario autenticado
QUIERO     editar una nota existente
PARA       actualizar o corregir información

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que estoy viendo la lista de notas
  Cuando hago clic en una nota
  Entonces veo el formulario de edición con los datos actuales

✓ Dado que modifico el título o contenido
  Cuando hago clic en "Guardar"
  Entonces los cambios se persisten y veo un mensaje de éxito

✓ Dado que edito una nota
  Cuando vuelvo a la lista
  Entonces veo la fecha de actualización reflejada

✓ Dado que intento acceder a una nota de otro usuario por URL
  Cuando navego a /notas/[id-ajeno]
  Entonces veo un error 404 o soy redirigido (no puedo ver esa nota)

TRAZABILIDAD:
─────────────
→ RF-07 (Editar nota)
→ RF-09 (Aislamiento de datos)
→ RF-17 (Fecha de última edición)
```

#### HU-07: Eliminar Nota

```
COMO       usuario autenticado
QUIERO     eliminar una nota que ya no necesito
PARA       mantener mi lista organizada

CRITERIOS DE ACEPTACIÓN:
─────────────────────────
✓ Dado que estoy viendo una nota o la lista
  Cuando hago clic en "Eliminar"
  Entonces veo un diálogo de confirmación

✓ Dado que confirmo la eliminación
  Cuando hago clic en "Sí, eliminar"
  Entonces la nota desaparece de mi lista y veo un mensaje de éxito

✓ Dado que cancelo la eliminación
  Cuando hago clic en "Cancelar"
  Entonces la nota permanece intacta

TRAZABILIDAD:
─────────────
→ RF-08 (Eliminar nota)
→ RF-14 (Confirmación de eliminación)
```

---

### 2.2 Casos de Uso (Formato Estricto)

#### CU-01: Gestionar Autenticación

```
┌─────────────────────────────────────────────────────────────┐
│ CASO DE USO: CU-01 - Gestionar Autenticación               │
├─────────────────────────────────────────────────────────────┤
│ Actor Principal: Usuario (registrado o no)                  │
│ Precondiciones: La aplicación está disponible              │
│ Postcondiciones: Usuario autenticado o no autenticado      │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO PRINCIPAL: Registro                              │
│ 1. Usuario accede a /login                                 │
│ 2. Sistema muestra formulario con tabs Login/Registro      │
│ 3. Usuario selecciona tab "Registro"                       │
│ 4. Usuario ingresa email y contraseña                      │
│ 5. Usuario hace clic en "Registrarse"                      │
│ 6. Sistema valida campos                                   │
│ 7. Sistema crea cuenta en Supabase Auth                    │
│ 8. Sistema redirige a lista de notas                       │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO ALTERNATIVO: Login                               │
│ 3a. Usuario permanece en tab "Login"                       │
│ 4a. Usuario ingresa credenciales existentes                │
│ 5a. Usuario hace clic en "Iniciar Sesión"                  │
│ 6a. Sistema valida credenciales con Supabase               │
│ 7a. Sistema establece sesión JWT                           │
│ 8a. Sistema redirige a lista de notas                      │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO ALTERNATIVO: Logout                              │
│ 1b. Usuario autenticado hace clic en "Cerrar Sesión"       │
│ 2b. Sistema destruye token JWT                             │
│ 3b. Sistema redirige a /login                              │
├─────────────────────────────────────────────────────────────┤
│ EXCEPCIONES:                                               │
│ E1. Email ya registrado → Mostrar error                    │
│ E2. Credenciales inválidas → Mostrar error genérico        │
│ E3. Campos vacíos → Mostrar validación                     │
│ E4. Error de red → Mostrar mensaje de reintento            │
├─────────────────────────────────────────────────────────────┤
│ TRAZABILIDAD: RF-01, RF-02, RF-03, RF-04                   │
└─────────────────────────────────────────────────────────────┘
```

#### CU-02: Gestionar Notas (CRUD)

```
┌─────────────────────────────────────────────────────────────┐
│ CASO DE USO: CU-02 - Gestionar Notas                       │
├─────────────────────────────────────────────────────────────┤
│ Actor Principal: Usuario autenticado                        │
│ Precondiciones: Usuario ha iniciado sesión                 │
│ Postcondiciones: Notas creadas/modificadas/eliminadas      │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO PRINCIPAL: Listar Notas                          │
│ 1. Usuario accede a /notas                                 │
│ 2. Sistema verifica sesión activa                          │
│ 3. Sistema consulta notas WHERE user_id = auth.uid()       │
│ 4. Sistema renderiza lista ordenada por fecha DESC         │
│ 5. Usuario ve sus notas (o mensaje si no tiene)            │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO ALTERNATIVO: Crear Nota                          │
│ 5a. Usuario hace clic en "Nueva Nota"                      │
│ 6a. Sistema muestra formulario vacío                       │
│ 7a. Usuario completa título y contenido                    │
│ 8a. Usuario hace clic en "Guardar"                         │
│ 9a. Sistema valida campos obligatorios                     │
│ 10a. Sistema inserta en BD con user_id = auth.uid()        │
│ 11a. Sistema redirige a lista con mensaje de éxito         │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO ALTERNATIVO: Editar Nota                         │
│ 5b. Usuario hace clic en una nota existente                │
│ 6b. Sistema carga datos de la nota                         │
│ 7b. Usuario modifica título y/o contenido                  │
│ 8b. Usuario hace clic en "Guardar"                         │
│ 9b. Sistema actualiza en BD y updated_at = now()           │
│ 10b. Sistema redirige a lista con mensaje de éxito         │
├─────────────────────────────────────────────────────────────┤
│ ESCENARIO ALTERNATIVO: Eliminar Nota                       │
│ 5c. Usuario hace clic en icono "Eliminar" de una nota      │
│ 6c. Sistema muestra diálogo de confirmación                │
│ 7c. Usuario confirma eliminación                           │
│ 8c. Sistema elimina de BD                                  │
│ 9c. Sistema actualiza lista con mensaje de éxito           │
├─────────────────────────────────────────────────────────────┤
│ EXCEPCIONES:                                               │
│ E1. Sesión expirada → Redirigir a /login                   │
│ E2. Nota no encontrada → Mostrar 404                       │
│ E3. Intento de acceder a nota ajena → Denegar (RLS)        │
│ E4. Error de BD → Mostrar mensaje y permitir reintento     │
├─────────────────────────────────────────────────────────────┤
│ TRAZABILIDAD: RF-05, RF-06, RF-07, RF-08, RF-09            │
└─────────────────────────────────────────────────────────────┘
```

---

### 2.3 Diagrama de Flujo de Usuario

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUJO PRINCIPAL DE USUARIO                       │
└─────────────────────────────────────────────────────────────────────┘

    ┌─────────┐
    │ INICIO  │
    └────┬────┘
         │
         ▼
    ┌─────────────┐     NO     ┌─────────────┐
    │ ¿Autenticado?├──────────►│   /login    │
    └──────┬──────┘            └──────┬──────┘
           │ SÍ                       │
           │                          ▼
           │                 ┌────────────────┐
           │                 │ ¿Tiene cuenta? │
           │                 └───────┬────────┘
           │                    SÍ   │   NO
           │               ┌─────────┴─────────┐
           │               ▼                   ▼
           │        ┌───────────┐       ┌───────────┐
           │        │   Login   │       │ Registro  │
           │        └─────┬─────┘       └─────┬─────┘
           │              │                   │
           │              └─────────┬─────────┘
           │                        │ Éxito
           ▼                        ▼
    ┌─────────────────────────────────────────┐
    │              /notas (Lista)             │
    │  ┌─────────────────────────────────┐    │
    │  │  [+ Nueva Nota]                 │    │
    │  │  ┌───────────────────────────┐  │    │
    │  │  │ Nota 1        [✏️] [🗑️]  │  │    │
    │  │  │ Nota 2        [✏️] [🗑️]  │  │    │
    │  │  │ ...                       │  │    │
    │  │  └───────────────────────────┘  │    │
    │  │                                 │    │
    │  │  [Cerrar Sesión]                │    │
    │  └─────────────────────────────────┘    │
    └─────────────────────────────────────────┘
         │           │            │
         │ Nueva     │ Editar     │ Eliminar
         ▼           ▼            ▼
    ┌─────────┐ ┌─────────┐ ┌─────────────┐
    │ /nueva  │ │ /[id]   │ │ Confirmar?  │
    │         │ │         │ │  [Sí] [No]  │
    │ Form    │ │ Form    │ └──────┬──────┘
    │ ────────│ │ ────────│        │ Sí
    │ Título  │ │ Título  │        ▼
    │ Contenido│ │Contenido│  DELETE nota
    │ [Guardar]│ │[Guardar]│        │
    └────┬────┘ └────┬────┘        │
         │           │             │
         └───────────┴─────────────┘
                     │
                     ▼
              Volver a /notas
```

---

## 3. Modularización

### 3.1 Arquitectura de Módulos

Siguiendo el principio de **Separación de Responsabilidades (SoC)**, el sistema se organiza en los siguientes módulos lógicos:

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MODULAR (PYTHON)            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   MÓDULO: AUTH                       │   │
│  │  Responsabilidad: Autenticación y autorización      │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Componentes:                                       │   │
│  │  • src/services/auth_service.py (AuthService)       │   │
│  │  • src/services/session_manager.py (SessionManager) │   │
│  │  • IAuthStrategy, EmailPasswordStrategy             │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Requisitos: RF-01, RF-02, RF-03, RF-04, RF-15      │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   MÓDULO: NOTAS                      │   │
│  │  Responsabilidad: CRUD de notas del usuario         │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Componentes:                                       │   │
│  │  • src/services/notas_service.py (NotasService)     │   │
│  │  • src/models/nota.py (clase Nota)                  │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Requisitos: RF-05, RF-06, RF-07, RF-08, RF-16, RF-17│   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   MÓDULO: UI                         │   │
│  │  Responsabilidad: Interfaz de línea de comandos     │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Componentes:                                       │   │
│  │  • src/ui/menu.py (menú interactivo CLI)            │   │
│  │  • Funciones: input(), print()                      │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Requisitos: RF-10, RF-11, RF-12, RF-13, RF-14      │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   MÓDULO: CORE                       │   │
│  │  Responsabilidad: Infraestructura compartida        │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Componentes:                                       │   │
│  │  • src/repositories/supabase_client.py (Singleton)  │   │
│  │  • src/config/settings.py (configuración .env)      │   │
│  │  • .env (variables de entorno)                      │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Requisitos: RNF-SEC-01, RNF-ARCH-01, RNF-ARCH-02   │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   MÓDULO: DATA                       │   │
│  │  Responsabilidad: Modelo y seguridad de datos       │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Componentes:                                       │   │
│  │  • database/init.sql (script SQL)                   │   │
│  │  • src/models/user.py (clase User)                  │   │
│  │  • Políticas RLS en Supabase Dashboard              │   │
│  │  ───────────────────────────────────────────────    │   │
│  │  Requisitos: RF-09, RNF-SEC-03, RNF-SEC-05          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Matriz de Trazabilidad Completa

| Requisito | Módulo | Archivo Principal | Historia de Usuario | Caso de Uso |
|-----------|--------|-------------------|---------------------|-------------|
| RF-01 | AUTH | auth_service.py | HU-01 | CU-01 |
| RF-02 | AUTH | auth_service.py | HU-02 | CU-01 |
| RF-03 | AUTH | session_manager.py | HU-03 | CU-01 |
| RF-04 | AUTH | menu.py | HU-02, HU-03 | CU-01 |
| RF-05 | NOTAS | notas_service.py | HU-04 | CU-02 |
| RF-06 | NOTAS | notas_service.py | HU-05 | CU-02 |
| RF-07 | NOTAS | notas_service.py | HU-06 | CU-02 |
| RF-08 | NOTAS | notas_service.py | HU-07 | CU-02 |
| RF-09 | DATA | init.sql | HU-04, HU-05, HU-06 | CU-02 |
| RF-10 | UI | menu.py | HU-04 | CU-02 |
| RF-11 | UI | menu.py | - | - |
| RF-12 | UI | menu.py | - | - |
| RF-13 | UI | menu.py | - | - |
| RF-14 | UI | menu.py | HU-07 | CU-02 |
| RF-15 | AUTH | session_manager.py | HU-02 | CU-01 |
| RF-16 | NOTAS | notas_service.py | HU-05 | CU-02 |
| RF-17 | NOTAS | nota.py | HU-06 | CU-02 |

### 3.3 Dependencias entre Módulos

```
┌─────────────────────────────────────────────────────────────┐
│               DIAGRAMA DE DEPENDENCIAS                      │
└─────────────────────────────────────────────────────────────┘

    ┌────────┐
    │  AUTH  │◄──────────────────────────────┐
    └───┬────┘                               │
        │ depende de                         │
        ▼                                    │
    ┌────────┐     ┌────────┐               │
    │  CORE  │◄────│  DATA  │               │
    └────────┘     └────────┘               │
        ▲                                    │
        │ depende de                         │
    ┌───┴────┐                               │
    │ NOTAS  │───────────────────────────────┤ usa auth para
    └───┬────┘                               │ validar usuario
        │ depende de                         │
        ▼                                    │
    ┌────────┐                               │
    │   UI   │───────────────────────────────┘
    └────────┘

LEYENDA:
────────
A ──► B  significa "A depende de B"
A ◄── B  significa "B depende de A"
```

---

## 4. Resumen de Entregables de Fase 2

| Artefacto | Estado | Ubicación |
|-----------|--------|-----------|
| Requisitos Funcionales MoSCoW | ✅ Completo | Sección 1.1 |
| Requisitos No Funcionales | ✅ Completo | Sección 1.2 |
| Historias de Usuario (7) | ✅ Completo | Sección 2.1 |
| Casos de Uso (2) | ✅ Completo | Sección 2.2 |
| Diagrama de Flujo | ✅ Completo | Sección 2.3 |
| Modularización | ✅ Completo | Sección 3 |
| Matriz de Trazabilidad | ✅ Completo | Sección 3.2 |

---

## 5. Próximos Pasos

1. ✅ **Fase 1 Completada:** Planificación
2. ✅ **Fase 2 Completada:** Análisis
3. 🔜 **Fase 3 Pendiente:** Diseño de Arquitectura
   - Diagrama de componentes
   - Diseño de base de datos (DDL)
   - Diseño de API
   - Wireframes de UI

---

> **Documento generado:** 2025-12-23  
> **Trazabilidad:** Este documento está vinculado a `01_planificacion.md`
