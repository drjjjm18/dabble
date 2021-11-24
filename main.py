import dobble
from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
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
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, DictProperty


class GameScreen(Screen):
    cards = ListProperty()
    image_lookup = DictProperty()

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        App.get_running_app().gm = self
        self.cards = dobble.create_cards()
        self.image_lookup = {
            1: 'dab1.png',
            -1: 'cat1.png'
        }

    def on_touch_down(self, touch):
        self.ids.deck.images = self.cards[0]
        self.ids.card.images = self.cards[1]
        print(self.ids.deck.images, self.ids.card.images)


class Deck(Widget):
    images = ListProperty()

    def __init__(self, **kwargs):
        super(Deck, self).__init__(**kwargs)
        self.images =[0, 0, 0, 0, 0, 0, 0, 0]


class Card(Widget):
    images = ListProperty()

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.images = [0, 0, 0, 0, 0, 0, 0, 0]


class SM(ScreenManager):

    def __init__(self, **kwargs):
        super(SM, self).__init__(**kwargs)
        App.get_running_app().sm = self


class CardImage(Image):
    image = NumericProperty()


class DeckImage(Widget):
    image = NumericProperty()


class DabbleApp(App):
    sm = ObjectProperty()
    gm = ObjectProperty()

    def build(self):
        sm = SM()
        return sm


if __name__ == '__main__':
    DabbleApp().run()
