# 📝 CRUD Didáctico con Supabase

> **Aplicación CRUD de notas** desarrollada con Python POO (sin frameworks) + Supabase como BaaS.

---

## 🎯 Descripción

Este proyecto es una **aplicación didáctica** que implementa un CRUD completo de notas personales, diseñada para enseñar:

- **Programación Orientada a Objetos** en Python
- **Patrones de Diseño** (Singleton, Strategy, Adapter, Factory)
- **Integración con BaaS** (Supabase)
- **Arquitectura por Capas**
- **Metodología SDLC** con documentación completa

---

## ⚠️ ADVERTENCIAS IMPORTANTES

### 🚨 NO APTO PARA PRODUCCIÓN

Este proyecto está diseñado **exclusivamente** para:

- ✅ **MVP (Minimum Viable Product)** - Pruebas de concepto
- ✅ **Uso Local** - Desarrollo y aprendizaje
- ✅ **Uso Pedagógico** - Enseñanza de conceptos

**NO debe ser desplegado en producción** porque:

- ❌ No implementa HTTPS (solo HTTP)
- ❌ No tiene rate limiting
- ❌ Manejo básico de tokens
- ❌ Sin logging de seguridad
- ❌ Código no auditado para vulnerabilidades

---

## 🤖 AI Stack

Este proyecto fue desarrollado utilizando **Inteligencia Artificial Generativa**:

| Herramienta | Uso |
|-------------|-----|
| **Google Antigravity** | IDE con asistente de IA integrado |
| **Claude Opus Thinking 4.5** | Generación de código y documentación |

### Metodología de Desarrollo con IA

1. **Prompt Engineering** - Instrucciones detalladas para cada fase SDLC
2. **Revisión Humana** - Validación de cada archivo generado
3. **Pruebas Atómicas** - Verificación de cada componente
4. **Documentación Narrativa** - Manuales técnicos para cada archivo

> ⚠️ **Nota:** El código generado por IA debe ser revisado cuidadosamente antes de cualquier uso.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Lenguaje** | Python 3.11+ |
| **Paradigma** | POO (sin frameworks web) |
| **Base de Datos** | Supabase (PostgreSQL) |
| **Autenticación** | Supabase Auth (JWT) |
| **Cliente DB** | supabase-py |
| **Variables de Entorno** | python-dotenv |
| **Interfaz** | CLI (Command Line Interface) |

---

## 📁 Estructura del Proyecto

```
proyecto/
├── main.py                    # Entry point CLI (local)
├── api/
│   └── index.py               # Entry point API (Vercel)
├── src/
│   ├── config/
│   │   └── settings.py        # Configuración (Singleton)
│   ├── repositories/
│   │   └── supabase_client.py # Cliente Supabase (Singleton)
│   ├── models/
│   │   ├── user.py            # Entidad Usuario
│   │   └── nota.py            # Entidad Nota
│   ├── services/
│   │   ├── session_manager.py # Gestión de sesión (Singleton)
│   │   ├── auth_service.py    # Autenticación (Strategy)
│   │   └── notas_service.py   # CRUD de notas (Adapter)
│   └── ui/
│       └── menu.py            # Menú CLI
├── database/
│   └── init.sql               # Script de inicialización
├── docs/                      # Documentación SDLC completa
├── requirements.txt           # Dependencias
├── vercel.json                # Config Vercel
├── Dockerfile                 # Config Docker
└── .env.example               # Plantilla de variables
```

---

## 🚀 Inicio Rápido

### 1. Clonar y Configurar

```bash
git clone https://github.com/usuario/app_prueba_prompts.git
cd app_prueba_prompts

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Supabase

1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ejecutar `database/init.sql` en SQL Editor
3. Copiar API keys a `.env`:

```bash
cp .env.example .env
# Editar .env con SUPABASE_URL y SUPABASE_KEY
```

### 3. Ejecutar

```bash
# CLI Interactivo
python main.py

# API HTTP (puerto 8000)
python api/index.py
```

---

## 📚 Documentación SDLC

| Fase | Documento |
|------|-----------|
| **Planificación** | `docs/01_planificacion.md` |
| **Análisis** | `docs/02_analisis.md` |
| **Diseño - Arquitectura** | `docs/03_a_1_arquitectura.md` |
| **Diseño - Patrones** | `docs/03_a_2_patrones.md` |
| **Diseño - Stateless** | `docs/03_a_3_stateless.md` |
| **Diseño - Datos** | `docs/03_b_modelado_datos.md` |
| **Diseño - API** | `docs/03_c_api_dinamica.md` |
| **Base de Datos** | `docs/035_manual_bbdd.md` |
| **Setup Local** | `docs/04_a_setup_local.md` |
| **Manuales Técnicos** | `docs/04_b_*.md` |

---

## 🔐 Seguridad Implementada

| Característica | Implementación |
|----------------|----------------|
| **RLS** | Políticas en tabla `notas` |
| **JWT** | Supabase Auth |
| **Timeout 15 min** | SessionManager |
| **Variables de entorno** | python-dotenv |
| **Sin hardcode** | Auditoría en cada archivo |

---

## 📜 Licencia

Este proyecto está bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Puedes:
- ✅ Copiar y redistribuir
- ✅ Modificar y adaptar
- ✅ Uso comercial

Con la condición de:
- Dar crédito apropiado
- Indicar si se realizaron cambios

Ver [LICENSE](LICENSE) para más detalles.

---

## 👥 Créditos

- **Desarrollo:** Asistido por IA (Claude + Antigravity)
- **Supervisión:** Equipo de Desarrollo
- **Documentación:** Generada con metodología SDLC

---

## 📞 Soporte

Este es un proyecto **didáctico**. Para consultas:

1. Revisar documentación en `docs/`
2. Consultar `docs/CHECKPOINT.md` para estado actual
3. Abrir issue en el repositorio

---

> **Generado:** 2025-12-24  
> **Versión:** 1.0.0  
> **Stack:** Python POO + Supabase
