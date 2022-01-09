from . import db, login_manager
from . import bcrypt
from flask_login import UserMixin
import datetime
import pytz

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    nama = db.Column(db.String(length=100), nullable=False, unique=True)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    alamat = db.Column(db.String(length=100), nullable=False)
    email_address = db.Column(db.String(length=100), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=100), nullable=False)
    # devices = db.relationship('Device', backref='owned_user', lazy=True)
    images = db.relationship('Image', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

#
# class Device(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     serial = db.Column(db.String(length=30), nullable=False, unique=True)
#     firmware_version = db.Column(db.String(length=30), nullable=False, unique=True)
#     hardware_version = db.Column(db.String(length=30), nullable=False, unique=True)
#     user = db.Column(db.Integer(), db.ForeignKey('user.id'))
#     def __repr__(self):
#         return f'Item {self.name}'


class Image(db.Model):
    #idImage
    #lokasi
    #waktu_dibuat/upload
    current_time = datetime.datetime.now(pytz.timezone("Asia/Jakarta"))
    print(current_time)
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    # device_id = db.Column(db.Integer(), db.ForeignKey('device.id'))#ga btuh
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now(pytz.timezone("Asia/Jakarta")))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now(pytz.timezone("Asia/Jakarta")))
    image = db.Column(db.String(length=300), nullable=False)
    place = db.Column(db.String(length=100), nullable=False)

# ganti jadi hasil
class Result(db.Model):
    #idHasil
    id = db.Column(db.Integer(), primary_key=True)
    image_id = db.Column(db.Integer(), db.ForeignKey('image.id'))
    image = db.Column(db.String(length=300), nullable=False)#ga butuh
    total = db.Column(db.Integer(), nullable=False, default=0)
    #waktu_upload
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now(pytz.timezone("Asia/Jakarta")))
    whitefly = db.Column(db.Integer(), nullable=False, default=0)
    # thripps = db.Column(db.Integer(), nullable=False, default=0)
    # lalatbuah = db.Column(db.Integer(), nullable=False, default=0)
    # leafminer = db.Column(db.Integer(), nullable=False, default=0)
    damage = db.Column(db.Float(), nullable=False, default=0.0)
