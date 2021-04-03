import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
import asyncio

Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '576')

def_x_obs = 1300
def_y_obs = 400

def_x_ball = 20
def_y_ball = 400


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest position = current velocity + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # print(self.pos)


class Obstacle(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest position = current velocity + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

    def has_collided(self, ball):
        return self.collide_widget(ball)


# moving the obstacle by calling move()
class BallRunner(Widget):
    obstacle = ObjectProperty(None)
    ball = ObjectProperty(None)
    event = None

    def moving_obstacle(self):
        self.obstacle.velocity = Vector(-7, 0)

    def update_obstacle(self, dt):
        self.obstacle.move()

        # checks for boundary and resets obstacle position

        if self.obstacle.x <= -160:
            self.obstacle.x = def_x_obs
            self.obstacle.y = def_y_obs

        if self.obstacle.has_collided(self.ball):
            try:
                self.event.cancel()
            except:
                pass
            self.clear_widgets()

    def moving_ball(self):
        self.ball.velocity = Vector(0, 8)

    def update_ball(self, dt):
        self.ball.move()

        # checks if ball has reached climax and changes directions if it has

        if self.ball.y >= 900:
            self.ball.velocity = Vector(0, -8)

        # checks if ball has reached to base and stops if it has

        if self.ball.y <= def_y_ball:
            self.event.cancel()

    def on_touch_down(self, touch):
        self.moving_ball()
        self.event = Clock.schedule_interval(self.update_ball, 1.0/60.0)


class BallRunnerApp(App):

    def build(self):
        game = BallRunner()
        game.moving_obstacle()
        Clock.schedule_interval(game.update_obstacle, 1.0/60.0)
        return game


if __name__ == "__main__":
    window = BallRunnerApp()
    window.run()
