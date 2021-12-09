from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor, task
import pickle


class QOTD(Protocol):

    def __init__(self, factory):

        self.factory = factory

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def dataReceived(self, data):
        msg = pickle.loads(data)
        x = msg[0]
        if x == 'join':
            self.factory.names.append(msg[1])
            print(self.factory.names)
            self.transport.write(pickle.dumps(['joined']))


class QOTDFactory(Factory):

    protocol = QOTD

    def __init__(self):
       self.names = []

    def buildProtocol(self, addr):

        return QOTD(self)


endpoint = TCP4ServerEndpoint(reactor, 8001)
endpoint.listen(QOTDFactory())
reactor.run()
