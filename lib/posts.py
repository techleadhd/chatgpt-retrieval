class Post:
    def __init__(self, id, message, user_id, timestamp):
        self.id = id
        self.message = message
        self.user_id = user_id
        self.timestamp = timestamp

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __repr__(self):
        return f"Post(id={self.id}, message='{self.message}', user_id={self.user_id}, timestamp='{self.timestamp}')"
