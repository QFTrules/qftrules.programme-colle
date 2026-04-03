r = dt/(dx**2*alpha)
assert r <= 0.5,"""simulation risquée dt trop grand ou dx trop petit"""
