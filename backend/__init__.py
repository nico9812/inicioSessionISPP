# Importación de Modulos
from .config import config
from backend.funcionalidades import enviarEmail
from .models.ModeloUsuario import modeloUsuario
from .models.entidad import EntidadUsuario

# Importación Flask
from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask.json import jsonify

# Inicialización primera del MYSQL y del LoginManager sin instanciar aplicación Flask
mysql = MySQL()
administrador_login = LoginManager()


def create_app():
    import os
    # Importado de Templates
    template_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(template_dir, 'frontend')
    template_dir = os.path.join(template_dir, "templates")

    # Importado de CSS
    staticcss_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    staticcss_dir = os.path.join(staticcss_dir, 'frontend')
    staticcss_dir = os.path.join(staticcss_dir, "static")

    # Inicialización de la APP flask, Token CSRF, MySQL y LoginManager
    app = Flask(__name__, template_folder=template_dir)
    app.static_folder = staticcss_dir
    app.config.from_object(config['desarrollo'])

    # Declaración de Error Handlers
    @administrador_login.user_loader
    def load_user(id):
        return modeloUsuario().conseguirID(mysql, id)

    @app.errorhandler(400)
    def handler400Error(error):
        return jsonify({'error': 'Bad Request'}), 400

    @app.errorhandler(401)
    def handler401Error(error):
        return redirect(url_for('index'))

    @app.errorhandler(404)
    def handler404Error(error):
        return jsonify({'error': 'NotFound'}), 404

    @app.errorhandler(500)
    def handler500error(error):
        return jsonify({'error': 'Error a la hora de conectar a la base de datos'}), 500

    app.register_error_handler(400, handler400Error)
    app.register_error_handler(401, handler401Error)
    app.register_error_handler(404, handler404Error)
    app.register_error_handler(500, handler500error)

    csrf = CSRFProtect(app)

    # Importado de Vistas
    from .vistas.controlUsuario import auth
    from .vistas.views import views
    from .vistas.alumno import vistAlumno
    
    # Rgistración de Blueprints (vistas)
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(vistAlumno, url_prefix="/alumno")
    
    # Inicializar DataBase
    mysql.init_app(app)

    # Inicializar Login
    administrador_login.init_app(app)
    administrador_login.session_protection = 'strong'
    administrador_login.login_view = "auth.login"
    administrador_login.login_message_category = "warning"
    administrador_login.login_message = "Inicie la sesión para acceder a esta pagina"

    return app
