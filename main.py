import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')


class Ball(Widget):
    pass


class Obstacle(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest position = current velocity + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# moving the obstacle by calling move()
class BallRunner(Widget):
    obstacle = ObjectProperty(None)

    def moving_obstacle(self):
        self.obstacle.velocity = Vector(-4, 0)

    def update(self, dt):
        self.obstacle.move()


class BallRunnerApp(App):

    def build(self):
        game = BallRunner()
        game.moving_obstacle()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == "__main__":
    window = BallRunnerApp()
    window.run()
