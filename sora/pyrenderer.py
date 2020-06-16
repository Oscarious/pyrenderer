import cv2
import numpy as np
from rasterizer import *
from framebuffer import FrameBuffer
from color import Color



def CombineRow(vector1, vector2):
  return np.r_[vector1, vector2]

class PyRenderer:
  def __init__(self):
    self.framebuffer = FrameBuffer()

  def RenderWireFrame(self, primitive, camera):
    VBO = primitive.vertex_buffer
    IBO = primitive.index_buffer
    for index in IBO:
      v0, v1, v2 = VBO[index[0][0]-1], VBO[index[1][0]-1], VBO[index[2][0]-1]
      
      v0 = CombineRow(v0, np.asarray([1]))
      v1 = CombineRow(v1, np.asarray([1]))
      v2 = CombineRow(v2, np.asarray([1]))

      v0 = v0.dot(camera.view_matrix)
      v1 = v1.dot(camera.view_matrix)
      v2 = v2.dot(camera.view_matrix)

      RenderTriangle(self.framebuffer, camera.projection_matrix, v0, v1, v2, Color(1, 1, 1))
    
  def Render(self, primitive, camera):
    camera.update_projection_matrix(self.framebuffer.width / self.framebuffer.height)
    while(True):
      self.RenderWireFrame(primitive, camera)
      cv2.imshow('render: ', self.framebuffer.pixel_data)
      key = cv2.waitKey(20)
      camera.update(key)

    


    