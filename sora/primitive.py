import numpy as np
from tinyloader import TinyLoader
from texture import Texture
import matrix 
import math
from light import Light
from color import Color
class Primitive:
  def __init__(self, model_data):
    self.vertex_buffer = np.asarray(model_data['vertex'])
    self.texture_buffer = np.asarray(model_data['texture'])
    self.normal_buffer = np.asarray(model_data['normal'])
    self.index_buffer = model_data['face']
    w_column = np.array([1 for _ in range(self.vertex_buffer.shape[0])])
    self.vertex_buffer = np.c_[self.vertex_buffer, w_column]
    w_column = np.array([1 for _ in range(self.normal_buffer.shape[0]) ])
    self.normal_buffer = np.c_[self.normal_buffer, w_column]
  def LoadTexture(self, filename):
    self.texture = Texture(filename)

  def RotateY(self, degree):
    rotate_matrix = matrix.create_rotation_matrix_y(math.radians(degree))
    self.vertex_buffer = self.vertex_buffer.dot(rotate_matrix)
    self.normal_buffer = self.normal_buffer.dot(rotate_matrix)

  def RotateX(self, degree):
    rotate_matrix = matrix.create_rotation_matrix_x(math.radians(degree))
    self.vertex_buffer = self.vertex_buffer.dot(rotate_matrix)
    self.normal_buffer = self.normal_buffer.dot(rotate_matrix)