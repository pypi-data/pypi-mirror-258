class Client:
    def __init__(self, client_id, ip_address, username, password, dir, python):
        self.client_id = client_id
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.dir = dir
        self.python = python

class Server:
    def __init__(self, ip_address, username, password, dir):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.dir = dir