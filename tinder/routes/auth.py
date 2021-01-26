import json
import os

from flask import render_template, request, flash, redirect, jsonify

from tinder import app, db
from tinder.models import User
from tinder.utils import allowed_file, random_string, stop_logged_users

@app.route('/register', methods=['GET', 'POST'])
@stop_logged_users
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        description = request.form['description']
        file = request.files['profile_picture']

        if file and file.filename != '' and allowed_file(file.filename):
            file.filename = random_string(48)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        try:
            user = User(
                    username=username,
                    password=password,
                    description=description,
                    picture=file.filename
                    )
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            flash('Error: {}'.format(e))
            return redirect(request.url)

@app.route('/login', methods=['GET', 'POST'])
@stop_logged_users
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})
