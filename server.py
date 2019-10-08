# a = input()
# print(f"It was: {a}")
import time

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class Handler(LineOnlyReceiver):
    factory: 'Server'
    login: str

    def connectionLost(self, reason=connectionDone):
        self.factory.user_list.remove(self)
        print(f"Disconnected user: {self.login}")

    def connectionMade(self):
        self.login = None
        self.factory.user_list.append(self)
        print("New connection")

    def lineReceived(self, line):
        message = line.decode()
        if self.login is not None:
            message = f"<{self.login}>: {message}"
            for user in self.factory.user_list:
                if user is not self:
                    user.sendLine(message.encode())
        else:
            if message.startswith("login:"):
                login = message.replace("login:", "")
                self.login = login
                print(f"New user: {self.login}")
                self.sendLine(f"Welcome, {self.login}!!".encode())
            else:
                self.sendLine("Unreadable login input".encode())


class Server(ServerFactory):
    protocol = Handler
    user_list: list

    def __init__(self):
        self.user_list = []

    def startFactory(self):
        print("Server is running...")


reactor.listenTCP(8443, Server())

reactor.run()