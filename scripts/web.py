from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import subprocess
import signal
import time
from typing import NoReturn
from werkzeug.serving import WSGIRequestHandler

def stop_existing_server(port: int = 80) -> None:
    """Stop any process running on the specified port."""
    try:
        # Find process using port 80
        cmd = f"lsof -t -i:{port}"
        pids = subprocess.check_output(cmd, shell=True).decode().strip().split('\n')
        
        for pid in pids:
            if pid:
                # Kill the process
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"Terminated process {pid} on port {port}")
                except ProcessLookupError:
                    print(f"Process {pid} not found")
                except Exception as e:
                    print(f"Error killing process {pid}: {e}")
        
        # Wait for port to be released
        time.sleep(2)
        
    except subprocess.CalledProcessError:
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error stopping existing server: {e}")

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev')
    return app

myapp = create_app()

def shutdown_server() -> NoReturn:
    """Shutdown the development server."""
    if not os.environ.get('FLASK_ENV') == 'development':
        raise RuntimeError('Shutdown command only available in development mode')
    
    if 'werkzeug.server.shutdown' in request.environ:
        request.environ['werkzeug.server.shutdown']()
    raise RuntimeError('Not running with Werkzeug Server')

@myapp.route('/shutdown', methods=['POST'])
def shutdown() -> tuple[str, int]:
    """Endpoint to shutdown the development server."""
    try:
        shutdown_server()
        return 'Server shutting down...', 200
    except RuntimeError as e:
        return str(e), 500

@myapp.route("/")
def hello() -> str:
    """Root endpoint rendering the test template."""
    return render_template('test.html')

def check_port_available(port: int = 80) -> bool:
    """Check if port is available."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            s.close()
            return True
        except socket.error:
            return False

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    
    # Stop any existing server on the port
    if not check_port_available(port):
        print(f"Port {port} is in use. Attempting to stop existing process...")
        stop_existing_server(port)
    
    # Check again after stopping
    if not check_port_available(port):
        print(f"Error: Port {port} is still in use. Please check manually.")
        exit(1)
    
    # Modern server configuration
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    myapp.run(
        host='0.0.0.0', 
        port=port,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )
