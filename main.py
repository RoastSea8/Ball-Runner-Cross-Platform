import kivy
from kivy.app import App
from kivy.uix.widget import Widget


class BallRunnerGame(Widget):
    pass


class BallRunnerApp(App):
    def build(self):
        return BallRunnerGame()


BallRunnerApp().run()
