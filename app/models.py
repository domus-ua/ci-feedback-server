class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tokens = []

    def register_token(self, token):
        self.tokens.append(token)
    
    def delete_token(self, token):
        if token not in self.tokens:
            return False
        else:
            self.tokens.remove(token)
            return True

    def check_credentials(self, username, password):
        return self.username == username and self.password == password

    def __repr__(self):
        return f"User: {self.username}"
