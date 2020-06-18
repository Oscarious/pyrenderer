import numpy as np
from color import Color
from vector import *
DIRECTIONAL = 0
AMBIENT = 1

class Light:
  def __init__(self, intensity, color = Color(1.0, 1.0, 1.0) , pos = [0, 0, 15]):
    self.intensity = intensity
    self.color = color
    self.pos = pos

  def affect(self, attributes):
    return Color().FromVector3f(attributes.GetVector3f() * self.color.GetVector3f()).GetVector3i() * self.intensity

  def diffuse(self, frag_pos, frag_normal):
    light_dir = self.pos - frag_pos
    light_dir = get_normalized_vector(light_dir)
    frag_normal = get_normalized_vector(frag_normal)
    intensity = max(0.0, np.dot(light_dir, frag_normal)) * self.intensity
    return intensity


class AmbientLight(Light):
  def __init__(self, intensity, color = Color(1.0, 1.0, 1.0) , pos = [0, 0, 15]):
    super.__init__(self, intensity, color, pos)
  