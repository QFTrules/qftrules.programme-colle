import numpy as np

A = np.array([1, 2, 3])
B = np.array([6, 5, 4])
C = np.array([0, 1, -1])

AvB = np.cross(A, B)
AdB = np.dot(A, B)
AdC = np.dot(A, C)
BvC = np.cross(B, C)
AvBvC = np.cross(A, BvC)

print("AvB = ", AvB)
print("BvC = ", BvC)
print("AvBvC = ", AvBvC)
