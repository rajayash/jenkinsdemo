from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from typing import NoReturn
from werkzeug.serving import WSGIRequestHandler

# Modern Flask application factory pattern
def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev')
    
    return app

myapp = create_app()

# In newer Flask versions, the shutdown functionality has changed
def shutdown_server() -> NoReturn:
    """Shutdown the development server."""
    if not os.environ.get('FLASK_ENV') == 'development':
        raise RuntimeError('Shutdown command only available in development mode')
    
    # Modern way to handle server shutdown
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

if __name__ == "__main__":
    # Modern way to run Flask development server
    if os.environ.get('FLASK_ENV') == 'production':
        print("Please use a production WSGI server like Gunicorn")
    else:
        # Modern server configuration
        WSGIRequestHandler.protocol_version = "HTTP/1.1"
        myapp.run(
            host='0.0.0.0', 
            port=int(os.environ.get('PORT', 80)),
            debug=os.environ.get('FLASK_ENV') == 'development'
        )
