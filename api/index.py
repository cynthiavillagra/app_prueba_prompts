# -*- coding: utf-8 -*-
"""
============================================================================
API/INDEX.PY - Entry Point para Vercel (Serverless)
============================================================================
Proyecto: CRUD Didáctico con Supabase
Tipo: Entry Point Serverless / Bridge Pattern
Fecha: 2025-12-24

REGLA "SIN FRAMEWORKS" - BRIDGE PATTERN:
Este archivo implementa un adaptador WSGI manual que permite
ejecutar la aplicación en Vercel sin usar Flask, Django, etc.

EJECUCIÓN:
- En Vercel: Automático (api/index.py es el entry point)
- Local: python api/index.py (inicia HTTPServer en puerto 8000)

ARQUITECTURA SERVERLESS:
- Cada request es independiente
- NO hay estado entre requests
- Variables de entorno vienen del Dashboard de Vercel

NOTA: Este archivo es para demostración del patrón.
La aplicación principal es CLI (main.py).
============================================================================
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any, Tuple, Optional

# Agregar directorio padre al path para imports
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# En Vercel, las variables de entorno ya están cargadas
# En local, cargarlas desde .env
if not os.getenv('VERCEL'):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_parent_dir, '.env'))


# ============================================================================
# VERCEL BRIDGE - Adaptador WSGI Manual
# ============================================================================

class VercelBridge:
    """
    Adaptador que traduce requests HTTP a operaciones de la aplicación.
    
    PATRÓN BRIDGE:
    - Desacopla la interfaz HTTP de la lógica de negocio
    - Permite usar la misma lógica en CLI y API
    
    POR QUÉ NO FLASK:
    - Requisito: "Sin frameworks"
    - Didáctico: Entender cómo funciona HTTP a bajo nivel
    
    POR QUÉ SÍ HTTP.SERVER:
    - Módulo estándar de Python (sin dependencias)
    - Suficiente para demostración
    """
    
    def __init__(self):
        """Inicializa dependencias lazy (solo cuando se necesiten)."""
        self._auth = None
        self._notas = None
    
    @property
    def auth(self):
        """Lazy loading de AuthService."""
        if self._auth is None:
            from src.services.auth_service import AuthService
            self._auth = AuthService()
        return self._auth
    
    @property
    def notas(self):
        """Lazy loading de NotasService."""
        if self._notas is None:
            from src.services.notas_service import NotasService
            self._notas = NotasService()
        return self._notas
    
    def handle_request(
        self, 
        method: str, 
        path: str, 
        query: Dict[str, list], 
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Router principal - dirige requests a handlers.
        
        PARÁMETROS:
        - method: GET, POST, PUT, DELETE
        - path: Ruta sin query string (ej: /api/notas)
        - query: Parámetros de query string
        - body: Cuerpo del request (para POST/PUT)
        - headers: Headers HTTP
        
        RETORNA:
        - Tuple[status_code, response_dict]
        
        RUTAS:
        - GET /api/health → Health check
        - POST /api/auth/login → Login
        - POST /api/auth/logout → Logout
        - GET /api/notas → Listar notas
        - POST /api/notas → Crear nota
        - DELETE /api/notas?id=xxx → Eliminar nota
        """
        # Health check
        if path == '/api/health' or path == '/':
            return 200, {
                'status': 'ok',
                'message': 'CRUD Didáctico con Supabase - API funcionando',
                'version': '1.0.0'
            }
        
        # Auth routes
        if path == '/api/auth/login' and method == 'POST':
            return self._handle_login(body or {})
        
        if path == '/api/auth/logout' and method == 'POST':
            return self._handle_logout()
        
        # Notas routes
        if path == '/api/notas':
            if method == 'GET':
                return self._handle_listar_notas()
            elif method == 'POST':
                return self._handle_crear_nota(body or {})
            elif method == 'DELETE':
                nota_id = query.get('id', [None])[0]
                return self._handle_eliminar_nota(nota_id)
        
        # 404 Not Found
        return 404, {'error': 'Ruta no encontrada', 'path': path}
    
    def _handle_login(self, body: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """Handler para login."""
        email = body.get('email', '')
        password = body.get('password', '')
        
        if not email or not password:
            return 400, {'error': 'Email y password son requeridos'}
        
        try:
            user = self.auth.login(email, password)
            return 200, {
                'success': True,
                'user': {'id': user.id, 'email': user.email}
            }
        except ValueError as e:
            return 400, {'error': str(e)}
        except PermissionError as e:
            return 401, {'error': str(e)}
        except Exception as e:
            return 500, {'error': f'Error interno: {e}'}
    
    def _handle_logout(self) -> Tuple[int, Dict[str, Any]]:
        """Handler para logout."""
        try:
            self.auth.logout()
            return 200, {'success': True, 'message': 'Sesión cerrada'}
        except Exception as e:
            return 500, {'error': f'Error al cerrar sesión: {e}'}
    
    def _handle_listar_notas(self) -> Tuple[int, Dict[str, Any]]:
        """Handler para listar notas."""
        try:
            notas = self.notas.listar()
            return 200, {
                'success': True,
                'data': [n.to_dict() for n in notas],
                'count': len(notas)
            }
        except PermissionError as e:
            return 401, {'error': str(e)}
        except Exception as e:
            return 500, {'error': f'Error al listar: {e}'}
    
    def _handle_crear_nota(self, body: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """Handler para crear nota."""
        titulo = body.get('titulo', body.get('title', ''))
        contenido = body.get('contenido', body.get('content'))
        
        if not titulo:
            return 400, {'error': 'Título es requerido'}
        
        try:
            nota = self.notas.crear(titulo, contenido)
            return 201, {
                'success': True,
                'data': nota.to_dict()
            }
        except PermissionError as e:
            return 401, {'error': str(e)}
        except ValueError as e:
            return 400, {'error': str(e)}
        except Exception as e:
            return 500, {'error': f'Error al crear: {e}'}
    
    def _handle_eliminar_nota(self, nota_id: Optional[str]) -> Tuple[int, Dict[str, Any]]:
        """Handler para eliminar nota."""
        if not nota_id:
            return 400, {'error': 'ID de nota es requerido'}
        
        try:
            eliminada = self.notas.eliminar(nota_id)
            if eliminada:
                return 200, {'success': True, 'message': 'Nota eliminada'}
            else:
                return 404, {'error': 'Nota no encontrada'}
        except PermissionError as e:
            return 401, {'error': str(e)}
        except Exception as e:
            return 500, {'error': f'Error al eliminar: {e}'}


# ============================================================================
# HTTP REQUEST HANDLER - Para servidor local
# ============================================================================

class RequestHandler(BaseHTTPRequestHandler):
    """
    Handler HTTP que usa VercelBridge.
    
    POR QUÉ BaseHTTPRequestHandler:
    - Estándar de Python
    - Sin dependencias externas
    - Suficiente para demostración
    """
    
    bridge = VercelBridge()
    
    def _send_json_response(self, status: int, data: Dict[str, Any]) -> None:
        """Envía respuesta JSON."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _parse_body(self) -> Dict[str, Any]:
        """Parsea el body del request."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                return json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                return {}
        return {}
    
    def do_GET(self) -> None:
        """Maneja requests GET."""
        parsed = urlparse(self.path)
        
        # Servir archivos estáticos del frontend
        if self._serve_static_file(parsed.path):
            return
        
        # API routes
        query = parse_qs(parsed.query)
        status, data = self.bridge.handle_request('GET', parsed.path, query)
        self._send_json_response(status, data)
    
    def _serve_static_file(self, path: str) -> bool:
        """
        Sirve archivos estáticos del directorio public/.
        
        POR QUÉ:
        - SÍ: Permite servir el frontend HTML/CSS/JS
        - SÍ: Sin necesidad de servidor web adicional
        - NO en producción: Usar nginx/CDN para estáticos
        
        RETORNA: True si sirvió un archivo, False si es ruta API
        """
        # Rutas que deben manejarse como API
        if path.startswith('/api'):
            return False
        
        # Directorio de archivos estáticos
        public_dir = os.path.join(_parent_dir, 'public')
        
        # Determinar archivo a servir
        if path == '/' or path == '':
            file_path = os.path.join(public_dir, 'index.html')
        else:
            # Limpiar path y buscar archivo
            clean_path = path.lstrip('/')
            file_path = os.path.join(public_dir, clean_path)
        
        # Verificar que el archivo existe y está dentro de public/
        if not os.path.exists(file_path):
            return False
        
        # Verificar que no se intenta acceder fuera de public/
        real_path = os.path.realpath(file_path)
        real_public = os.path.realpath(public_dir)
        if not real_path.startswith(real_public):
            return False
        
        # Determinar content-type
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml'
        }
        
        ext = os.path.splitext(file_path)[1].lower()
        content_type = content_types.get(ext, 'application/octet-stream')
        
        try:
            # Leer y enviar archivo
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', f'{content_type}; charset=utf-8')
            self.send_header('Content-Length', len(content))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
            return True
            
        except Exception as e:
            print(f"Error sirviendo archivo: {e}")
            return False
    
    def do_POST(self) -> None:
        """Maneja requests POST."""
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        body = self._parse_body()
        status, data = self.bridge.handle_request('POST', parsed.path, query, body)
        self._send_json_response(status, data)
    
    def do_DELETE(self) -> None:
        """Maneja requests DELETE."""
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        status, data = self.bridge.handle_request('DELETE', parsed.path, query)
        self._send_json_response(status, data)
    
    def do_OPTIONS(self) -> None:
        """Maneja CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()


# ============================================================================
# VERCEL HANDLER - Función expuesta para Vercel
# ============================================================================

# Instancia global para Vercel (se recrea en cada cold start)
app = VercelBridge()

def handler(request):
    """
    Handler para Vercel Serverless Functions.
    
    NOTA: Este es el formato esperado por Vercel para Python.
    Recibe un objeto request y retorna un response.
    
    En Vercel real, usar:
    from http.server import BaseHTTPRequestHandler
    """
    # Para Vercel, el formato es diferente
    # Este es un ejemplo simplificado
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Use /api/health para verificar'})
    }


# ============================================================================
# EJECUCIÓN LOCAL - if __name__ == "__main__"
# ============================================================================

if __name__ == "__main__":
    """
    Inicia servidor HTTP local para pruebas.
    
    EJECUCIÓN:
        python api/index.py
    
    ENDPOINTS:
        GET  http://localhost:8000/api/health
        POST http://localhost:8000/api/auth/login
        GET  http://localhost:8000/api/notas
    """
    PORT = 8000
    
    print("=" * 60)
    print("SERVIDOR API LOCAL - CRUD Didáctico")
    print("=" * 60)
    print(f"Servidor iniciado en: http://localhost:{PORT}")
    print(f"\nEndpoints disponibles:")
    print(f"  GET  /api/health     - Health check")
    print(f"  POST /api/auth/login - Login")
    print(f"  GET  /api/notas      - Listar notas")
    print(f"  POST /api/notas      - Crear nota")
    print(f"\nPresione Ctrl+C para detener")
    print("=" * 60)
    
    try:
        server = HTTPServer(('localhost', PORT), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
