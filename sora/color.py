import numpy as np


class Color:
  def __init__(self, r = 0.0, g = 0.0, b = 0.0, a = 1.0):
    self.r = r
    self.g = g
    self.b = b
    self.a = a
    # self.AssertValue()

  def AssertValue(self):
    assert self.r >= 0.0 and self.r <= 1.0 and self.g >= 0.0 and self.g <= 1.0 and self.b >= 0.0 and self.b <= 1.0 and self.a >= 0.0 and self.a <= 1.0

  def GetVector3f(self):
    return np.array([self.r, self.g, self.b])
  
  def GetVector3i(self):
    return np.array([self.r * 255, self.g * 255, self.b * 255], np.uint) 
  
  def GetVector4(self):
    return np.array([self.r, self.g, self.b, self.a])
  
  def FromVector3i(self, color_vector):
    self.r = color_vector[0] / 255.0
    self.g = color_vector[1] / 255.0
    self.b = color_vector[2] / 255.0
    return self
  
  def FromVector3f(self, color_vector):
    self.r = color_vector[0]
    self.g = color_vector[1]
    self.b = color_vector[2]
    return self
  
  def Multiply(self, color):
    return Color(self.r * color.r, self.g * color.g, self.b * color.b)
  
  def MultiplyNumber(self, val):
    return Color(self.r * val, self.g * val, self.b * val)

  def Accumulate(self, color):
    return Color(self.r + color.r, self.g + color.g, self.b + color.b)
  
  def Clip(self, minVal, maxVal):
    self.r = max(self.r, minVal)
    self.r = min(self.r, maxVal)
    self.g = max(self.g, minVal)
    self.g = min(self.g, maxVal)
    self.b = max(self.b, minVal)
    self.b = min(self.b, maxVal)