from manim import *
import numpy as np

class VectorField(Scene):
    def construct(self):
        U = 5  # Free stream velocity
        def func(pos):
            x,y = pos[0], pos[1]
            rsquared = x**2 + y**2
            r = np.sqrt(rsquared) + 0.1  # avoid division by zero
            # source flow
            u = U * 1/r**2 * (x**2/rsquared)
            v = U * 1/r**2 * (x*y/rsquared)
            
            return u * RIGHT + v * UP
        
        # sphere = Circle(radius=R, color=BLUE, fill_opacity=0.3)
        # self.add(sphere)
        
        # represent vector fiels of speed 
        vf = ArrowVectorField(func, length_func=lambda norm: 1)
        self.add(vf)
        # reduce change image range
     
        # stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=10, dt=0.05, virtual_time=5)
        # self.add(stream_lines)
        # stream_lines.start_animation(warm_up=False, flow_speed=1.25)
        # self.wait(stream_lines.virtual_time / stream_lines.flow_speed)