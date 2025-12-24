# 📝 CRUD Didáctico con Supabase

> **Aplicación CRUD de notas personales** desarrollada con Python POO (sin frameworks web) + Supabase como BaaS.

[![Tests](https://img.shields.io/badge/tests-45%20passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![Supabase](https://img.shields.io/badge/supabase-backend-green)](https://supabase.com)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-orange)](LICENSE)

---

## 🎯 Descripción

Este proyecto es una **aplicación didáctica** que implementa un CRUD completo de notas personales, diseñada para enseñar:

- **Programación Orientada a Objetos** en Python
- **Patrones de Diseño** (Singleton, Strategy, Adapter, Factory)
- **Integración con BaaS** (Backend as a Service - Supabase)
- **Arquitectura por Capas**
- **Metodología SDLC** con documentación completa

---

## ⚠️ ADVERTENCIAS IMPORTANTES

### 🚨 NO APTO PARA PRODUCCIÓN

Este proyecto está diseñado **exclusivamente** para:

| ✅ Uso Permitido | ❌ Uso NO Recomendado |
|-----------------|----------------------|
| MVP / Pruebas de concepto | Producción real |
| Desarrollo local | Datos sensibles |
| Uso pedagógico | Aplicaciones críticas |
| Aprendizaje | Sin auditoría de seguridad |

**Razones:**
- No implementa HTTPS (solo HTTP)
- No tiene rate limiting
- Manejo básico de tokens
- Sin logging de seguridad profesional
- Código no auditado para vulnerabilidades

---

## 🤖 AI Stack

Este proyecto fue desarrollado utilizando **Inteligencia Artificial Generativa**:

| Herramienta | Uso |
|-------------|-----|
| **Google Antigravity** | IDE con asistente de IA integrado |
| **Claude Opus 4** | Generación de código y documentación |

### Metodología de Desarrollo con IA

1. **Prompt Engineering** - Instrucciones detalladas para cada fase SDLC
2. **Ciclo Atómico** - Código → Manual → Test → Aprobación
3. **Revisión Humana** - Validación de cada archivo generado
4. **Documentación Narrativa** - Manuales técnicos explicativos

> ⚠️ **Nota:** El código generado por IA debe ser revisado cuidadosamente antes de cualquier uso.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.11+ |
| **Paradigma** | POO (sin frameworks web) |
| **Base de Datos** | Supabase (PostgreSQL) |
| **Autenticación** | Supabase Auth (JWT) |
| **Cliente DB** | supabase-py 2.x |
| **Variables de Entorno** | python-dotenv |
| **Testing** | pytest |
| **Interfaz CLI** | Menú interactivo |
| **Interfaz Web** | HTML/CSS/JS puro |

---

## 📁 Estructura del Proyecto

```
app_prueba_prompts/
├── 📄 main.py                    # Entry point CLI (local)
├── 📁 api/
│   └── index.py                  # Entry point API + VercelBridge
├── 📁 src/
│   ├── 📁 config/
│   │   └── settings.py           # Configuración (Singleton)
│   ├── 📁 repositories/
│   │   └── supabase_client.py    # Cliente Supabase (Singleton)
│   ├── 📁 models/
│   │   ├── user.py               # Entidad Usuario
│   │   └── nota.py               # Entidad Nota
│   ├── 📁 services/
│   │   ├── session_manager.py    # Gestión de sesión (Singleton)
│   │   ├── auth_service.py       # Autenticación (Strategy)
│   │   └── notas_service.py      # CRUD notas (Adapter)
│   └── 📁 ui/
│       └── menu.py               # Menú CLI
├── 📁 public/
│   └── index.html                # Frontend HTML/CSS/JS
├── 📁 database/
│   └── init.sql                  # Script inicialización BD
├── 📁 tests/
│   ├── conftest.py               # Fixtures pytest
│   ├── test_models.py            # Tests de modelos
│   ├── test_services.py          # Tests de servicios
│   └── test_api.py               # Tests de API
├── 📁 docs/                      # Documentación SDLC (22 docs)
├── 📄 requirements.txt           # Dependencias Python
├── 📄 vercel.json                # Configuración Vercel
├── 📄 Dockerfile                 # Contenedor Docker
├── 📄 Procfile                   # Configuración Heroku
├── 📄 .env.example               # Plantilla de variables
└── 📄 LICENSE                    # CC BY 4.0
```

---

## 🚀 Inicio Rápido

### 1. Clonar y Configurar

```bash
git clone https://github.com/cynthiavillagra/app_prueba_prompts.git
cd app_prueba_prompts

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Supabase

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ejecutar `database/init.sql` en SQL Editor
3. Copiar API keys:

```bash
copy .env.example .env
# Editar .env con SUPABASE_URL y SUPABASE_KEY
```

### 3. Ejecutar

```bash
# CLI Interactivo (menú en terminal)
python main.py

# API HTTP (puerto 8000)
python api/index.py
# Luego abrir http://localhost:8000 en el navegador
```

### 4. Ejecutar Tests

```bash
pytest tests/ -v
# Resultado esperado: 45 passed
```

---

## 📡 API Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/health` | Health check | No |
| `POST` | `/api/auth/login` | Iniciar sesión | No |
| `POST` | `/api/auth/logout` | Cerrar sesión | Sí |
| `GET` | `/api/notas` | Listar notas | Sí |
| `POST` | `/api/notas` | Crear nota | Sí |
| `DELETE` | `/api/notas?id=xxx` | Eliminar nota | Sí |

---

## 📚 Documentación SDLC

| Fase | Documento | Descripción |
|------|-----------|-------------|
| **1. Planificación** | `docs/01_planificacion.md` | Objetivos, alcance, riesgos |
| **2. Análisis** | `docs/02_analisis.md` | Requisitos, HU, CU |
| **3a. Arquitectura** | `docs/03_a_*.md` | Capas, patrones, stateless |
| **3b. Datos** | `docs/03_b_modelado_datos.md` | DER, clases |
| **3c. API** | `docs/03_c_api_dinamica.md` | Endpoints, secuencias |
| **4. Implementación** | `docs/04_*.md` | Setup + 11 manuales técnicos |
| **5. Testing** | `docs/05_*.md` | Plan UAT + ejecución |
| **6. Deploy** | `docs/06_despliegue_cierre.md` | Guía de deploy |

---

## 🔐 Seguridad

| Característica | Implementación |
|----------------|----------------|
| **RLS** | Políticas en tabla `notas` |
| **JWT** | Supabase Auth |
| **Timeout 15 min** | SessionManager |
| **Variables de entorno** | python-dotenv |
| **Sin hardcode** | Auditoría en cada archivo |

---

## 🧪 Tests

```
===== 45 passed, 12 warnings in 2.94s =====
```

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| Models | 14 | User, Nota |
| Services | 19 | SessionManager, Auth, Notas |
| API | 12 | VercelBridge endpoints |

---

## 📦 Deploy

### Opciones Disponibles

| Plataforma | Comando/Guía |
|------------|--------------|
| **Local** | `python api/index.py` |
| **Docker** | `docker build -t crud-notas . && docker run -p 8000:8000 crud-notas` |
| **Vercel** | Push a GitHub → Auto-deploy |
| **Heroku** | `git push heroku main` |

Ver guía completa en `docs/06_despliegue_cierre.md`.

---

## 📜 Licencia

Este proyecto está bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

- ✅ Copiar y redistribuir
- ✅ Modificar y adaptar
- ✅ Uso comercial (con atribución)

Ver [LICENSE](LICENSE) para más detalles.

---

## 👥 Créditos

| Rol | Detalle |
|-----|---------|
| **Desarrollo** | Asistido por IA (Claude + Antigravity) |
| **Supervisión** | Revisión humana en cada ciclo |
| **Documentación** | Metodología SDLC completa |

---

## 📞 Soporte

Este es un proyecto **didáctico**. Para consultas:

1. Revisar documentación en `docs/`
2. Ver `docs/CHECKPOINT.md` para estado actual
3. Abrir issue en el repositorio

---

> **Versión:** 1.0.0  
> **Fecha de cierre:** 2025-12-24  
> **Estado:** ✅ COMPLETADO
