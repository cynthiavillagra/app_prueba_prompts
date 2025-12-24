# 📘 Manual Técnico: settings.py

> **Archivo:** `src/config/settings.py`  
> **Tipo:** Singleton de Configuración  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `settings.py` centraliza toda la configuración de la aplicación, cargando variables de entorno desde el archivo `.env` y proporcionando acceso seguro a credenciales.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | CORE |
| **Requisito** | RNF-SEC-01 (Credenciales en variables de entorno) |
| **Historia de Usuario** | Transversal (todas las HU necesitan configuración) |
| **Criterio de Aceptación** | Cero hardcode de claves en código fuente |
| **Caso de Uso** | Todos |
| **Escenario** | Inicialización de la aplicación |

---

## 2. Estrategia de Construcción

### Patrón Singleton

```
┌─────────────────────────────────────────────────────────────┐
│                    PATRÓN SINGLETON                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Primera llamada:                                          │
│   Settings() ──► __new__() ──► Crea instancia               │
│              ──► __init__() ──► Carga .env                  │
│              ──► _validate() ──► Verifica variables         │
│                                                             │
│   Llamadas posteriores:                                     │
│   Settings() ──► __new__() ──► Devuelve instancia existente │
│              ──► __init__() ──► No recarga (ya inicializado)│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Dependencias

| Librería | Uso | Versión |
|----------|-----|---------|
| `os` | Acceso a variables de entorno | Built-in |
| `python-dotenv` | Carga de archivo .env | >=1.0.0 |
| `typing` | Type hints | Built-in |

---

## 3. Aclaración Metodológica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` implementa una **prueba atómica** que:

1. **Verifica carga de configuración** - Settings carga correctamente
2. **Verifica patrón Singleton** - Misma instancia en múltiples llamadas
3. **Audita secretos** - No hay claves hardcodeadas en el código

**No es un test unitario tradicional** (pytest), sino una **prueba de fuego** rápida que permite validar el archivo de forma aislada.

---

## 4. Código Fuente

### Ubicación

```
src/
└── config/
    ├── __init__.py
    └── settings.py    ◄── Este archivo
```

### Variables de Configuración

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `supabase_url` | str | - | URL del proyecto Supabase (requerido) |
| `supabase_key` | str | - | Anon key de Supabase (requerido) |
| `session_timeout_seconds` | int | 900 | Timeout de inactividad (15 min) |
| `is_vercel` | bool | False | Detecta entorno Vercel |
| `debug` | bool | False | Modo debug para desarrollo |

### Métodos Públicos

| Método | Retorno | Descripción |
|--------|---------|-------------|
| `__new__()` | Settings | Retorna instancia única (Singleton) |
| `get_masked_key()` | str | Key parcialmente oculta para logs |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
# Desde la raíz del proyecto
cd "c:\Users\...\app_prueba_prompts"

# Activar entorno virtual
venv\Scripts\activate

# Ejecutar prueba atómica
python src/config/settings.py
```

### 5.2 Resultado Esperado (OK)

```
============================================================
PRUEBA DE FUEGO: Settings (Singleton)
============================================================
✅ Settings cargado correctamente
   URL: https://xxx.supabase.co
   Key: eyJhb...xxxxx
   Timeout: 900s
   Is Vercel: False
   Debug: False
✅ Singleton verificado: misma instancia
✅ Auditoría de secretos: OK (sin claves hardcodeadas)
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

### 5.3 Resultado Error (Falta .env)

```
❌ Error de configuración: Variables de entorno faltantes: SUPABASE_URL, SUPABASE_KEY. Copia .env.example a .env y completa los valores.
   Solución: Copia .env.example a .env y completa los valores
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| Singleton con `__new__` | Control explícito de instanciación |
| `load_dotenv()` sin override | Variables de sistema tienen prioridad |
| Validación en `__init__` | Falla rápido si falta configuración |
| `get_masked_key()` | Logging seguro sin exponer credenciales |
| Type hints | Mejor documentación y autocompletado |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Variables globales | Sin encapsulación, difícil de testear |
| Decorador @singleton | Menos explícito, más "mágico" |
| Archivo JSON de config | Menos seguro, no estándar |
| Valores por defecto para URLs | Fallaría silenciosamente |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Variables faltantes` | No existe `.env` | Copiar `.env.example` a `.env` |
| `ModuleNotFoundError: dotenv` | Dependencia no instalada | `pip install python-dotenv` |
| `Key: ***` (muy corta) | Key incorrecta en `.env` | Verificar formato de la key |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel/Docker |
|---------|-------|---------------|
| Archivo `.env` | Sí, en raíz | No existe |
| Variables | Cargadas de `.env` | Cargadas de entorno |
| `is_vercel` | `False` | `True` |
| Prioridad | `.env` | Variables de sistema |

### 7.3 Seguridad

**Auditoría de Secretos:**
- ✅ No hay URLs de Supabase hardcodeadas
- ✅ No hay API keys en el código
- ✅ `.env` está en `.gitignore`
- ✅ `get_masked_key()` para logging seguro

---

## 8. Compatibilidad Serverless

| Check | Estado |
|-------|--------|
| Sin estado global mutable | ✅ |
| Sin archivos temporales | ✅ |
| Carga desde env vars | ✅ |
| Falla rápido si falta config | ✅ |

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `src/repositories/supabase_client.py`
