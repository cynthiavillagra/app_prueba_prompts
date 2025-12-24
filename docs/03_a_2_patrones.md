# 🏗️ Fase 3-A (Parte 2): Patrones de Diseño

> **Proyecto:** CRUD Didáctico con Supabase  
> **Fecha:** 2025-12-23  
> **Referencia:** Continuación de `03_a_1_arquitectura.md`  
> **Stack:** Python POO (sin frameworks)

---

## 1. Catálogo de Patrones

| Tipo | Patrón | Uso en el Proyecto |
|------|--------|-------------------|
| Creacional | **Singleton** | Cliente Supabase único |
| Creacional | **Factory Method** | Crear servicios según contexto |
| Estructural | **Adapter** | Services que encapsulan Supabase |
| Comportamiento | **Strategy** | Estrategias de autenticación |

---

## 2. Singleton: Cliente Supabase

**Propósito:** Una única instancia del cliente en toda la app.

```
auth_service ──┐
notas_service ─┼──► [ SupabaseClient ] ──► Supabase API
main.py ───────┘    (Única Instancia)
```

**Ubicación:** `src/repositories/supabase_client.py`

**Implementación Python:**

```python
# POR QUÉ Singleton: Evita crear múltiples conexiones a Supabase
# Cada instancia consumiría recursos innecesarios

class SupabaseClient:
    _instance = None  # Variable de clase para guardar instancia
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicialización solo ocurre una vez
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        from supabase import create_client
        from src.config.settings import Settings
        
        settings = Settings()
        self.client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
```

**¿Por qué SÍ?**
- Evita múltiples conexiones
- Centraliza configuración
- Fácil de mockear en tests

---

## 3. Factory Method: Crear Servicios

**Propósito:** Crear diferentes servicios según el contexto.

```python
# Ejemplo de uso futuro (extensibilidad)
class ServiceFactory:
    @staticmethod
    def create_auth_service(strategy: str = "email"):
        if strategy == "email":
            return EmailAuthService()
        elif strategy == "oauth":
            return OAuthService()  # Futuro v2
```

**¿Por qué SÍ?**
- Facilita agregar nuevas estrategias de auth
- Cumple Open/Closed principle

---

## 4. Adapter: Servicios Desacoplados

**Propósito:** Aislar la UI del SDK de Supabase.

```
[ Menu CLI ] ──► [ NotasService ] ──► [ SupabaseClient ]
                 (Adapter)
```

**Ubicación:** `src/services/notas_service.py`

**Implementación Python:**

```python
# POR QUÉ Adapter: Desacopla la UI del SDK de Supabase
# Si cambiamos de Supabase a Firebase, solo modificamos este archivo

class NotasService:
    def __init__(self):
        self.client = SupabaseClient().client
    
    def listar(self, user_id: str) -> list:
        """Obtiene todas las notas del usuario"""
        response = self.client.table('notas') \
            .select('*') \
            .eq('user_id', user_id) \
            .execute()
        return response.data
    
    def crear(self, user_id: str, titulo: str, contenido: str) -> dict:
        """Crea una nueva nota"""
        response = self.client.table('notas').insert({
            'user_id': user_id,
            'title': titulo,
            'content': contenido
        }).execute()
        return response.data[0]
```

**¿Por qué SÍ?**
- Desacopla UI de implementación
- Facilita migración futura
- Centraliza manejo de errores

**¿Por qué NO llamar Supabase desde el menú?**
- Código duplicado
- Difícil de cambiar proveedor
- Complejo de testear

---

## 5. Strategy: Autenticación Extensible

**Propósito:** Estrategias de auth intercambiables.

```
AuthService ──► IAuthStrategy (ABC)
                    ├── EmailPasswordStrategy ✅ (v1)
                    ├── GoogleOAuthStrategy   🔜 (v2)
                    └── MagicLinkStrategy     🔜 (v2)
```

**Implementación Python:**

```python
from abc import ABC, abstractmethod

# Interfaz (Abstract Base Class)
class IAuthStrategy(ABC):
    @abstractmethod
    def login(self, **kwargs) -> dict:
        pass
    
    @abstractmethod
    def register(self, **kwargs) -> dict:
        pass

# Estrategia concreta: Email/Password
class EmailPasswordStrategy(IAuthStrategy):
    def __init__(self):
        self.client = SupabaseClient().client
    
    def login(self, email: str, password: str) -> dict:
        response = self.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user
    
    def register(self, email: str, password: str) -> dict:
        response = self.client.auth.sign_up({
            "email": email,
            "password": password
        })
        return response.user

# Servicio que usa la estrategia
class AuthService:
    def __init__(self, strategy: IAuthStrategy = None):
        self.strategy = strategy or EmailPasswordStrategy()
    
    def login(self, **kwargs):
        return self.strategy.login(**kwargs)
```

**¿Por qué SÍ?**
- MVP usa email/password
- v2 puede agregar OAuth sin modificar código existente
- Cumple Open/Closed principle
- Demuestra polimorfismo en POO

---

## 6. Resumen de Patrones

| Patrón | Clase | Archivo |
|--------|-------|---------|
| Singleton | `SupabaseClient` | `repositories/supabase_client.py` |
| Singleton | `Settings` | `config/settings.py` |
| Adapter | `NotasService` | `services/notas_service.py` |
| Adapter | `AuthService` | `services/auth_service.py` |
| Strategy | `IAuthStrategy` | `services/auth_service.py` |
| Strategy | `EmailPasswordStrategy` | `services/auth_service.py` |

---

> **Continúa en:** `03_a_3_stateless.md`
