from manim import *
import numpy as np  

class AnimRays(Scene):
    def construct(self):
        """
        Represents the axes and animates the incident and refracted rays.
        """
        # Create axes
        axes = Axes(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE},
            tips=False,
        )
        
        # Define the incident ray
        incident_ray = Line(start=[-5, 5, 0], end=[0, 0, 0], color=GREEN)

        # Define the refracted ray
        refracted_ray = Line(start=[0, 0, 0], end=[5, -5, 0], color=RED)

        # Define the dioptre
        dioptre = Line(start=[-5, -5, 0], end=[5, 5, 0], color=BLUE)

        # Define the normal line
        normal_line = DashedLine(start=[-5, 5, 0], end=[5, -5, 0], color=WHITE)

        # Define the angle arc
        angle_arc = Arc(
            radius=0.5,
            start_angle=3*PI/4,
            angle=incident_ray.get_angle() - 3*PI/4 + PI,
            arc_center=[0, 0, 0],
            color=WHITE
        )
        
        # Define the angle label
        angle_label = MathTex("i").next_to(angle_arc, UP, buff=0.5)

        # Add the angle label and arc to the scene
        self.add(angle_label, angle_arc)

        # Add the rays, dioptre, and normal line to the scene
        self.add(incident_ray, refracted_ray, dioptre, normal_line)
        
        
        # Animate the rays and update angle label and arc
        self.play(
            Rotate(
                incident_ray, angle=0.5*PI, about_point=incident_ray.get_end(),
                run_time=5, rate_func=linear
            ),
            Rotate(
                refracted_ray, angle=0.5*PI, about_point=incident_ray.get_end(),
                run_time=5, rate_func= lambda t: np.arcsin(np.sin(PI*t/5))
            ),
            UpdateFromFunc(angle_label, lambda m: m.next_to(angle_arc, LEFT, buff=0.5)),
            UpdateFromFunc(angle_arc, lambda m: m.become(                
                Arc(
                    radius=0.5,
                    start_angle=3*PI/4,
                    angle=incident_ray.get_angle() - 3*PI/4 + PI,
                    arc_center=[0, 0, 0],
                    color=WHITE
                )
            ))
        )

        self.wait(2)
            