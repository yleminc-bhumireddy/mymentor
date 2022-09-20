from flask import render_template
from sqlalchemy.orm import load_only
from app.modules.jobs import blueprint
from app.modules.jobs.jobModel import Customer
from app.modules.login.routes import login_is_required


@blueprint.route('/')
@login_is_required
def jobs():
    data = Customer.query.options(load_only("name")).all()
    return render_template('createjob.html', data=data)
