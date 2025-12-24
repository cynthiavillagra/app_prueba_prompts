# 📋 Manual de Ejecución y Validación Final

> **Documento:** `docs/05_manual_testing.md`  
> **Tipo:** Guía de Ejecución de Tests  
> **Fecha:** 2025-12-24  
> **Versión:** 1.0.0

---

## 1. Objetivo

Este manual explica cómo ejecutar los tests automáticos y realizar la validación manual UAT.

---

## PARTE A: Tests Automáticos

### A.1 Prerrequisitos

```powershell
# 1. Activar entorno virtual
cd "c:\Users\Cynthia\OneDrive\Escritorio\EDUCACION\00 Pedagogia\app_prueba_prompts"
venv\Scripts\activate

# 2. Instalar pytest (si no está instalado)
pip install pytest

# 3. Verificar instalación
pytest --version
```

### A.2 Ejecutar Todos los Tests

```powershell
# Ejecutar todos los tests con output verbose
pytest tests/ -v

# Ejecutar con reporte de cobertura resumido
pytest tests/ -v --tb=short
```

### A.3 Ejecutar Tests por Módulo

```powershell
# Solo tests de modelos
pytest tests/test_models.py -v

# Solo tests de servicios
pytest tests/test_services.py -v

# Solo tests de API
pytest tests/test_api.py -v
```

### A.4 Ejecutar Tests por Marker

```powershell
# Solo tests unitarios
pytest tests/ -v -m unit

# Solo tests de integración (si los hubiera)
pytest tests/ -v -m integration
```

### A.5 Resultado Esperado

```
========================== test session starts ==========================
platform win32 -- Python 3.11.x, pytest-x.x.x
collected XX items

tests/test_api.py::TestVercelBridge::test_health_check_get PASSED
tests/test_api.py::TestVercelBridge::test_health_check_root PASSED
tests/test_api.py::TestVercelBridge::test_unknown_route_returns_404 PASSED
...
tests/test_models.py::TestUser::test_user_creation_basic PASSED
tests/test_models.py::TestUser::test_user_from_dict PASSED
...
tests/test_services.py::TestSessionManager::test_singleton_pattern PASSED
...

========================== XX passed in X.XXs ============================
```

### A.6 Troubleshooting Tests

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError` | Path incorrecto | Ejecutar desde raíz del proyecto |
| `pytest not found` | No instalado | `pip install pytest` |
| Tests fallan por env | .env no cargado | Los tests usan mocks, no .env |

---

## PARTE B: Validación Manual Humana (UAT)

### B.1 Preparación del Ambiente

1. **Terminal 1** - Servidor:
```powershell
cd "c:\Users\Cynthia\OneDrive\Escritorio\EDUCACION\00 Pedagogia\app_prueba_prompts"
venv\Scripts\activate
python api/index.py
```

2. **Navegador** - Cliente:
```
Abrir: http://localhost:8000
```

### B.2 Ejecutar Flujos UAT

Seguir los pasos detallados en `docs/05_plan_uat.md`:

#### Flujo 1: Autenticación
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Errores se muestran correctamente

#### Flujo 2: CRUD Notas
- [ ] Crear nota funciona
- [ ] Listar notas funciona
- [ ] Editar nota funciona
- [ ] Eliminar nota funciona (con confirmación)

#### Flujo 3: Timeout Sesión
- [ ] Timer visible y funciona
- [ ] Modal aparece al expirar
- [ ] Redirección a login funciona

### B.3 Checklist de Validación

| Ítem | Verificación | ✓ |
|------|--------------|---|
| **Frontend** | Carga correctamente | |
| **Login** | Autentica con Supabase | |
| **CRUD** | Las 4 operaciones funcionan | |
| **Timer** | Cuenta regresiva visible | |
| **Modal** | Aparece al expirar | |
| **Responsive** | Se ve bien en móvil | |
| **Errores** | Mensajes claros | |
| **Seguridad** | Sin credenciales en consola | |

### B.4 Registro de Resultados

```
╔═══════════════════════════════════════════════════════════════════╗
║              REGISTRO DE VALIDACIÓN UAT                           ║
╠═══════════════════════════════════════════════════════════════════╣
║ Fecha:        _______________________                             ║
║ Ejecutor:     _______________________                             ║
║ Versión:      _______________________                             ║
╠═══════════════════════════════════════════════════════════════════╣
║ Tests Automáticos:  [ ] PASSED  [ ] FAILED                        ║
║ Flujo UAT #1:       [ ] PASSED  [ ] FAILED                        ║
║ Flujo UAT #2:       [ ] PASSED  [ ] FAILED                        ║
║ Flujo UAT #3:       [ ] PASSED  [ ] FAILED                        ║
╠═══════════════════════════════════════════════════════════════════╣
║ RESULTADO FINAL:    [ ] APROBADO  [ ] RECHAZADO                   ║
╠═══════════════════════════════════════════════════════════════════╣
║ Observaciones:                                                    ║
║ _________________________________________________________________║
║ _________________________________________________________________║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## 3. Criterios de Aceptación Final

### Tests Automáticos
- ✅ Todos los tests pasan (100%)
- ✅ Sin errores de sintaxis
- ✅ Sin warnings críticos

### UAT Manual
- ✅ Los 3 flujos completos pasan
- ✅ Sin errores en consola del navegador
- ✅ UX intuitiva y clara

### Seguridad
- ✅ Sin credenciales hardcodeadas
- ✅ Mocks en tests (sin credenciales reales)
- ✅ Variables de entorno correctamente usadas

---

## 4. Próximos Pasos (Post-Validación)

Si todos los tests pasan:

```powershell
# Git checkpoint
git add tests/ docs/
git commit -m "test: formalize unit tests and UAT plan"
git push
```

Si hay fallos:
1. Documentar el error específico
2. Corregir el código
3. Re-ejecutar tests
4. Repetir hasta que pasen

---

> **Documento generado:** 2024-12-24  
> **Requisito:** Tests verdes + UAT OK antes de deploy
