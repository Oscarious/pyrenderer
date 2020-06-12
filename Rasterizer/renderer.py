import numpy as np
import cv2
import math
from RenderUtils import *
from multiprocessing.dummy import Pool
from functools import partial
from ControlUtils import *
import os
from data import Light

class MyRenderer:
  def __init__(self, width=800, height=600):
    self.near = 0.1
    self.far = 100
    self.canvas = np.zeros((height, width, 3), np.uint8)
    self.width = width
    self.height = height
    self.perspective_matrix = PerspectiveMatrix(45, width/height, 0.1, 100)
    self.rotate = False
    self.zbuffer = np.full((self.height, self.width), -9999.9, dtype=np.float)
    self.colorbuffer = np.zeros((self.height, self.width, 3), np.uint8)
  def SetLight(self, light):
    self.light = light
  def SetVertices(self, vertices):
    self.vertices = vertices
  def SetIndices(self, indices):
    self.indices = indices
  def SetCanvasSize(self, width, height):
    self.width = width
    self.height = height
    self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
    self.colorbuffer = np.zeros((self.height, self.width, 3), np.uint8)
    self.zbuffer = np.full((self.height, self.width), -9999)
  def SetNormals(self, normals):
    self.normals = normals
  def MapCoords(self, x, y):
    maped_x = self.width / 2 * x + self.width / 2
    maped_y = -self.height / 2 * y + self.height / 2
    return maped_x, maped_y
  def Transform(self, trans_mat=np.identity(4)):
    if (self.rotate):
      self.vertices[:,0:4] = trans_mat.dot(self.vertices[:,0:4].T).T
  def VertexDraw(self):
    coords_z = [] 
    view_vertices = view_mat.dot(self.vertices[:,0:4].T).T
    projected_vertices = self.perspective_matrix.dot(view_vertices.T).T
    triangle_count = 0
    for triangle_indices in self.indices:
      assert(len(triangle_indices) == 3)
      for i in range(len(triangle_indices)):
        coords_z.append(projected_vertices[triangle_indices[i]][2])
      attr_vertices = []
      normals = []
      orig_vertices = []
      for i in range(len(triangle_indices)):
        x1, y1 = self.MapCoords(projected_vertices[triangle_indices[i]][0] / projected_vertices[triangle_indices[i]][3], projected_vertices[triangle_indices[i]][1] / projected_vertices[triangle_indices[i]][3])
        x2, y2 = self.MapCoords(projected_vertices[triangle_indices[(i+4)%3]][0] / projected_vertices[triangle_indices[(i+4)%3]][3], projected_vertices[triangle_indices[(i+4)%3]][1] / projected_vertices[triangle_indices[(i+4)%3]][3])
        #triangle_vertices.extend(projected_vertices[triangle_indices[i]])
        cv2.line(self.canvas, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 1)
        attr_vertex = [(x1, y1), self.vertices[triangle_indices[i]][4:7]]
        # attr_vertex.extend((x1, y1))
        # attr_vertices.extend(self.vertices[triangle_indices[i]][4:7])
        attr_vertices.append(attr_vertex)
        index = i+triangle_count*len(triangle_indices)
        normals.append(self.normals[index])
        orig_vertices.append(self.vertices[index])
      triangle_count+=1
      self.FragmentDraw(attr_vertices, coords_z, orig_vertices, normals)  
  def FragmentDraw(self, vertices, coords_z, orig_vertices, normals):
    coord_a = vertices[0][0]
    color_a = vertices[0][1]
    coord_b = vertices[1][0]
    color_b = vertices[1][1]
    coord_c = vertices[2][0]
    color_c = vertices[2][1]
    area = EdgeFunction(coord_a, coord_b, coord_c)
    coords_2d = [vertices[0][0], vertices[1][0], vertices[2][0]]
    minX, minY, maxX, maxY = GetTriangleBorder(coords_2d)
    for x in range(int(minX), int(maxX)):
      for y in range(int(minY), int(maxY)):
        w0 = EdgeFunction(coord_a, coord_b, [x, y])
        w1 = EdgeFunction(coord_c, coord_a, [x, y])
        w2 = EdgeFunction(coord_b, coord_c, [x, y])
        if (w0 >= 0 and w1 >= 0 and w2 >= 0):
          inter_coord_z = 1 / (w0 / coords_z[0] + w1 / coords_z[1] + w2 / coords_z[2])
          inter_coord_x = (w0 * orig_vertices[0][0] + w1 * orig_vertices[1][0] + w2 * orig_vertices[2][0]) / area
          inter_coord_y = (w0 * orig_vertices[0][1] + w1 * orig_vertices[1][1] + w2 * orig_vertices[2][1]) / area
          inter_normal = (w0 * normals[0] + w1 * normals[1] + w2 * normals[2]) / area
          diffuse = self.light.DiffuseFactor(inter_normal, np.array([inter_coord_x, inter_coord_y, inter_coord_z]))
          if (inter_coord_z > self.zbuffer[x][y]):
            self.zbuffer[x][y] = inter_coord_z
            color = (w0 * color_a * 255 + w1 * color_b * 255 + w2 * color_c * 255) * diffuse / area
            color = color.astype(np.uint)
            self.colorbuffer[y][x] = color
  def Draw(self):
    global view_mat
    while(True):
      self.Transform(RotateMatrix(math.radians(2), NormolizeVector([0, 1, 0])))
      self.VertexDraw()
      # self.canvas = self.colorbuffer.copy()
      cv2.imshow('render: ', self.colorbuffer)
      key = cv2.waitKey(20)
      if (key == ord('q')):
        print('exit')
        break
      elif (key == ord('a')):
        view_mat += left_shift_mat
      elif (key == ord('d')):
        view_mat += right_shift_mat
      elif (key == ord('s')):
        view_mat += down_shift_mat
      elif (key == ord('w')):
        view_mat += up_shift_mat        
      elif (key == ord('8')):
        view_mat += near_shift_mat
      elif (key == ord('2')):
        view_mat += far_shift_mat
      elif (key == ord(' ')):
        self.rotate = not self.rotate
      self.zbuffer = np.full((self.height, self.width), -9999.9, dtype=np.float)
      self.colorbuffer = np.zeros((self.height, self.width, 3), np.uint8)