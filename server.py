from flask_app import app
from flask_app.controllers import users_controllers
from flask_app.controllers import messages_controller
from flask_app.models.user import User
from flask_app.models.message import Message
from flask import session
from flask_app.controllers import recipes_controller

if __name__ == '__main__':
    app.run(debug=True)
