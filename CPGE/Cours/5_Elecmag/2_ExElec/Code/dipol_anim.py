from manim import *

from manim_physics import *

class ElectricFieldDipole(Scene):
    class ElectricFieldDipole(Scene):
        def construct(self):
            charge1 = Charge(-1, LEFT)
            charge3 = Charge(+1, RIGHT)
            field = ElectricField(charge1, charge3)
            
            self.add(charge1, charge3)
            self.add(field)
            
            equipotentials = Equipotentials(field)
            self.add(equipotentials)
