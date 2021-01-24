from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from pipe import Pipe

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

class MainApp(App):
    
    def on_start(self):
        # set clock to 60 fps
        Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)

def main():
    MainApp().run()

if __name__ == '__main__':
    main()