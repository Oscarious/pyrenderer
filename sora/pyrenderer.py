import cv2
import numpy as np
from rasterizer import Rasterizer
from framebuffer import FrameBuffer
from color import Color
from rasterizer import Rasterizer

class PyRenderer:
  def __init__(self):
    self.framebuffer = FrameBuffer()
    self.rasterizer = Rasterizer()

  def RenderWireFrame(self, primitive, camera):
    VBO = primitive.vertex_buffer
    IBO = primitive.index_buffer
    for index in IBO:
      v0, v1, v2 = VBO[index[0][0]-1], VBO[index[1][0]-1], VBO[index[2][0]-1]
      
      v0 = camera.view_matrix.dot(v0.T).T
      v1 = camera.view_matrix.dot(v1.T).T
      v2 = camera.view_matrix.dot(v2.T).T

      self.rasterizer.RenderTriangle(self.framebuffer, camera.projection_matrix, v0, v1, v2, Color(1, 1, 1))
    
  def draw(self, primitive, camera):

    self.rasterizer.Draw(self.framebuffer, camera.projection_matrix, v0, v1, v2, t0, t1, t2, texture)


  def Resize(self, width, height, camera):
    self.framebuffer.Resize(width, height)
    camera.update_projection_matrix(self.framebuffer.width / self.framebuffer.height)
    
  def Render(self, scene, camera):
    camera.update_projection_matrix(self.framebuffer.width / self.framebuffer.height)
    camera.update()
    while(True):
      # self.RenderWireFrame(primitive, camera)
      self.rasterizer.Draw(self.framebuffer, scene, camera)
      cv2.imshow('render: ', self.framebuffer.pixel_data)
      key = cv2.waitKey(20)
      # if (key == ord('1')):
      scene.primitive.RotateY(-5)
      # elif (key == ord('2')):
      scene.primitive.RotateX(-1)
      camera.update(key)
      self.framebuffer.Clear()

    


    