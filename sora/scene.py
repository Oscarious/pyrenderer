import numpy as np
from light import Light
from primitive import Primitive

class Scene:
  def __init__(self):
    self.ambient_lights = []
    self.directional_lights = []
  def AddAmbientLight(self, light):
    self.ambient_lights.append(light)

  def AddDirectionalLight(self, light):
    self.directional_lights.append(light)

  def AddAmbientLights(self, lights):
    self.ambient_lights = lights
  
  def AddDirectionalLights(self, lights):
    self.directional_lights = lights

  def AddPrimitive(self, primitve):
    self.primitive = primitve
  
  

