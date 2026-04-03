from manim import *
import numpy as np

class VectorField(Scene):
    def construct(self):
        U = 2  # Free stream velocity
        R = 2  # Radius of the sphere
        def func(pos):
            x, y = pos[0], pos[1]
            r_squared = x**2 + y**2
            r = np.sqrt(r_squared)  # avoid division by zero
            
            # exclude points inside the sphere
            if r < R:
                return np.array([0, 0, 0])
            
            # Potential flow: uniform flow + dipole (sphere effect)
            u = U - U * R**3/r**3/2 * (1+x**2/r_squared)
            v = -U * R**3/r**3/2 * (x*y/r_squared)
            
        #   u = U - U * R**3/2 * (2*x**2 - y**2)/r**5
            # v = -3*U * R**3/2 * (x*y)/r**5
            
            return u * RIGHT + v * UP
        
        sphere = Circle(radius=R, color=BLUE, fill_opacity=0.3)
        self.add(sphere)
        
        # represent vector fiels of speed 
        vf = ArrowVectorField(func, length_func=lambda norm: 0.4)
        self.add(vf)
        
        
        # stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=10, dt=0.05, virtual_time=5)
        # self.add(stream_lines)
        # stream_lines.start_animation(warm_up=False, flow_speed=1.25)
        # self.wait(stream_lines.virtual_time / stream_lines.flow_speed)