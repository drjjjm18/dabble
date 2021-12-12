import dobble
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, DictProperty, StringProperty
from random import choice, randint, uniform
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import pickle
from kivy.clock import Clock


class Client(LineReceiver):

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        App.get_running_app().connection = self
        self.app = App.get_running_app()

    def connectionMade(self):
        self.sendLine(pickle.dumps(['join', self.app.name]))

    def lineReceived(self, line):
        msg = pickle.loads(line)
        print(msg)
        if msg[0] == 'players':
            if self.app.sm.current == 'entername':
                self.app.sm.current = 'lobby'
            self.app.rv.players = msg[1:]
            self.app.lobby.latest = msg[-1]
            return
        if msg[0] == 'begin':
            print(msg[1], msg[2])
            self.app.gm.next_deck = msg[1]
            self.app.gm.next_card = msg[2]
            self.app.sm.current = 'gamescreen'
            return
        if msg[0] == 'next':
            self.app.gm.update_cards(deck=msg[1])
            text = f'{msg[2]} got that one!'
            self.app.gm.display_text = text
            return
        if msg[0] == 'win':
            self.app.gm.update_cards(deck=msg[1], card=self.app.gm.ids.deck.images)
            text = f'you got that one!'
            self.app.gm.display_text = text
            return
        if msg[0] == 'over':
            self.app.gm.display_text = 'GAME FINISHED'
            self.app.gm.update_cards(deck=[0, 0, 0, 0, 0, 0, 0, 0])
            Clock.schedule_once(lambda dt: setattr(self.app.sm, 'current', 'results'), 2)
            self.app.results.scores, self.app.results.result_string = msg[1], msg[2]
            return
        return


class NewClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('building protocol')

        return Client()

    def clientConnectionLost(self, connector, reason):
        pass

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


class Results(Screen):

    scores = DictProperty()
    results_string = StringProperty()
    data = DictProperty()
    display_string = StringProperty()

    def __init__(self, **kwargs):
        super(Results, self).__init__(**kwargs)
        App.get_running_app().results = self

    def on_enter(self, *args):
        # for x in range(len(self.scores.keys())):
        #     Clock.schedule_once(lambda dt: setattr(self, 'data', [{'text': f'{y}: {self.scores[y]}'} for y in list(self.scores.keys())[:x+1]]), x+1)
        # Clock.schedule_once(lambda dt: setattr(self, 'display_string', self.results_string), len(self.scores.keys())+1)
        for x in self.scores.keys():
            Lab = Label(text=f'{x} scored: {self.scores[x]}')
            self.add_widget(Lab)


class GameScreen(Screen):

    cards = ListProperty()
    image_lookup = DictProperty()
    #im = NumericProperty(0)
    card_match = NumericProperty(100)
    deck_match = NumericProperty(100)
    display_text = StringProperty()
    next_deck = ListProperty()
    next_card = ListProperty()
    total_cards = NumericProperty(1)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        App.get_running_app().gm = self
        #self.cards = dobble.create_cards()
        self.image_lookup = dobble.image_lookup()

    def matched(self):
        app = App.get_running_app()
        app.connection.sendLine(pickle.dumps(['match']))

    def on_enter(self, *args):
        self.count_down()

    def count_down(self):
        self.display_text = 'Game beginning in...'
        Clock.schedule_once(lambda dt: setattr(self, 'display_text', 'Game beginning in 3'), 2)
        Clock.schedule_once(lambda dt: setattr(self, 'display_text', 'Game beginning in 2'), 3)
        Clock.schedule_once(lambda dt: setattr(self, 'display_text', 'Game beginning in 1'), 4)
        Clock.schedule_once(lambda dt: setattr(self, 'display_text', 'BEGIN'), 5)
        Clock.schedule_once(lambda dt: self.update_cards(self.next_deck, self.next_card), 5)

    def update_cards(self, deck=None, card=None):
        if card is not None:
            self.ids.card.images = card
        if deck is not None:
            self.ids.deck.images = deck

    def leave_game(self):
        app = App.get_running_app()
        app.connection.sendLine(pickle.dumps(['left']))
        app.sm.current = 'lobby'
        ims = [0, 0, 0, 0, 0, 0, 0, 0]
        self.ids.card.images, self.ids.deck.images = ims, ims


class EnterName(Screen):

    def enter_game(self):
        app = App.get_running_app()
        if app.name == '' or str(app.name).lower() == 'amrik':
            app.name = 'xXxCAT4LYF_'+str(randint(10, 99))+'xXx'
        app.connect_to_server()


class Lobby(Screen):
    latest = StringProperty('')
    ready_text = StringProperty()

    def __init__(self, **kwargs):
        super(Lobby, self).__init__(**kwargs)
        App.get_running_app().lobby = self
        self.ready_text = 'Not ready'

    def ready_press(self):
        if self.ready_text == 'Not ready':
            self.ready_text = 'READY!'
            App.get_running_app().connection.sendLine(pickle.dumps(['ready', 'y']))
        else:
            self.ready_text = 'Not ready'
            App.get_running_app().connection.sendLine(pickle.dumps(['ready', 'n']))

    def begin_press(self):
        App.get_running_app().connection.sendLine(pickle.dumps(['begin']))

    def on_enter(self, *args):
        self.ready_text = 'Not ready'


class RV(RecycleView):

    players = ListProperty()

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in self.players]
        App.get_running_app().rv = self

    def on_players(self, instance, value):
        self.data = [{'text': str(x)} for x in self.players]


class Deck(Widget):

    images = ListProperty()
    im = NumericProperty()

    def __init__(self, **kwargs):
        super(Deck, self).__init__(**kwargs)
        self.images = [0, 0, 0, 0, 0, 0, 0, 0]


class Card(Widget):
    images = ListProperty()
    total = NumericProperty(15)

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.images = [0, 0, 0, 0, 0, 0, 0, 0]


class SM(ScreenManager):

    def __init__(self, **kwargs):
        super(SM, self).__init__(**kwargs)
        App.get_running_app().sm = self


class CardImage(Image):
    image = NumericProperty()
    angle = NumericProperty()

    def __init__(self, **kwargs):
        super(CardImage, self).__init__(**kwargs)
        self.angle = randint(0, 360)
        self.rand_x = 0.25
        self.rand_y = 0.5
        self.size_hint = uniform(self.rand_x, self.rand_y), uniform(self.rand_x, self.rand_y)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            print('True')
            gm = App.get_running_app().gm
            gm.card_match = self.image

            if gm.card_match == gm.deck_match:
                App.get_running_app().gm.matched()

    def on_image(self, instance, value):
        self.angle = randint(0, 360)
        self.size_hint = uniform(self.rand_x, self.rand_y), uniform(self.rand_x, self.rand_y)


class DeckImage(CardImage):

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            print('True2')
            gm = App.get_running_app().gm
            gm.deck_match = self.image

            if gm.card_match == gm.deck_match:
                App.get_running_app().gm.matched()


class DabbleApp(App):
    sm = ObjectProperty()
    gm = ObjectProperty()
    lobby = ObjectProperty()
    name = StringProperty('')
    rv = ObjectProperty()
    results = ObjectProperty()

    def build(self):
        sm = SM()
        return sm

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8001, NewClientFactory())  # server: '18.222.132.112' # home server:81.100.102.190


if __name__ == '__main__':
    DabbleApp().run()
