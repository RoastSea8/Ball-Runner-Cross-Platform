import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')


class Ball(Widget):
    pass


class Obstacle(Widget):
    pass


class BallRunner(Widget):
    pass


class BallRunnerApp(App):

    def build(self):
        return BallRunner()


if __name__ == "__main__":
    window = BallRunnerApp()
    window.run()
