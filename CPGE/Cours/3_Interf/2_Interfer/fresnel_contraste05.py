from manim import *

class FresnelC05(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=(-2, 2, 1),
            y_range=(-2, 2, 1),
            x_length=6,
            y_length=6,
            axis_config={"color": WHITE},
            tips=False,
        )

        # Create two vectors
        vector1 = Arrow(start=[0, 0, 0], end=[1, 1, 0], buff=0, color=BLUE)
        vector1_label = Tex("$\\underline{s}_1$", color=BLUE).next_to(vector1, 0.3*RIGHT)
        vector1_group = Group(vector1, vector1_label)

        vector2 = Arrow(start=vector1.get_end(), end=[1.5, 1.5, 0], buff=0, color=RED)
        vector2_label = Tex("$\\underline{s}_2$", color=RED).next_to(vector2.get_end(), 0.5 * vector2.get_unit_vector())
        vector2_group = Group(vector2, vector2_label)
        
        # Create the sum of the vectors
        sum_vector = Arrow(start=[0, 0, 0], end=vector2.get_end(), buff=0, color=GREEN)
        
        # Add the axes and vectors to the scene
        self.add(axes, vector1_group, sum_vector, vector2_group)

        # Add the legend
        legend1 = Tex("interférences").move_to([3, 3.5, 0])
        legend2 = Tex("constructives").move_to([3, 3, 0])
        self.add(legend1,legend2)
        self.wait(2)
        self.remove(legend1,legend2)

        # Rotate only the end of vector1 at constant frequency
        self.play(
            Rotate(vector2, angle=0.5*TAU, about_point=vector1.get_end(), run_time=5, rate_func=linear),
            UpdateFromFunc(sum_vector, lambda m: m.become(Arrow(start=[0, 0, 0], end=vector2.get_end(), buff=0, color=GREEN))),
            UpdateFromFunc(vector2_label, lambda m: m.next_to(vector2.get_end(),  0.4*UP + 0.1 * LEFT))
        )

        # Add the legend
        legend1 = Tex("interférences").move_to([3, 3.5, 0])
        legend2 = Tex("destructives").move_to([3, 3, 0])
        self.add(legend1,legend2)
        self.wait(2)
        # self.remove(legend1,legend2)

