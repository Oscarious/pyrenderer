import numpy as np
from tinyloader import TinyLoader
from texture import Texture
import matrix 
import math
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
    w_column = np.array([1 for _ in range(self.vertex_buffer.shape[0])])
    self.vertex_buffer = np.c_[self.vertex_buffer, w_column]

  def LoadTexture(self, filename):
    self.texture = Texture(filename)

  def RotateY(self):
    rotate_matrix = matrix.create_rotation_matrix_y(math.radians(1))
    self.vertex_buffer = self.vertex_buffer.dot(rotate_matrix)

