from . import app
from flask import render_template, redirect, url_for, flash, request
from .models import User, Image, Result
from .forms import RegisterForm, LoginForm, UploadForm, RegisterDeviceForm, PasswordResetForm, ForgotPasswordForm
from . import db
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
import os
from datetime import datetime
import pytz

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

from flask_mail import Message
# from .email import send_email
from threading import Thread
import _thread

# from .image_processing import process_image

from .analysis import process_image
from .constant import UPLOAD_FOLDER, INPUT_FOLDER

import base64

"""
def send_email(app,msg):
    with app.app_context():
        mail.send(msg)

msg = Message()
msg.subject = "Email Subject"
msg.recipients = ['recipient@gmail.com']
msg.sender = 'tanya.info.hama@gmail.com'
msg.body = 'Email body'
Thread(target=send_email, args=(app, msg)).start()
"""

def create_and_save_result(input_filename, image_id):
    print("Processing Image in new threads")
    result = process_image(input_filename)
    result.image_id = image_id
    db.session.add(result)
    db.session.commit()
    print("Thread is going 2 die")


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/hama_whitefly")
def hama_whitefly():
    return render_template("hama_whitefly.html")

@app.route("/hama_thrips")
def hama_thrips():
    return render_template("hama_thrips.html")

@app.route("/hama_leafminer")
def hama_leafminer():
    return render_template("hama_leafminer.html")

@app.route("/hama_lalatbuah")
def hama_lalatbuah():
    return render_template("hama_lalatbuah.html")


@app.route("/test")
def test_page():
    return render_template("data.html")

@app.route("/data")
def data_page():
    """
    items = [
    {'no': 1, 'times': ['1 Agustus 2021'], 'place': 'lokasi A di kebun ---', 'trap': 'static/images/sample/sample1.png', 'notes': ['Jumlah hama: 14', 'Jenis Hama:', '- whitefly', '']},
    {'no': 2, 'times': ['8 Agustus 2021'], 'place': 'lokasi B di kebun ---', 'trap': 'static/images/sample/sample1.png', 'notes': ['Jumlah hama: 14', 'Jenis Hama:', '- whitefly', '']},
    {'no': 3, 'times': ['18 Agustus 2021', '11:06'], 'place': 'indoor', 'trap': 'static/images/sample/lapangan1.jpeg', 'notes': ['Jumlah hama: 23', 'Jenis Hama:', '- whitefly', '- thripps', '- lalat']},
    {'no': 4, 'times': ['18 Agustus 2021', '11:10'], 'place': 'indoor', 'trap': 'static/images/sample/lapangan2.jpeg', 'notes': ['Jumlah hama: 12', 'Jenis Hama:', '- whitefly', '- thripps']},
    {'no': 5, 'times': ['18 Agustus 2021', '11:11'], 'place': 'indoor', 'trap': 'static/images/sample/lapangan3.jpeg', 'notes': ['Jumlah hama: 5', 'Jenis Hama:', '- thripps', '- lalat']},
    {'no': 6, 'times': ['18 Agustus 2021', '11:13'], 'place': 'indoor', 'trap': 'static/images/sample/lapangan4.jpeg', 'notes': ['Jumlah hama: 3', 'Jenis Hama:', '- thripps', '- lalat']},
    {'no': 7, 'times': ['18 Agustus 2021', '11:13'], 'place': 'outdoor', 'trap': 'static/images/sample/lapangan5.jpeg', 'notes': ['Jumlah hama: 10', 'Jenis Hama:', '- thripps']},
    {'no': 8, 'times': ['18 Agustus 2021', '11:15'], 'place': 'outdoor', 'trap': 'static/images/sample/lapangan6.jpeg', 'notes': ['Jumlah hama: 31', 'Jenis Hama:', '- whitefly', '- thripps', '- lalat']},
    ]
    """
    items = Image.query.all()
    # KalauBlob
    # for item in items:
    #    item.image = item.image.decode("utf-8")

    results = []
    for item in items:

        # Actual
        result = Result.query.filter_by(image_id=item.id).all()

        if len(result) > 0:
            result = result[0]
        else:
            result = None
        """
        # Dummy None
        result=None

        # Dummy Isi
        result = Result(
            image="lalalal",
            total = 100,
            uploaded_at = datetime.utcnow().astimezone(pytz.timezone("Asia/Jakarta")),
            whitefly = 30,
            thripps = 23,
            lalatbuah = 27,
            leafminer = 20,
            damage = 0.02
        )
        """

        item.result = result
    for item in items:
        item.created_at = item.created_at.strftime("%d %B %Y %H:%M")
    print('items:', items)
    return render_template("data.html", items=items)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_page():
    form = UploadForm()
    if request.method == "POST":
        if form.validate_on_submit():
            filename = 'data' + str(len(os.listdir(os.path.join('data', 'static', 'images', 'input')))) + \
                       form.file.data.filename[form.file.data.filename.find("."):]
            # filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join('data', 'static', 'images', 'input', filename))
            print(filename)

            # device_id = form.device.data

            place = form.place.data

            image_to_create = Image(user_id=current_user.id,
                                    # device_id=device_id,
                                    image='static/images/input/' + filename,
                                    place=place)
            db.session.add(image_to_create)
            db.session.commit()
            flash('Success! You have uploaded an image', category='success')
            return redirect(url_for('upload_page'))
        if form.errors != {}:  # if there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error uploading an image: {err_msg}', category='danger')

    if request.method == "GET":
        # if len(Device.query.filter_by(user=current_user.id).all()) > 0:
            return render_template('upload.html', form=form)
        # else:
        #     flash('You do not have any device registered', category='danger')
        #     return redirect(url_for('register_device'))

