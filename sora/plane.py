import numpy as np

class Plane:
  def __init__(self):
    self.normal = np.array([0, 0, 0])
    self.distance = 0.0

  def SetupFromPoints(self, p0, p1, p2):
    normal = np.cross(p2 - p1, p0 - p1)
    distance = -(normal[0] * p0[0] + normal[1] * p0[1] + normal[2] * p0[2])
    normal_length = np.linalg.norm(normal)
    self.normal = normal / normal_length
    self.distance = distance / normal_length

  def PointDistance(self, p):
    return np.dot(p, self.normal) + self.distance
