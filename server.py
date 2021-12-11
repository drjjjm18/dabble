from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor, task
import pickle
import dobble


class QOTD(LineReceiver):

    def __init__(self, factory):

        self.factory = factory
        self.name = None
        self.ready = False

    def connectionMade(self):
        self.factory.cons.append(self)

    def connectionLost(self, reason):
        self.factory.names.remove(self.name)
        self.factory.cons.remove(self)
        self.update_players()

    def dataReceived(self, data):
        msg = pickle.loads(data)
        x = msg[0]
        print(x)
        if x == 'join':
            self.name = msg[1]
            self.factory.names.append(self.name)
            self.update_players()

        if x == 'ready':
            if msg[1] == 'y':
                self.ready = True
            else:
                self.ready = False

        if x == 'begin':
            if not self.factory.starting:
                self.factory.starting = True
                self.factory.begin_game()

        if x == 'match':
            if not self.factory.won:
                self.factory.won = True
                self.factory.next_card(self)

    def update_players(self):
        # self.factory.update_player_list()
        l1 = ['players']
        msg = pickle.dumps(l1 + self.factory.names)
        for x in self.factory.cons:
            x.sendLine(msg)


class QOTDFactory(Factory):

    protocol = QOTD

    def __init__(self):
        self.names = []
        self.cons = []
        self.starting = False
        self.cards = []
        self.finished = False
        self.won = False

    def buildProtocol(self, addr):
        return QOTD(self)

    def update_player_list(self):
        print('updating players')
        for x in self.cons:
            l1 = ['players']
            msg = pickle.dumps(l1 + self.names)
            print(x.name)
            x.sendLine(msg)

    def begin_game(self):
        if not all(x.ready for x in self.cons):
            print('not ready!')
            self.starting = False
        else:

            self.cards = dobble.create_cards()
            deckcard = self.cards.pop(0)
            for x in self.cons:
                card = self.cards.pop(0)
                x.sendLine(pickle.dumps(['begin', deckcard, card]))
                print(len(self.cards))
            self.starting = False
            for x in self.cons:
                x.ready = False

    def next_card(self, winner):
        if len(self.cards) > 0:
            deckcard = self.cards.pop(0)
            for x in self.cons:
                if x != winner:
                    x.sendLine(pickle.dumps(['next', deckcard]))
            winner.sendLine(pickle.dumps(['win', deckcard]))
            self.won = False


endpoint = TCP4ServerEndpoint(reactor, 8001)
endpoint.listen(QOTDFactory())
reactor.run()
