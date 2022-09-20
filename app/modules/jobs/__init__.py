from flask import Blueprint

blueprint = Blueprint('jobs', __name__, static_folder='static', template_folder='templates', url_prefix='/jobs')
