from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class Handler(LineOnlyReceiver):
    factory: 'Server'
    login: str

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)
        print(f"{self.login} Disconnected")

    def connectionMade(self):
        self.login = None
        self.factory.clients.append(self)
        print("New Connection")
        self.sendLine("Type your NickName".encode())

    def lineReceived(self, line: bytes):
        message = line.decode()

        if self.login is not None:
            message = f"<{self.login}>: {message}"

            for user in self.factory.clients:
                user.sendLine(message.encode())
        else:
            for user_names in self.factory.clients:
                if user_names.login == message:
                    self.sendLine(f"Логин {user_names.login} занят, попробуйте другой".encode())
                    return
            self.login = message
            print(f"New user: {self.login}")
            self.sendLine(f"Welcome, <{self.login}>!!!".encode())


class Server(ServerFactory):
    protocol = Handler
    clients: list

    def __init__(self):
        self.clients = []

    def startFactory(self):
        print("Server started...")


reactor.listenTCP(
    7410, Server()
)
reactor.run()