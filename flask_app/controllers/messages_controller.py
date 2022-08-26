from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.message import Message
from flask_app.models.user import User

@app.route('/wall')
def wall():
    if 'user_id' in session:
        id = session['user_id']
        sender = User.get_by_id(id)
        received_messages = Message.get_all_received_messages(id)
        sent_messages = Message.get_all_sent_messages(id)
        users = User.get_all_except(id)
        return render_template('wall.html',sender=sender, received_messages=received_messages, sent_messages= sent_messages, users=users, len=len(received_messages))
    return redirect('/')

@app.route('/send_message', methods=['POST'])
def send_message():
    if Message.validate_message(request.form):
        Message.create_message(request.form)
        return redirect('/wall')
    flash('Message must be between 5 and 255 characters','message_error')
    return redirect(url_for('wall'))

@app.route('/delete_message/<int:id>')
def delete_message(id):
    data = {'id':id}
    Message.delete_message(data)
    return redirect(url_for('wall'))