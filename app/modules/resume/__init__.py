from flask import Blueprint

blueprint = Blueprint("resume", __name__, static_folder="static", template_folder="templates", url_prefix="/resume")
