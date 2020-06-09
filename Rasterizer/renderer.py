import numpy as np
import cv2
import math
from RenderUtils import *
from multiprocessing.dummy import Pool
from functools import partial
from ControlUtils import *
import os

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
    self.colorbuffer = np.zeros((self.height, self.width, 3), np.uint8)
    self.zbuffer = np.full((self.height, self.width), -9999)
  def MapCoords(self, x, y):
    maped_x = self.width / 2 * x + self.width / 2
    maped_y = -self.height / 2 * y + self.height / 2
    return maped_x, maped_y
  def Transform(self, trans_mat=np.identity(4)):
    if (self.rotate):
      self.vertices = trans_mat.dot(self.vertices.T).T
  def VertexDraw(self):
    coords_z = [] 
    for j in range(len(self.indices)):
      triangle_indices = self.indices[j]
      assert(len(triangle_indices) == 3)
      projected_vertices = view_mat.dot(self.vertices.T).T
      for i in range(len(triangle_indices)):
        coords_z.append(projected_vertices[triangle_indices[i]][2])
      projected_vertices = self.perspective_matrix.dot(projected_vertices.T).T
      attr_vertices = []
      for i in range(len(triangle_indices)):
        x1, y1 = self.MapCoords(projected_vertices[triangle_indices[i]][0] / projected_vertices[triangle_indices[i]][3], projected_vertices[triangle_indices[i]][1] / projected_vertices[triangle_indices[i]][3])
        x2, y2 = self.MapCoords(projected_vertices[triangle_indices[(i+4)%3]][0] / projected_vertices[triangle_indices[(i+4)%3]][3], projected_vertices[triangle_indices[(i+4)%3]][1] / projected_vertices[triangle_indices[(i+4)%3]][3])
        #triangle_vertices.extend(projected_vertices[triangle_indices[i]])
        cv2.line(self.canvas, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 1)
        attr_vertices.extend((x1, y1))
        offset = i + j*len(triangle_indices)
        if (len(self.colors) > offset):
          attr_vertices.extend(self.colors[offset])
        else:
          attr_vertices.extend([0, 0, 0])
      self.FragmentDraw(attr_vertices, coords_z)  
  def FragmentDraw(self, vertices, coords_z):
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
    
    # pool = Pool(os.cpu_count())
    ys = [y for y in range(int(minY), int(maxY))]
    for x in range(int(minX), int(maxX)):
      #task = partial(task_def, x, (coord_a, color_a), (coord_b, color_b), (coord_c, color_c), area)
      #colors = pool.map(task, ys)
      for y in range(int(minY), int(maxY)):
        w0 = EdgeFunction(coord_a, coord_b, [x, y])
        w1 = EdgeFunction(coord_c, coord_a, [x, y])
        w2 = EdgeFunction(coord_b, coord_c, [x, y])
        if (w0 >= 0 and w1 >= 0 and w2 >= 0):
          coord_z = 1 / (w0 / coords_z[0] + w1 / coords_z[1] + w2 / coords_z[2])
          if (coord_z > self.zbuffer[x][y]):
            self.zbuffer[x][y] = coord_z
            w0 /= area
            w1 /= area
            w2 /= area
            color = w0 * color_a * 255 + w1 * color_b * 255 + w2 * color_c * 255
            color = [int(color[0][0]), int(color[0][1]), int(color[0][2])]
            self.colorbuffer[y][x] = color
        # cv2.circle(self.canvas, (x, y), 1, self.colorbuffer[x][y].tolist(), 0)
        # print(x, y, self.colorbuffer[x][y].tolist())
      # for i in range(len(ys)):
      #   cv2.circle(self.canvas, (x, ys[i]), 1, colors[i], 0)
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
      self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
      self.zbuffer = np.full((self.height, self.width), -9999.9, dtype=np.float)
      self.colorbuffer = np.zeros((self.height, self.width, 3), np.uint8)