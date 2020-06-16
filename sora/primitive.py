import numpy as np
from tinyloader import TinyLoader

class Primitive:
  def __init__(self):
    # self.vertex_buffer = []
    # self.texture_buffer = []
    # self.index_buffer = []
    # self.normal_buffer = []
    pass
  
  def LoadModel(self, filename):
    loader = TinyLoader()
    model_data = loader.load(filename)
    self.vertex_buffer = np.asarray(model_data['vertex'])
    self.texture_buffer = np.asarray(model_data['texture'])
    self.normal_buffer = np.asarray(model_data['normal'])
    self.index_buffer = model_data['face']

