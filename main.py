import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget


class BallRunner(Widget):
    pass


class BallRunnerApp(App):

    def build(self):
        return BallRunner()


if __name__ == "__main__":
    window = BallRunnerApp()
    window.run()
