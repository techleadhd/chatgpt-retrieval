class User:
    def __init__(self, id, name, username, password, email):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.email = email

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', username='{self.username}', email='{self.email}')"