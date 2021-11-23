from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import dobble
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen


class GameScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.cards = dobble.create_cards()


class Deck(Widget):
    pass


class Card(Widget):
    pass


class SM(ScreenManager):
    pass


class DabbleApp(App):

    def build(self):
        return GameScreen()


if __name__ == '__main__':
    DabbleApp().run()