"""
        if form.validate_on_submit():
            filename = 'data' + str(len(os.listdir(UPLOAD_FOLDER))) + \
                       form.file.data.filename[form.file.data.filename.find("."):]
            # filename = secure_filename(form.file.data.filename)
            form.file.data.save(os.path.join(UPLOAD_FOLDER, filename))
            print(filename)
            print(os.getcwd())
            device_id = form.device.data
            place = form.place.data
            image_to_create = Image(user_id=current_user.id,
                                    device_id=device_id,
                                    image=os.path.join(INPUT_FOLDER, filename),
                                    place=place,
                                    created_at=form.created_at,
                                    updated_at=form.updated_at)
            db.session.add(image_to_create)
            db.session.commit()
            flash('Success! You have uploaded an image', category='success')
            try:
                _thread.start_new_thread(create_and_save_result, (filename, image_to_create.id))
            except:
                print("Error processing Result")

            print("Done Uploading")
            return redirect(url_for('upload_page'))

        if form.errors != {}:  # if there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error uploading an image: {err_msg}', category='danger')

    if request.method == "GET":
        # if len(Device.query.filter_by(user=current_user.id).all()) > 0:
        return render_template('upload.html', form=form)
        # else:
        #     flash('You do not have any device registered', category='danger')
        #     return redirect(url_for('register_device'))
"""

