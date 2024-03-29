from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from random import shuffle

from app.models import *
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():

    if current_user.is_authenticated:
        posts = Posts.query.all()
        shuffle(posts)

        return render_template('index.html', posts=posts)

    else:
        return redirect(url_for('routes.auth.login'))

@views.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard():

    posts = Posts.query.filter_by(user=current_user).all()

    return render_template('dashboard.html', posts=posts, upload_path='static/uploads/')

@views.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_post():
    if request.method == 'POST':

        file = request.files['image']
        caption = request.form.get('caption')
        date_created = datetime.now()
        filename = secure_filename(f"{current_user.id}_{str(date_created.date()).replace('-','')}_{date_created.second}.png")
        file_url = os.path.join('./app/static/uploads', filename)
        file_url = os.path.normpath(file_url)
        print(file_url)
        file.save(file_url)

        post = Posts(post_name=filename, caption=caption,date_created=date_created,user=current_user)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('routes.views.home'))

    return render_template('upload.html')

