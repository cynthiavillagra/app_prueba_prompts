# 🏗️ Fase 3-A (Parte 3): Manejo de Estado y Sesión

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `03_a_2_patrones.md`  
> **Stack:** Python POO (sin frameworks)

---

## 1. Contexto: Aplicación de Escritorio/CLI

A diferencia de una aplicación web serverless, nuestra aplicación Python CLI:
- **Mantiene estado en memoria** durante la sesión
- **No tiene la restricción de memoria volátil** de Vercel/serverless
- **La sesión persiste** mientras el programa esté en ejecución

Sin embargo, seguimos buenas prácticas de manejo de estado.

---

## 2. Reglas de Manejo de Estado

### ✅ PERMITIDO

```python
# ✅ Estado de sesión en objeto (encapsulado)
class SessionManager:
    def __init__(self):
        self.current_user = None
        self.access_token = None
    
    def set_user(self, user):
        self.current_user = user
    
    def is_authenticated(self):
        return self.current_user is not None

# ✅ Singleton para configuración
class Settings:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# ✅ Estado en base de datos (Supabase)
# Los datos persisten entre ejecuciones del programa
```

### ⚠️ EVITAR (Anti-patrones)

```python
# ⚠️ Variables globales sueltas (difícil de testear)
current_user = None  # Mejor usar clase SessionManager

# ⚠️ Credenciales hardcodeadas
SUPABASE_KEY = "eyJhbG..."  # ❌ NUNCA

# ⚠️ Estado compartido sin control
datos_cache = []  # Sin encapsulación
```

---

## 3. Estrategia por Tipo de Estado

| Tipo de Estado | Dónde Almacenar | Cómo |
|----------------|-----------------|------|
| Usuario actual | `SessionManager` | Objeto en memoria |
| Access token | `SessionManager` | Renovar si expira |
| Datos de notas | PostgreSQL | Supabase Database |
| Configuración | `Settings` | Singleton + .env |

---

## 4. Flujo de Autenticación

```
1. REGISTRO
   Usuario ──► Ingresa email/password
          ──► AuthService.register()
          ──► Supabase Auth crea usuario
          ◄── Devuelve User object
          ──► SessionManager guarda usuario

2. LOGIN
   Usuario ──► Ingresa email/password
          ──► AuthService.login()
          ──► Supabase Auth valida
          ◄── Devuelve User + access_token
          ──► SessionManager guarda sesión

3. OPERACIÓN AUTENTICADA
   Usuario ──► Solicita listar notas
          ──► Verificar SessionManager.is_authenticated()
          ──► NotasService.listar(user_id)
          ──► Supabase aplica RLS
          ◄── Solo notas del usuario

4. LOGOUT
   Usuario ──► Solicita cerrar sesión
          ──► AuthService.logout()
          ──► SessionManager.clear()
          ◄── Vuelve al menú de login
```

---

## 5. Implementación de SessionManager

```python
# src/services/session_manager.py

class SessionManager:
    """
    Gestiona el estado de la sesión del usuario.
    
    POR QUÉ una clase: Encapsula el estado, facilita testing,
    evita variables globales sueltas.
    """
    
    _instance = None  # Singleton
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.current_user = None
        self.access_token = None
        self.refresh_token = None
    
    def set_session(self, user: dict, access_token: str, refresh_token: str = None):
        """Establece la sesión después de login exitoso"""
        self.current_user = user
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def clear(self):
        """Limpia la sesión (logout)"""
        self.current_user = None
        self.access_token = None
        self.refresh_token = None
    
    def is_authenticated(self) -> bool:
        """Verifica si hay usuario autenticado"""
        return self.current_user is not None
    
    def get_user_id(self) -> str:
        """Obtiene el ID del usuario actual"""
        if self.current_user:
            return self.current_user.get('id')
        return None
    
    def require_auth(self):
        """Lanza excepción si no está autenticado"""
        if not self.is_authenticated():
            raise PermissionError("Debe iniciar sesión primero")


# Uso en el menú:
if __name__ == "__main__":
    session = SessionManager()
    
    # Después de login exitoso
    session.set_session(user_data, token)
    
    # Verificar antes de operaciones
    if session.is_authenticated():
        notas = notas_service.listar(session.get_user_id())
```

---

## 6. Manejo de Token Expirado

```python
# En AuthService o decorador

def verificar_sesion(self):
    """
    Verifica si la sesión sigue válida.
    Supabase maneja expiración automáticamente,
    pero podemos agregar verificación explícita.
    """
    session = SessionManager()
    
    if not session.is_authenticated():
        return False
    
    try:
        # Intentar obtener usuario actual de Supabase
        user = self.client.auth.get_user(session.access_token)
        return user is not None
    except Exception:
        # Token expirado o inválido
        session.clear()
        return False
```

---

## 7. Carga Segura de Credenciales

```python
# src/config/settings.py

import os
from dotenv import load_dotenv

class Settings:
    """
    Singleton para configuración.
    Carga variables de .env de forma segura.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_env()
        return cls._instance
    
    def _load_env(self):
        # Cargar .env del directorio raíz
        load_dotenv()
        
        # POR QUÉ os.getenv: NUNCA hardcodear credenciales
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        # Validar que existen
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Faltan variables de entorno. "
                "Copia .env.example a .env y completa los valores."
            )


# Uso:
if __name__ == "__main__":
    settings = Settings()
    print(f"URL: {settings.supabase_url}")
```

---

## 8. Resumen de Decisiones

| ID | Decisión | Patrón | Ubicación |
|----|----------|--------|-----------|
| ADR-01 | Sesión en objeto | Singleton | `SessionManager` |
| ADR-02 | Config desde .env | Singleton | `Settings` |
| ADR-03 | Verificar auth antes de ops | Guard Clause | Services |
| ADR-04 | Cero hardcode de credenciales | Env Vars | `.env` |
| ADR-05 | Estado en Supabase | Database | PostgreSQL |

---

## 9. Próximos Pasos

1. ✅ **Fase 3-A Completada:** Arquitectura, Patrones, Estado
2. 🔜 **Fase 3-B Pendiente:** Modelado de Datos

---

> **Documento generado:** 2025-12-23
