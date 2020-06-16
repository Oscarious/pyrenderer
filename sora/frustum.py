from math import *
from plane import Plane


TOP = 0
FRONT = 1
BOTTOM = 2
BACK = 3
LEFT = 4
RIGHT = 5

class Frustum:
  def __init__(self):
    self.planes = [Plane() for _ in range(6)]
  def SetupFromCamera(self, camera):
    tangent = tan(radians(camera.vertical_fov) / 2.0)
    near_distance = camera.near_z
    near_half_height = tangent * near_distance
    near_half_width = near_half_height * camera.aspect_ratio
    far_distance = camera.far_z
    far_half_height = tangent * far_distance
    far_half_widht = far_half_height * camera.aspect_ratio

    origin = camera.position
    near_forward = camera.forward * near_distance
    near_right = camera.right * near_half_width
    near_up = camera.up * near_half_height
    far_forward = camera.farward * far_distance
    far_right = camera.right * far_half_widht
    far_up = camera.up * far_half_height

    ntl = near_forward - near_right + near_up
    ntr = near_forward + near_right + near_up
    nbl = near_forward - near_right - near_up
    nbr = near_forward + near_right - near_up

    ftl = far_forward - far_right + far_up
    ftr = far_forward + far_right + far_up
    fbl = far_forward - far_right - far_up
    fbr = far_forward + far_right - far_up

    self.planes[TOP] = plane.SetupFromPoints(ntl, ftr, ftl)
    self.planes[FRONT] = plane.SetupFromPoints(ntl, ntr, nbl)
    self.planes[BOTTOM] = plane.SetupFromPoints(nbl, nbr, fbl)
    self.planes[BACK] = plane.SetupFromPoints(ftl, fbl, ftr)
    self.planes[LEFT] = plane.SetupFromPoints(nbl, fbl, ntl)
    self.planes[RIGHT] = plane.SetupFromPoints(nbr, ntr, fbl)

  def IsPointInside(self, p):
    """
    Test if point is inside the frustum
    """
    for plane in self.planes:
      if (plane.PointDistance(p) < 0.0001):
        return False
    return True
  

    
    


