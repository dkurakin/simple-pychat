# a = input()
# print(f"It was: {a}")
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver


class Handler(LineOnlyReceiver):

    def lineReceived(self, line):
        print(line.decode())

class Server(ServerFactory):
    protocol = Handler

    def startFactory(self):
        print("Server is running...")

reactor.listenTCP(8443, Server())

reactor.run()

