import dobble
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, DictProperty, StringProperty
from random import choice, randint, uniform
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import pickle


class Client(Protocol):

    def __init__(self, **kwargs):
        super(Client, self).__init__(**kwargs)
        App.get_running_app().connection = self
        self.app = App.get_running_app()

    def connectionMade(self):
        self.transport.write(pickle.dumps(['join', self.app.name]))

    def dataReceived(self, data):
        msg = pickle.loads(data)
        if msg[0] == 'joined':
            self.app.sm.current = 'waiting'


class NewClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print('Started to connect.')

    def buildProtocol(self, addr):
        print('building protocol')

        # App.get_running_app().gm.ids.nought1.possession = True
        # App.get_running_app().sm.current = "GameScreen"
        # Clock.schedule_interval(App.get_running_app().pitch.tick_move_clock, 1)
        return Client()

    def clientConnectionLost(self, connector, reason):
        pass

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


class GameScreen(Screen):

    cards = ListProperty()
    image_lookup = DictProperty()
    im = NumericProperty(0)
    card_match = NumericProperty(100)
    deck_match = NumericProperty(100)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        App.get_running_app().gm = self
        self.cards = dobble.create_cards()
        self.image_lookup = dobble.image_lookup()

    def matched(self):
        print('match called')

    def on_touch_down(self, touch):
        self.ids.card.images = choice(self.cards)
        self.ids.deck.images = choice(self.cards)


class EnterName(Screen):

    def enter_game(self):
        app = App.get_running_app()
        app.connect_to_server()


class Waiting(Screen):
    pass

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
    name = StringProperty('')

    def build(self):
        sm = SM()
        return sm

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8001, NewClientFactory())  # server: '18.222.132.112' # home server:81.100.102.190


if __name__ == '__main__':
    DabbleApp().run()
