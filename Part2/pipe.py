from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

class Pipe(Widget):
    # Numeric Attributes
    GAP_SIZE = NumericProperty(60)
    CAP_SIZE = NumericProperty(20) # Height of pipe_cap.png
    pipe_centre = NumericProperty(0)
    bottom_body_position = NumericProperty(0)
    bottom_cap_position = NumericProperty(0)
    top_body_position = NumericProperty(0)
    top_cap_position = NumericProperty(0)
    
    # Texture
    pipe_body_texture = ObjectProperty(None)
    lower_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    top_pipe_tex_coords = ListProperty((0, 0, 1, 0, 1, 1, 0, 1))
    
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        self.pipe_body_texture = Image(source="pipe_body.png").texture
        self.pipe_body_texture.wrap = "repeat"
    
    def on_size(self, *args):
        lower_body_size = self.bottom_cap_position - self.bottom_body_position
        self.lower_pipe_tex_coords[5] = lower_body_size / 20.
        self.lower_pipe_tex_coords[7] = lower_body_size / 20.
        
        top_body_size = self.top - self.top_body_position
        self.top_pipe_tex_coords[5] = top_body_size/20.0
        self.top_pipe_tex_coords[7] = top_body_size/20.0