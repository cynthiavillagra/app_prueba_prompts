# 📘 Manual Técnico: supabase_client.py

> **Archivo:** `src/repositories/supabase_client.py`  
> **Tipo:** Singleton de Infraestructura  
> **Fecha:** 2025-12-24  
> **Autor:** Generado con IA (Claude + Antigravity)

---

## 1. Propósito

El archivo `supabase_client.py` proporciona un cliente único (Singleton) para conectarse a Supabase, centralizando la configuración de conexión y exponiendo acceso a Auth y Database.

### Trazabilidad Completa

| Campo | Valor |
|-------|-------|
| **Módulo** | CORE / INFRAESTRUCTURA |
| **Requisito** | RNF-ARCH-02 (Patrones de diseño implementados) |
| **Historia de Usuario** | Transversal (todas las operaciones de datos) |
| **Criterio de Aceptación** | Singleton para cliente Supabase |
| **Caso de Uso** | CU-01 (Auth), CU-02 (CRUD Notas) |
| **Escenario** | Todas las operaciones que requieren Supabase |

---

## 2. Estrategia de Construcción

### Cadena de Dependencias

```
┌─────────────────────────────────────────────────────────────┐
│              CADENA DE DEPENDENCIAS                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   .env                                                      │
│     │                                                       │
│     ▼                                                       │
│   Settings (Singleton)                                      │
│     │                                                       │
│     ▼                                                       │
│   SupabaseClient (Singleton) ◄── Este archivo               │
│     │                                                       │
│     ▼                                                       │
│   AuthService, NotasService, etc.                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Patrón Singleton + Adapter

```
┌─────────────────────────────────────────────────────────────┐
│   SupabaseClient                                            │
│   ├── _instance (Singleton)                                 │
│   ├── client: Client (supabase-py)                          │
│   ├── auth → Acceso a autenticación                         │
│   └── table(name) → Acceso a tablas                         │
│                                                             │
│   Internamente usa:                                         │
│   └── supabase.create_client(url, key)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Aclaración Metodológica

### 3.1 Rol del Bloque Main

El bloque `if __name__ == "__main__":` verifica:

1. **Creación del cliente** - Se conecta a Supabase
2. **Patrón Singleton** - Misma instancia en múltiples llamadas
3. **Query funcional** - Puede hacer SELECT a tabla notas
4. **Auth disponible** - Módulo de autenticación accesible
5. **Stateless** - No hay almacenamiento de sesiones en el código

---

## 4. Código Fuente

### Ubicación

```
src/
├── config/
│   └── settings.py        ◄── Dependencia
└── repositories/
    ├── __init__.py
    └── supabase_client.py ◄── Este archivo
```

### Propiedades y Métodos

| Miembro | Tipo | Descripción |
|---------|------|-------------|
| `_instance` | class var | Instancia única (Singleton) |
| `client` | property | Cliente Supabase subyacente |
| `auth` | property | Módulo de autenticación |
| `table(name)` | method | Acceso a una tabla específica |

---

## 5. Prueba de Fuego

### 5.1 Ejecución

```powershell
# Desde la raíz del proyecto (con venv activado)
python src/repositories/supabase_client.py
```

### 5.2 Resultado Esperado (OK)

```
============================================================
PRUEBA DE FUEGO: SupabaseClient (Singleton)
============================================================
✅ SupabaseClient creado
✅ Singleton verificado: misma instancia
✅ Query a 'notas' exitosa. Registros: 0
✅ Auth disponible
✅ Stateless verificado: sin almacenamiento de sesiones
============================================================
RESULTADO: TODOS LOS TESTS PASARON
============================================================
```

### 5.3 Posibles Advertencias

```
⚠️ Tabla 'notas' no existe. Ejecutar database/init.sql
```

**Solución:** Ejecutar el script SQL en Supabase Dashboard.

---

## 6. Análisis Dual

### ¿Por qué SÍ esta implementación?

| Decisión | Justificación |
|----------|---------------|
| Singleton con `__new__` | Control explícito de instanciación |
| Dependencia de Settings | Separa configuración de conexión |
| Exponer `client` directamente | Evita wrappear toda la API de Supabase |
| Property `auth` y `table()` | Sintaxis más limpia para uso común |

### ¿Por qué NO alternativas?

| Alternativa | Razón de Exclusión |
|-------------|-------------------|
| Crear cliente en cada request | Overhead innecesario, límites de API |
| HTTP requests manuales | Reinventar la rueda, sin abstracción |
| Guardar cliente en variable global | Menos control, testing difícil |
| Wrappear cada método de Supabase | Over-engineering extremo |

---

## 7. Guía de Resolución de Problemas

### 7.1 Troubleshooting

| Error | Causa | Solución |
|-------|-------|----------|
| `ModuleNotFoundError: supabase` | Dependencia no instalada | `pip install supabase` |
| `ValueError: Variables faltantes` | .env no configurado | Verificar `.env` |
| `relation notas does not exist` | Tabla no creada | Ejecutar `database/init.sql` |
| `Invalid API key` | Key incorrecta | Verificar `SUPABASE_KEY` en `.env` |

### 7.2 Diferencias Local vs Nube

| Aspecto | Local | Vercel/Docker |
|---------|-------|---------------|
| Configuración | Desde `.env` | Desde env vars del sistema |
| Persistencia del Singleton | Durante ejecución del script | Por request (se recrea) |
| Conexión | Una por ejecución | Una por invocación |

**IMPORTANTE para Serverless:**
En Vercel, el Singleton se recrea en cada "cold start", pero esto es correcto porque:
- Cada request es independiente
- No hay estado compartido entre requests
- El cliente Supabase es lightweight

### 7.3 Seguridad

| Check | Estado |
|-------|--------|
| Usa ANON_KEY (no SERVICE_ROLE) | ✅ |
| No hay sesiones hardcodeadas | ✅ |
| Credenciales desde Settings | ✅ |
| RLS protege los datos | ✅ |

---

## 8. Compatibilidad Serverless

| Check | Estado |
|-------|--------|
| Sin estado global mutable | ✅ |
| Recreación segura en cold start | ✅ |
| No guarda sesiones de usuario | ✅ |
| Depende solo de env vars | ✅ |

---

## 9. Uso en Services

```python
# Ejemplo de uso en NotasService
from src.repositories import SupabaseClient

class NotasService:
    def __init__(self):
        self._supabase = SupabaseClient()
    
    def listar(self, user_id: str):
        response = self._supabase.table('notas') \
            .select('*') \
            .eq('user_id', user_id) \
            .order('created_at', desc=True) \
            .execute()
        return response.data
```

---

> **Documento generado:** 2025-12-24  
> **Dependencia:** `src/config/settings.py`  
> **Próximo archivo:** `src/models/user.py`
