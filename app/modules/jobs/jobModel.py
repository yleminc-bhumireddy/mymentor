from app import db
from enum import Enum
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.fields import StringField, TextAreaField, IntegerField, FileField


class Status(Enum):
    ACTIVE = 'Y'
    IN_ACTIVE = 'N'


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    primary_address = db.Column(db.Text)
    poc = db.Column(db.String(100))

    # is_active = db.Column(db.Enum(Status))

    def __repr__(self):
        return str(self.name)


class Job(db.Model):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    locations = db.Column(db.String(100))
    jd = db.Column(db.String(100))
    skillset = db.Column(db.String(100))

    # name = db.Column(db.String(100))
    # name = db.Column(db.String(100))

    def __repr__(self):
        return str(self.name)


class NewJobForm(FlaskForm):
    companyId = StringField()
    jobId = IntegerField()
    name = StringField()
    locations = StringField()
    jd = TextAreaField()
    jd_file = FileField()
    skillset = StringField()
