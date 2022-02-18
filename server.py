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
        self.playing = False
        self.score = 0

    def connectionMade(self):
        self.factory.cons.append(self)

    def connectionLost(self, reason):
        self.factory.names.pop(self.name)
        self.factory.cons.remove(self)
        self.update_players()
        self.factory.check_playing()

    def lineReceived(self, data):
        msg = pickle.loads(data)
        x = msg[0]

        if x == 'join':
            self.name = msg[1]
            self.factory.names[self.name] = 0
            self.update_players()

        if x == 'ready':
            if msg[1] == 'y':
                self.ready = True
            else:
                self.ready = False

        if x == 'begin':
            if self.factory.finished:
                self.factory.finished = False
                self.factory.begin_game()

        if x == 'match':
            if not self.factory.won:
                self.factory.won = True
                self.factory.next_card(self)

        if x == 'left':
            self.playing = False
            self.ready = False
            self.factory.check_playing()

    def update_players(self):
        # self.factory.update_player_list()
        msg = pickle.dumps(['players', self.factory.names])
        for x in self.factory.cons:
            x.sendLine(msg)


class QOTDFactory(Factory):

    protocol = QOTD

    def __init__(self):
        self.names = {}
        self.cons = []
        self.cards = []
        self.finished = True
        self.won = False

    def buildProtocol(self, addr):
        return QOTD(self)

    def update_player_list(self):
        print('updating players')
        for x in self.cons:
            msg = pickle.dumps(['players', self.names])
            print(x.name)
            x.sendLine(msg)

    def begin_game(self):
        if not all(x.ready for x in self.cons):
            print('not ready!')
            self.finished = True
        else:
            self.cards = None
            self.cards = dobble.create_cards()

            deckcard = self.cards.pop()
            print(deckcard)
            for x in self.cons:
                card = self.cards.pop()
                print(card)
                x.sendLine(pickle.dumps(['begin', deckcard, card]))
                print(len(self.cards))

            for x in self.cons:
                x.playing = True
                x.ready = False

    def next_card(self, winner):
        if len(self.cards) > 0:
            deckcard = self.cards.pop(0)
            for x in list(filter(lambda y: y.playing, self.cons)):
                if x != winner:
                    x.sendLine(pickle.dumps(['next', deckcard, winner.name]))
            winner.sendLine(pickle.dumps(['win', deckcard]))
            winner.score += 1
            self.won = False

        else:
            winner.score += 1
            players = list(filter(lambda y: y.playing, self.cons))
            scores = {y.name: y.score for y in players}
            result_string = self.find_winner(players)
            for x in players:
                x.sendLine(pickle.dumps(['over', scores, result_string]))
            self.won = False
            self.finished = True
            self.update_player_list()

    def find_winner(self, players):
        print('finding winner')
        if len(players) > 0:
            scores = {x: x.score for x in players}
            max_value = max(scores.values())
            winner = [k for k, v in scores.items() if v == max_value]
            print(f'winner= {winner}')
            if len(winner) == 1:
                self.names[winner[0].name] += 1
                return f'{winner[0].name} wins!'
            else:
                for x in winner:
                    self.names[x.name] += 0.5
                return f'{[x.name for x in winner]} drew'
        else:
            pass

    def check_playing(self):
        if not any(x.playing for x in self.cons):
            self.finished = True


endpoint = TCP4ServerEndpoint(reactor, 8002)
endpoint.listen(QOTDFactory())
reactor.run()
