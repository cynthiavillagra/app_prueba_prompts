# 📘 Manual Técnico: main.py

> **Archivo:** `main.py`  
> **Tipo:** Entry Point Local  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `main.py` es el **punto de entrada** para ejecutar la aplicación CLI de forma local.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | CORE / INFRAESTRUCTURA |
| **Requisitos** | RNF-ARCH-01, RNF-SEC-01 |
| **Caso de Uso** | Todos (entry point) |
| **Escenario** | Ejecución local |

---

## 2. Estrategia de Construcción

### Orden de Ejecución (Crítico)

```
┌─────────────────────────────────────────────────────────────┐
│                    ORDEN DE CARGA                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [1] from dotenv import load_dotenv                        │
│                    │                                        │
│                    ▼                                        │
│   [2] load_dotenv()  ◄─── ANTES de cualquier import src/    │
│                    │                                        │
│                    ▼                                        │
│   [3] from src.ui.menu import Menu                          │
│        └── Importa Settings (que lee os.getenv)             │
│                    │                                        │
│                    ▼                                        │
│   [4] Menu().run()                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**¿Por qué este orden?**
- `Settings` es Singleton y lee `os.getenv()` en su `__init__`
- Si importamos `Menu` antes de `load_dotenv()`, las variables no existen
- Resultado: `ValueError: Variables faltantes`

---

## 3. Aclaración Metodológica

### 3.1 Rol del Bloque Main

```python
if __name__ == "__main__":
    main()
```

Este bloque:
- Se ejecuta SOLO si el archivo se llama directamente
- NO se ejecuta si se importa como módulo
- Permite testear `main()` sin ejecutarla automáticamente

---

## 4. Código Fuente

### Ubicación

```
proyecto/
├── main.py    ◄── Este archivo (Entry Point Local)
├── api/
│   └── index.py   (Entry Point Vercel - futuro)
└── src/
    └── ...
```

### Manejo de Errores

| Excepción | Causa | Acción |
|-----------|-------|--------|
| `KeyboardInterrupt` | Ctrl+C | Salida graceful |
| `ValueError` | Config faltante | Guía de solución |
| `Exception` | Error inesperado | Log y salida |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
# Desde la raíz del proyecto (venv activado)
python main.py
```

### 5.2 Resultado Esperado

```
==================================================
   📝 CRUD DIDÁCTICO DE NOTAS
   Proyecto con Supabase + Python POO
==================================================

--- MENÚ DE AUTENTICACIÓN ---
1. Iniciar sesión
2. Registrarse
0. Salir

Seleccione una opción: _
```

### 5.3 Error si falta .env

```
❌ Error de configuración: Variables de entorno faltantes: SUPABASE_URL, SUPABASE_KEY

Verifique:
  1. Que existe el archivo .env
  2. Que SUPABASE_URL y SUPABASE_KEY están configurados
  3. Consulte docs/04_a_setup_local.md
```

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| `load_dotenv()` primero | Variables disponibles para Settings |
| `main()` como función | Testeable, reutilizable |
| Manejo de errores | UX amigable |
| sys.exit con códigos | Estándar Unix |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| load_dotenv en Settings | Ya tarde, import previo fallaría |
| Sin try/except | Tracebacks confusos para usuario |
| Código directo sin main() | Menos testeable |

---

## 7. Diferencias Local vs Nube

| Aspecto | Local (main.py) | Vercel (api/index.py) |
|---------|-----------------|----------------------|
| Carga .env | `load_dotenv()` | No necesario |
| Variables | Desde .env | Desde Vercel Dashboard |
| Ejecución | `python main.py` | Automático por request |
| Interfaz | CLI interactivo | HTTP (futuro) |

---

## 8. Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: src` | Path incorrecto | Ejecutar desde raíz proyecto |
| `Variables faltantes` | .env no existe | `copy .env.example .env` |
| `No module named dotenv` | Dependencia faltante | `pip install python-dotenv` |

---

> **Documento generado:** 2025-12-24  
> **Próximo archivo:** `api/index.py` (Entry Point Vercel)
