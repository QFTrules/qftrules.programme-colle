from manim import *
import numpy as np

class VectorField(Scene):
    def construct(self):
        U = 10  # Free stream velocity
        def func(pos):
            # uniform flow
            u = U 
            v = 0
            
            return u * RIGHT + v * UP
        
        # sphere = Circle(radius=R, color=BLUE, fill_opacity=0.3)
        # self.add(sphere)
        
        # represent vector fiels of speed 
        vf = ArrowVectorField(func, length_func=lambda norm: 1, x_range=[-5.5, 4.5, 2], y_range=[-3.5, 3, 1])
        self.add(vf)
        # reduce change image range
     
        # stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=10, dt=0.05, virtual_time=5)
        # self.add(stream_lines)
        # stream_lines.start_animation(warm_up=False, flow_speed=1.25)
        # self.wait(stream_lines.virtual_time / stream_lines.flow_speed)