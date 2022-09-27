from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import StringField, TextAreaField, IntegerField, FileField, SubmitField
from flask_ckeditor import CKEditorField


class EmailForm(FlaskForm):
    totalSent = 0
    companyId = StringField()
    tolist = StringField()
    subject = StringField()
    emailBody = CKEditorField()
    jobDescriptionFile = FileField()
    send = SubmitField()