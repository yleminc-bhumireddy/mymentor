from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import StringField, TextAreaField, IntegerField, FileField, SubmitField


class EmailForm(FlaskForm):
    totalSent = 0
    companyId = StringField()
    tolist = StringField()
    subject = StringField()
    emailBody = TextAreaField()
    jobDescriptionFile = FileField()
    send = SubmitField()