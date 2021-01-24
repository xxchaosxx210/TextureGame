from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from pipe import Pipe
import random

FRAME_RATE = 1/60.

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        # Create Textures
        self.cloud_texture = Image(source="cloud.png").texture
        self.cloud_texture.wrap = "repeat"
        self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
        
        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = "repeat"
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)
        
    def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        cloud_x_speed = 2.0
        new_uvpos_x = (self.cloud_texture.uvpos[0] + time_passed / cloud_x_speed) % Window.width
        new_uvpos_y = self.cloud_texture.uvpos[1]
        #print(f"X: {new_uvpos_x}, Y: {new_uvpos_y}")
        self.cloud_texture.uvpos = (new_uvpos_x, new_uvpos_y)
        # Redraw the texture
        texture = self.property("cloud_texture")
        texture.dispatch(self)
        
        floor_x_speed = 1.0
        new_uvpos_x = (self.floor_texture.uvpos[0] + time_passed / floor_x_speed) % Window.width
        self.floor_texture.uvpos = (new_uvpos_x, self.floor_texture.uvpos[1])
        texture = self.property("floor_texture")
        texture.dispatch(self)


class Bird(Image):
    
    velocity = NumericProperty(0)
    
    def on_touch_down(self, touch):
        self.source = "bird2.png"
        self.velocity = 150
        super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        self.source = "bird1.png"
        super().on_touch_up(touch)

class MainApp(App):
    
    pipes = []
    GRAVITY = 300
    
    def on_start(self):
        # set clock to 60 fps
        Clock.schedule_interval(self.root.ids.background.scroll_textures, FRAME_RATE)
    
    def start_game(self):
        Clock.schedule_interval(self.move_bird, FRAME_RATE)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.pipes = []
        # Create the pipes
        # 5 Pipes per screen
        num_pipes = 5
        # create the distance between the pipes
        distance_between_pipes = Window.width / (num_pipes - 1)
        # create the Pipes
        for i in range(num_pipes):
            pipe = Pipe()
            # set the pipe centre positioning randomly
            pipe.pipe_centre = random.randint(96 + 100, self.root.height - 100)
            pipe.size_hint = (None, None)
            # spawn pipe off screen plus the offset distance between the pipes
            pipe.pos = (i * distance_between_pipes, 96)
            pipe.size = (64, self.root.height - 96)
            
            self.pipes.append(pipe)
            self.root.add_widget(pipe)
            
        # Move the pipes
        Clock.schedule_interval(self.move_pipes, FRAME_RATE)
    
    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        print(f"Bird Y: {bird.y}, Bird Velocity: {bird.velocity}")
    
    def move_pipes(self, time_passed):
        for pipe in self.pipes:
            # decrment the pipe x position
            pipe.x -= time_passed * 100
        # check if pipe is moved off screen
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        # find the highest x position in the pipes list
        right_most_x = max(pipe_xs)
        num_pipes = 5
        # create the distance between the pipes
        distance_between_pipes = Window.width / (num_pipes - 1)
        # check if the furthest pipe to the right is off the screen
        if right_most_x <= Window.width - distance_between_pipes:
            # move the leftist pipe back to the right hand of the screen
            most_left_pipe_index = pipe_xs.index(min(pipe_xs))
            most_left_pipe = self.pipes[most_left_pipe_index]
            most_left_pipe.x = Window.width

def main():
    MainApp().run()

if __name__ == '__main__':
    main()