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
WIDTH = 640
HEIGHT = 480

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
    was_colliding = False
    
    def on_start(self):
        # get holder instance, change holder size relative to the window size
        # and reposition centre of window
        #bck_holder = self.root
        #bck_holder.size_hint = (None, None)
        #bck_holder.size = (WIDTH, HEIGHT)
        #bck_holder.pos_hint = None
        #centre_x = (Window.width / 2) - (bck_holder.width / 2)
        #centre_y = (Window.height / 2) - (bck_holder.height / 2)
        #bck_holder.pos = (centre_x, centre_y)
        # set clock to 60 fps
        pass
    
    def start_game(self):
        self.was_colliding = False
        self.root.ids.score.text = "0"
        self.pipes = []
        # Game Loop
        self.frames = Clock.schedule_interval(self.next_frame, FRAME_RATE)
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
            pipe.pos = (Window.width + (i * distance_between_pipes), 96)
            pipe.size = (64, self.root.height - 96)
            
            self.pipes.append(pipe)
            self.root.add_widget(pipe)
    
    def next_frame(self, time_passed):
        self.root.ids.background.scroll_textures(time_passed)
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
    
    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        #print(f"Bird Y: {bird.y}, Bird Velocity: {bird.velocity}")
        self.check_collisions()
    
    def check_collisions(self):
        bird = self.root.ids.bird
        is_colliding = False
        # check if pipe and bird collide
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                # Make sure that Bird is between Gap
                if bird.y < (pipe.pipe_centre - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_centre + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            bird.y = 96
        if bird.y > Window.height:
            self.game_over()
        
        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text) + 1)
        
        self.was_colliding = is_colliding
    
    def game_over(self):
        self.root.ids.bird.source = "bird1.png"
        self.root.ids.bird.pos = (20, (self.root.height - 96) / 2.0)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.pipes = []
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1
    
    def move_pipes(self, time_passed):
        score = int(self.root.ids.score.text)
        if score > 3:
            pipe_speed = 200
        else:
            pipe_speed = 150
        if self.pipes:
            for pipe in self.pipes:
                # decrment the pipe x position
                pipe.x -= time_passed * pipe_speed
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