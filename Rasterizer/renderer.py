import numpy as np
import cv2
import math
from RenderUtils import *

class MyRenderer:
  def __init__(self, width=800, height=600):
    self.near = 0.1
    self.far = 100
    self.canvas = np.zeros((height, width, 3), np.uint8)
    self.width = width
    self.height = height
    self.perspective_matrix = PerspectiveMatrix(45, width/height, 0.1, 100)
  def SetVertices(self, vertices):
    self.vertices = vertices
  def SetColors(self, colors):
    self.colors = colors
  def SetIndices(self, indices):
    self.indices = indices
  def SetCanvasSize(self, width, height):
    self.width = width
    self.height = height
    self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
  def MapCoords(self, x, y):
    maped_x = self.width / 2 * x + self.width / 2
    maped_y = -self.height / 2 * y + self.height / 2
    return maped_x, maped_y
  def Transform(self, trans_mat=np.identity(4)):
    self.vertices = trans_mat.dot(self.vertices)
  def VertexDraw(self):
    for triangle_indices in self.indices:
      assert(len(triangle_indices) == 3)
      projected_vertices = self.perspective_matrix.dot(self.vertices).T
      attr_vertices = []
      for i in range(len(triangle_indices)):
        x1, y1 = self.MapCoords(projected_vertices[triangle_indices[i]][0] / projected_vertices[triangle_indices[i]][3], projected_vertices[triangle_indices[i]][1] / projected_vertices[triangle_indices[i]][3])
        x2, y2 = self.MapCoords(projected_vertices[triangle_indices[(i+4)%3]][0] / projected_vertices[triangle_indices[(i+4)%3]][3], projected_vertices[triangle_indices[(i+4)%3]][1] / projected_vertices[triangle_indices[(i+4)%3]][3])
        #triangle_vertices.extend(projected_vertices[triangle_indices[i]])
        cv2.line(self.canvas, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 1)
        attr_vertices.extend((x1, y1))
        if (len(self.colors) > i):
          attr_vertices.extend(self.colors[i])
        else:
          attr_vertices.extend([0, 0, 0])
      #self.FragmentDraw(attr_vertices)  
  def FragmentDraw(self, vertices):
    coord_a = [vertices[0], vertices[1]]
    color_a = np.array([
      [vertices[2], vertices[3], vertices[4]]
    ])
    coord_b = [vertices[5], vertices[6]]
    color_b = np.array([
      [vertices[7], vertices[8], vertices[9]]
    ])
    coord_c = [vertices[10], vertices[11]]
    color_c = np.array([
      [vertices[12], vertices[13], vertices[14]]
    ])
    area = EdgeFunction(coord_a, coord_b, coord_c)
    minX, minY, maxX, maxY = GetTriangleBorder(vertices, 5)
    for x in range(int(minX), int(maxX)):
      for y in range(int(minY), int(maxY)):
        w0 = EdgeFunction(coord_a, coord_b, [x, y])
        w1 = EdgeFunction(coord_c, coord_a, [x, y])
        w2 = EdgeFunction(coord_b, coord_c, [x, y])
        if (w0 >= 0 and w1 >= 0 and w2 >= 0):
          w0 /= area
          w1 /= area
          w2 /= area
          color = w0 * color_a * 255 + w1 * color_b * 255 + w2 * color_c * 255
          color = [int(color[0][0]), int(color[0][1]), int(color[0][2])]
          cv2.circle(self.canvas, (x, y), 1, color, 0)
  def Draw(self):
    while(True):
      self.Transform(RotateMatrix(math.radians(2), NormolizeVector([0, 1, 0])))
      self.VertexDraw()
      cv2.imshow('render: ', self.canvas)
      if (cv2.waitKey(20) == ord('q')):
        print('exit')
        break
      self.canvas = np.zeros((self.height, self.width, 3), np.uint8)