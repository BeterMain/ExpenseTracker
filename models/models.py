

class User:
    def __init__(self, name, password, email, account_id, public_id):
        self.name = name
        self.password = password
        self.email = email
        self.account_id = account_id
        self.public_id = public_id
    
    # Getters
    def get_username(self):
        return self.name
    
    def get_password(self):
        return self.password

    def get_email(self):
        return self.email
    
    def get_account_id(self):
        return self.account_id
    
    def get_public_id(self):
        return self.public_id
    
    def __str__(self):
        return f"Username: {self.name}\nEmail: {self.email}\nAccount Id: {self.account_id}\nPublic ID: {self.public_id}"
