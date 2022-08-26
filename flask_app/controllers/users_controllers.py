from flask import  render_template, request, redirect, url_for, flash, session, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    validation = User.validate_registration(request.form)
    if validation[1]:
        pwd = bcrypt.generate_password_hash(request.form['password'])
        form = {
            'first_name': request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password': pwd
            }
        session['user_id']= User.register(form)
        return jsonify(message ='success')
    else:
        for error in validation[0]:
            return jsonify(message = error)

@app.route('/login', methods=['POST'])
def login():
    user= User.get_by_email(request.form)
    if not user:
        return jsonify(message ='Invalid email')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        return jsonify(message ='Invalid password')
    session['user_id'] = user.id
    return jsonify(message ='success')

@app.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('index'))