@app.route("/register_user", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user_to_create = User(nama=form.nama.data,
                                  username=form.username.data,
                                  alamat=form.alamat.data,
                                  email_address=form.email_address.data,
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()

            login_user(user_to_create)
            flash('Account created successfully! You are now logged in as: {user_to_create.username}',
                  category='success')
            return redirect(url_for('home_page'))
        if form.errors != {}:  # if there are not errors from the validations
            # error_message = "Error: <br>"
            # for err_msg in form.errors.values():
            #     flash(f'There was an error registering user: {err_msg}', category='danger')
            for field,errs in form.errors.items():
                flash(f'{field} : {", ".join(errs)}', category='danger')
                # for msg in err_msg:
                #     error_message += msg + "<br>"
            # flash(error_message, category='danger')
            # print(error_message)
            return render_template("register.html", form=form)

    if request.method == "GET":
        return render_template("register.html", form=form)

@app.route('/reset', methods=['GET', 'POST'])
def reset_page():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(u"Invalid/Unknown email address.")
            return render_template("reset.html", form=form)
        elif user is not None and form.new_password.data != form.new_pass_confirm.data:
            flash(u"Password mismatch!")
            return render_template("reset.html", form=form)
        else:
            user.passwordUpdated_on = datetime.now()
            user.password = form.new_password.data  # This is my problem line, I guess.
            db.session.add(user)
            db.session.commit()
            flash("Password has been successfully updated!")
            return redirect(url_for("login"))
    return render_template("reset.html", form=form)
#
# # Helper function to redirect User after clicking on password reset link:
# @app.route("/reset/<token>")
# def pwdreset_email(token):
#     try:
#         email = pwdreset_token(token)
#     except:
#         flash("Your password reset link is invalid or has expired.")
#         return redirect(url_for("support"))
#     return redirect(url_for("reset_page"))
#
#
# # User Registration/Signup View:
# @app.route("/forgot_password", methods=["GET","POST"])
# def forgot_password():
#     form = ForgotPasswordForm()
#     if form.validate_on_submit():
#         # If User is registered with us:
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None:
#             flash(u"Unknown email address!")
#             return render_template("reset.html", form=form)
#         # If User is registered and confirmed, sending Password Reset email:
#         if user.confirmed:
#             token = generate_pwdreset_token(user.email)
#             reset_url = url_for("pwdreset_email", token=token, _external=True)
#             html = render_template("password_email.html", confirm_url=reset_url)
#             subject = "Password Reset!"
#             send_email(user.email, subject, html)
#             db.session.add(user)
#             db.session.commit()
#             flash(u"Kindly check registered email for a password reset link!")
#             # Routing User to Login page:
#             return redirect(url_for("login_page"))
#         elif user.confirmed is False:
#             flash(u"Your email address must be confirmed before attempting a password reset.")
#             return redirect(url_for("unconfirmed"))
#     # Rendering a template for User to initiate Password Reset:
#     return render_template("reset.html", form=form)

"""
@app.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):

    user = User.verify_reset_token(token)
    if not user:
        print('no user found')
        return redirect(url_for('app_routes.login'))

    password = request.form.get('password')
    if password:
        user.set_password(password, commit=True)

        return redirect(url_for('app_routes.login'))

    return render_template('reset_verified.html')
"""

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(username=form.username.data).all()
            if len(attempted_user) > 0:
                attempted_user = attempted_user[0]
                if attempted_user and attempted_user.check_password_correction(
                        attempted_password=form.password.data
                ):
                    login_user(attempted_user)
                    flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                    return redirect(url_for('home_page'))
                else:
                    flash('Username and password are not match! Please try again', category='danger')
                    return redirect(url_for('login_page'))
            else:
                flash('User Unknown', category='danger')
                return redirect(url_for('login_page'))
    if request.method == "GET":
        return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


# @app.route("/register_device", methods=["GET", "POST"])
# @login_required
# def register_device():
#     form = RegisterDeviceForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user = current_user.id
#             serial = form.serial.data
#             firmware_version = form.firmware_version.data
#             hardware_version = form.hardware_version.data
#
#             device_to_create = Device(user=user, serial=serial, firmware_version=firmware_version,
#                                       hardware_version=hardware_version)
#             db.session.add(device_to_create)
#             db.session.commit()
#             flash('Success! You have registered a device', category='success')
#             return redirect(url_for('register_device'))
#         if form.errors != {}:  # if there are not errors from the validations
#             for err_msg in form.errors.values():
#                 flash(f'There was an error registering the device: {err_msg}', category='danger')
#
#     if request.method == "GET":
#         return render_template('device.html', form=form)
#

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if request.method == 'POST':
        content = request.json
        """ Dummy Content
            {
                "username": "gabriela",
                "password": "25100099",
                "device_hardware" : "Iphone 5s",
                "place" : "garden 1",
                "image": "..."
            }
        """
        # Authorize user
        attempted_user = User.query.filter_by(username=content["username"]).all()
        if len(attempted_user) > 0:
            attempted_user = attempted_user[0]
            if attempted_user and attempted_user.check_password_correction(
                    attempted_password=content["password"]
            ):
                # Cek apakah device milik user
                # all_devices = Device.query.filter_by(user=attempted_user.id).all()

                # if len(all_devices) > 0:
                #     for device in all_devices:
                #         if device.hardware_version == content["device_hardware"]:
                # decode image
                imgdata = base64.b64decode(content["image"])

                filename = 'data' + str(len(os.listdir(UPLOAD_FOLDER))) + ".jpg"

                with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
                    f.write(imgdata)
                image_to_create = Image(user_id=attempted_user.id,
                                        # device_id=device.id,
                                        image=os.path.join(INPUT_FOLDER, filename),
                                        place=content["place"])
                db.session.add(image_to_create)
                db.session.commit()
                try:
                    _thread.start_new_thread(create_and_save_result, (filename, image_to_create.id))
                except:
                    print("Error processing Result")

                print("Done Uploading")
                return "Success: Upload Image"
                    # else:
                    #     return "Error: Device not found"
                # else:
                #     return "Error: Device not found"
            else:
                return "Error: Unable to login"
        else:
            return "Error: Unable to login"