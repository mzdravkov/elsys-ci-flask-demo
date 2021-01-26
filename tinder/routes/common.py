import os

from flask import render_template, request, flash, redirect
from flask import send_from_directory
from sqlalchemy.sql import func

from tinder import app, db
from tinder.utils import require_login
from tinder.models import User

@app.route('/')
@require_login
def index():
    token = request.cookies.get('token')
    current_user = User.find_by_token(token)
    random_user = User.query.filter(User.id != current_user.id).order_by(func.random()).first()
    i = 0
    users_count = User.query.count()
    while random_user in current_user.likes:
        i += 1
        if i >= users_count:
            random_user = None
            break
        random_user = User.query.filter(User.id != current_user.id).order_by(func.random()).first()
    print(current_user.likes)
    print(current_user.liked_by)

    matches = set(current_user.likes) & set(current_user.liked_by)

    return render_template('index.html', current_user=current_user, random_user=random_user, matches=matches)

@app.route('/like/<id>')
@require_login
def like(id):
    token = request.cookies.get('token')
    current_user = User.find_by_token(token)
    liked_user = User.query.filter_by(id=id).first()
    current_user.likes.append(liked_user)
    db.session.commit()
    flash('<3 {} <3'.format(liked_user.username))
    return redirect('/')


@app.route('/uploads/<filename>')
@require_login
def get_uploaded_file(filename):
    directory = os.path.join('..', app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory, filename)
