from math import *
from plane import Plane

TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3
NEAR = 4
FAR = 5

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
    near_forward = camera.forward_vector * near_distance
    near_right = camera.right_vector * near_half_width
    near_up = camera.up_vector * near_half_height
    far_forward = camera.forward_vector * far_distance
    far_right = camera.right_vector * far_half_widht
    far_up = camera.up_vector * far_half_height

    ntl = origin + near_forward - near_right + near_up
    ntr = origin + near_forward + near_right + near_up
    nbl = origin + near_forward - near_right - near_up
    nbr = origin + near_forward + near_right - near_up
    
    ftl = origin + far_forward - far_right + far_up
    ftr = origin + far_forward + far_right + far_up
    fbl = origin + far_forward - far_right - far_up
    fbr = origin + far_forward + far_right - far_up

    # self.planes[TOP].SetupFromPoints(ntl, ftr, ftl)
    # self.planes[FRONT].SetupFromPoints(ntl, ntr, nbl)
    # self.planes[BOTTOM].SetupFromPoints(nbl, nbr, fbl)
    # self.planes[BACK].SetupFromPoints(ftl, fbl, ftr)
    # self.planes[LEFT].SetupFromPoints(nbl, fbl, ntl)
    # self.planes[RIGHT].SetupFromPoints(nbr, ntr, fbl)

    self.planes[TOP].SetupFromPoints(ntl, ftl, ftr)
    self.planes[BOTTOM].SetupFromPoints(nbl, fbr, fbl)
    self.planes[LEFT].SetupFromPoints(ntl, fbl, ftl)
    self.planes[RIGHT].SetupFromPoints(ntr, ftr, fbr)
    self.planes[NEAR].SetupFromPoints(ntl, ntr, nbr)
    self.planes[FAR].SetupFromPoints(ftr, ftl, fbl)
    return self
  def IsPointInside(self, p, planes):
    """
    Test if point is inside the frustum
    """
    # v = p[:3].copy()
    # v /= p[2]
    # v[2] = p[3]
    for plane in planes:
      if (plane.PointDistance(p[:3]) < 0.0001):
        return False
    return True
  
  def IsPointInsideZ(self, point):
    return self.IsPointInside(point, [self.planes[NEAR], self.planes[FAR]])
  
  def IsPointInsideXY(self, point):
    return self.IsPointInside(point, [self.planes[LEFT], self.planes[RIGHT], self.planes[BOTTOM], self.planes[TOP]])

    
    


