from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.user import User
from datetime import datetime

class Message:
    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.recipient_id = data['recipient_id']
        self.sender_id = data['sender_id']
        self.sender = User.get_by_id(data['sender_id']).first_name
        self.recipient = User.get_by_id(data['recipient_id']).first_name
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def get_time(self):
        delta = datetime.now() - self.updated_at
        if delta.total_seconds() // 60 < 1:
            return 'just now'
        elif delta.total_seconds() // 60 < 60:
            return str(delta.total_seconds() // 60) + ' minutes ago'
        elif delta.total_seconds() // 3600 < 24:
            return str(delta.total_seconds() // 3600) + ' hours ago'
        else:
            return str(delta.total_seconds() // 86400) + ' days ago'

    @classmethod
    def get_all_received_messages(cls, id):
        mysql = MySQLConnection('private_wall')
        data = {'id': id}
        query = "SELECT * FROM messages WHERE recipient_id = %(id)s"
        result = mysql.query_db(query, data)
        if result:
            return [cls(message) for message in result]
        return 'No messages'

    @classmethod
    def get_all_sent_messages(cls, id):
        mysql = MySQLConnection('private_wall')
        data = {'id': id}
        query = "SELECT * FROM messages WHERE sender_id = %(id)s"
        result = mysql.query_db(query, data)
        return len(result) #[cls(message) for message in result]
        

    @classmethod
    def create_message(cls, data):
        mysql = MySQLConnection('private_wall')
        query = "INSERT INTO messages (message, sender_id, recipient_id ) VALUES (%(message)s, %(sender_id)s, %(recipient_id)s)"
        return mysql.query_db(query, data)

    @classmethod
    def delete_message(cls, data):
        mysql = MySQLConnection('private_wall')
        query = "DELETE FROM messages WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def update_message(cls, data):
        mysql = MySQLConnection('private_wall')
        query = "UPDATE messages SET message = %(message)s WHERE id = %(id)s"
        return mysql.query_db(query, data)

    @classmethod
    def get_message_by_id(cls, data):
        mysql = MySQLConnection('private_wall')
        query = "SELECT * FROM messages WHERE id = %(id)s"
        result = mysql.query_db(query, data)
        return result[0]

    @classmethod
    def get_user_messages(cls, data):
        mysql = MySQLConnection('private_wall')
        id = {'id': data}
        query = "SELECT * FROM users LEFT JOIN ON user.id = messages.sender_id JOIN users AS recipients ON messages.recipient_id = recipients.id WHERE user.id = %(id)s"  
        result = mysql.query_db(query, id)
        return [cls(message) for message in result]

    @classmethod
    def validate_message(cls, data):
        if len(data['message']) > 5:
            return True
        return False
