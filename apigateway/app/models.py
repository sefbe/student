from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, first_name, last_name, status):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.status = status

