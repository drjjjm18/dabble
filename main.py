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
from random import choice


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

    def __init__(self, **kwargs):
        super(CardImage, self).__init__(**kwargs)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            print('True')
            gm = App.get_running_app().gm
            gm.card_match = self.image

            if gm.card_match == gm.deck_match:
                App.get_running_app().gm.matched()


class DeckImage(Image):
    image = NumericProperty()

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

    def build(self):
        sm = SM()
        return sm


if __name__ == '__main__':
    DabbleApp().run()
