from manim import *

class StreamFlow(Scene):
    def construct(self):
        # Define the parameters
        v_0 = 1
        a = 1.5

        # Create the vector field
        def vector_field_func(point, alpha):
            x = point[0]
            y = point[1]
            r = np.sqrt(x**2 + y**2)
            vr = v_0 * (1 - (a**2) / (r**2)) * x/r
            vtheta = v_0 * (alpha * a / r - (1 + (a**2) / (r**2)) * y/r)
            vx = vr * x/r - vtheta * y/r
            vy = vr * y/r + vtheta * x/r
            return np.array([vx, vy, 0])

        # Add vector field
        vector_field0 = ArrowVectorField(lambda point: vector_field_func(point, 0), x_range=[-7, 7, 0.38], y_range=[-4, 4, 0.38])  
        self.add(vector_field0)
        
        # Add black disk
        black_disk = Circle(radius=a, fill_color=BLACK, fill_opacity=1)
        self.add(black_disk)

        # Add alpha legend
        alpha_legend = MathTex("\\frac{a\\Omega}{U} = 0.0", fill_color=WHITE, background_stroke_color=BLACK, background_stroke_width=1)
        # alpha_legend.to_corner(UL)
        self.add(alpha_legend)

        # Add blue dots for zero points
        blue_dot1 = Dot([a, 0, 0], color=BLUE, radius=0.1)
        blue_dot2 = Dot([-a, 0, 0], color=BLUE, radius=0.1)
        self.add(blue_dot1)
        self.add(blue_dot2)
        self.wait(5)

        for alpha in np.arange(0.5, 3.5, 0.5):
            vector_field = ArrowVectorField(lambda point: vector_field_func(point, alpha), x_range=[-7, 7, 0.38], y_range=[-4, 4, 0.38])    
            if alpha <= 2:    
                self.play(vector_field0.animate.become(vector_field),
                        blue_dot1.animate.become(Dot([a*np.sqrt(1 - alpha**2/4), a*alpha/2, 0], color=BLUE, radius=0.1)),
                        blue_dot2.animate.become(Dot([-a*np.sqrt(1 - alpha**2/4), a*alpha/2, 0], color=BLUE, radius=0.1)),
                        alpha_legend.animate.become(MathTex("\\frac{a\\Omega}{v_0} = %.1f" % (alpha), fill_color=WHITE, background_stroke_color=BLACK, background_stroke_width=1)))
            if alpha > 2:
                self.play(vector_field0.animate.become(vector_field),
                        blue_dot1.animate.become(Dot([0, a/2*(np.sqrt(alpha**2-4)+alpha), 0], color=BLUE, radius=0.1)),
                        blue_dot2.animate.become(Dot([0, a/2*(np.sqrt(alpha**2-4)+alpha), 0], color=BLUE, radius=0.1)),
                        alpha_legend.animate.become(MathTex("\\frac{a\\Omega}{v_0} = %.1f" % (alpha), fill_color=WHITE, background_stroke_color=BLACK, background_stroke_width=1)))
            self.wait()
        self.wait(2)
