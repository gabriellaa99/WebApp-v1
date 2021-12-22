from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User, Device
from flask_wtf.file import FileField
from datetime import datetime, timezone
from flask_login import current_user


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(username=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    nama = StringField(label='Nama Anda:', validators=[Length(min=2, max=30), DataRequired()])
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    alamat = StringField(label='Alamat:', validators=[Length(max=150), DataRequired()])
    email_address = StringField(label='Alamat Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Konfirmasi Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Masuk')

# resetting password
class ForgotPasswordForm(FlaskForm):
    email_address = StringField(label='Alamat Email:', validators=[Email(), DataRequired()])

class PasswordResetForm(FlaskForm):
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])

# Hanya bisa diakses setelah login
class UploadForm(FlaskForm):
    file = FileField()
    # device = SelectField(label='Device:', validators=[DataRequired()])
    place = StringField(label='Lokasi:', validators=[DataRequired()])
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)
    submit = SubmitField(label='Unggah Gambar')

    def __init__(self):
        super(UploadForm, self).__init__()
        # self.device.choices = [(d.id, d.serial) for d in Device.query.filter_by(user=current_user.id).all()]


# Hanya bisa diakses setelah login
class RegisterDeviceForm(FlaskForm):
    serial = StringField(label='Serial Number / Phone Model', validators=[Length(min=2, max=30), DataRequired()])
    firmware_version = StringField(label='Firmware Version / Android Version',
                                   validators=[Length(min=2, max=30), DataRequired()])
    hardware_version = StringField(label='Hardware Version', validators=[Length(min=2, max=30), DataRequired()])



