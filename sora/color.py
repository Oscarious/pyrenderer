import numpy as np


class Color:
  def __init__(self, r = 0.0, g = 0.0, b = 0.0, a = 1.0):
    self.r = r
    self.g = g
    self.b = b
    self.a = a
    self.AssertValue()

  def AssertValue(self):
    assert self.r >= 0.0 and self.r <= 1.0 and self.g >= 0.0 and self.g <= 1.0 and self.b >= 0.0 and self.b <= 1.0 and self.a >= 0.0 and self.a <= 1.0

  def GetVector3(self):
    return np.array([self.r, self.g, self.b])
  
  def GetVector3i(self):
    return np.array([self.r * 255, self.g * 255, self.b * 255], np.uint) 
  def GetVector4(self):
    return np.array([self.r, self.g, self.b, self.a])
  