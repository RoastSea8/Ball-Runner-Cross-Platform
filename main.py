import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import *

def_x_obs = 1300
def_y_obs = 200

def_x_ball = 20
def_y_ball = 200

obs_right_end = -160
ball_max_height = 800


class Background(Widget):
    grass_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size = Window.size
        self.pos = (0, 0)

        # Create textures
        self.grass_texture = Image(source="images/grass.jpg").texture
        self.grass_texture.wrap = 'repeat'
        self.grass_texture.uvsize = (Window.width / self.grass_texture.width, -1)
        self.time_passed = 0

    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        self.time_passed = time_passed
        self.grass_texture.uvpos = ((self.grass_texture.uvpos[0] + self.time_passed/2.0) % Window.width, self.grass_texture.uvpos[1])
        print(self.time_passed)

        # Redraw the texture
        texture = self.property('grass_texture')
        texture.dispatch(self)


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
class BallRunner(Background, Widget):
    obstacle = ObjectProperty(None)
    ball = ObjectProperty(None)
    event = None
    current_touch = None
    img = None
    obs_start_spd = -7.0
    ball_start_down_spd = -8

    def moving_obstacle(self):
        self.obstacle.velocity = Vector(self.obs_start_spd, 0)

    def update_obstacle(self, dt):
        self.obstacle.move()

        # checks for boundary and resets obstacle position

        if self.obstacle.x <= obs_right_end:
            self.obstacle.x = def_x_obs
            self.obstacle.y = def_y_obs
            self.obs_start_spd -= .5
            self.obstacle.velocity = Vector(self.obs_start_spd, 0)
            self.ball_start_down_spd -= .2
            self.ball.velocity = Vector(0, self.ball_start_down_spd)
            self.time_passed += .5
            print(self.time_passed)

        if self.obstacle.has_collided(self.ball):
            try:
                self.event.cancel()
            except:
                pass
            self.grass_texture.uvpos = (0, 0)
            self.obstacle.velocity = Vector(0, 0)
            with self.canvas:
                explosion = Rectangle(source="images/explosion.png", pos=(self.ball.x-self.ball.width, self.ball.y-self.ball.height), size=(250, 250))

    def moving_ball(self):
        self.ball.velocity = Vector(0, 11)

    def update_ball(self, dt):
        self.ball.move()

        # checks if ball has reached climax and changes directions if it has

        if self.ball.y >= ball_max_height:
            self.ball.velocity = Vector(0, self.ball_start_down_spd)

        # checks if ball has reached to base and stops if it has

        if self.ball.y <= def_y_ball:
            self.event.cancel()
            self.current_touch = None  # allows for else-statement to pass in on_touch_down

    def on_touch_down(self, touch):
        # returns if touch object is received more than once in a single jump command
        if self.current_touch is not None:
            return
        else:
            self.current_touch = touch
            self.moving_ball()
            self.event = Clock.schedule_interval(self.update_ball, 1.0/60.0)


class BallRunnerApp(App):
    def on_start(self):
        Clock.schedule_interval(self.root.ids._background.scroll_textures, 1/120.0)

    def build(self):
        game = BallRunner()
        game.moving_obstacle()
        Clock.schedule_interval(game.update_obstacle, 1/360.0)
        return game


if __name__ == "__main__":
    window = BallRunnerApp()
    Window.maximize()
    window.run()
