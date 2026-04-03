from manim import *
from manim_physics import *
from manim import *

class ProgressiveWave(Scene):
    def construct(self):
        # Create the wave
        wave = FunctionGraph(lambda x: np.sin(x), x_range=[-5, 5], color=BLUE)

        # Create the wavefront
        wavefront = FunctionGraph(lambda x: np.sin(x+2), x_range=[-5, 5], color=BLUE)

        # Create the axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=3,
            axis_config={"color": WHITE},
            x_axis_config={"numbers_to_include": np.arange(-5, 6, 1)},
            y_axis_config={"numbers_to_include": np.arange(-1.5, 1.6, 0.5)},
        )
        self.add(axes)

        # Create animation
        # self.play(ShowCreation(wave))
        # self.play(ShowCreation(wavefront))
        # self.wait(2)

        # Create the propagation animation
        # self.play(MoveAlongPath(wave, axes.get_graph(lambda x: axes.c2p(x, np.sin(x))), run_time=10))

        # self.play(wave.animate.move_to(axes.c2p(-5, 0)), run_time=10)
        self.wait(2)