from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

# from app.modules.jobs.jobsController import jobs_bp

db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)


# def configure_database(app):
# @app.before_first_request
# def initialize_database():
#     db.create_all()
#
# @app.teardown_request
# def shutdown_session(exception=None):
#     db.session.remove()
def register_blueprints(app):
    for module_name in ('login', 'jobs', 'emailservice'):
        module = import_module('app.modules.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def create_app(config):
    app = Flask(__name__)
    bootstrap = Bootstrap5(app)
    app.config.from_object(config)
    # app.register_blueprint(email_bp)
    # app.register_blueprint(jobs_bp)
    register_extensions(app)
    register_blueprints(app)
    app.secret_key = "EmailServicesYLEMINC"
    # configure_database(app)
    return app

