from flask import render_template, request, url_for, redirect
import httplib2
from app.modules.emailservice import blueprint
from app.modules.login.routes import login_is_required
from app.modules.emailservice.model import EmailForm
from app.modules.emailservice.email import gmail_send

from app.modules.emailservice.gdocs_reader import readSheets


@blueprint.route('/', methods=['GET', 'POST'])
@login_is_required
def email():
    emailForm = EmailForm(request.form)
    # readSheets()
    if 'send' in request.form:
        print('i am in post request')
        total_count = gmail_send(emailForm)
        emailForm = EmailForm()
        emailForm.totalSent = total_count
        return render_template("email.html", form=emailForm)
    else:
        return render_template("email.html", form=emailForm)
