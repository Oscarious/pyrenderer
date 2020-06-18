import json
import os
from light import Light
from color import Color
class TinyLoader:
  def __init__(self):
    self.ambient_lights = []
    self.directional_lights = []
  def load(self, filename):
    print(filename)
    with open(filename, 'r') as f:
      self.data = json.load(f)
      self.loadAmbientLights()
      self.loadDirectionalLights()
    return self.data

  def loadAmbientLights(self):
    lights = self.data['light']['ambient']
    for light in lights:
      self.ambient_lights.append(Light(light['intensity'], Color().FromVector3f(light['color'])))

  def loadDirectionalLights(self):
    lights = self.data['light']['directional']
    for light in lights:
      self.directional_lights.append(Light(light['intensity'], Color().FromVector3f(light['color']), light['pos']))

