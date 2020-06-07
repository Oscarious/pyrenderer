import numpy as np
import cv2
import math
from renderer import MyRenderer

class Renderer:
  def __init__(self):
    self.near = 0.1
    self.far = 100
    self.color_attr = ([
      [1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]
    ])
  def SetVertex(self, vertices):
    self.vertices = vertices
  def SetIndex(self, indexes):
    self.indexes = indexes
  def SetScreen(self, width, height):
    self.width = width
    self.height = height
  def MapCoords(self, x, y):
    maped_x = self.width / 2 * x + self.width / 2
    maped_y = -self.height / 2 * y + self.height / 2
    return maped_x, maped_y
  def SetTransMat(self, mat):
    self.transMat = mat
  def ScanlineColoring(self, img):
    def takeSecond(elem):
      return elem[1]
    for index in self.indexes:
      li = []
      for i in range(3):
        li.append(self.MapCoords(self.vertices[index[i]][0] / self.vertices[index[i]][3], self.vertices[index[i]][1] / self.vertices[index[i]][3]))
      li.sort(key=takeSecond)
      x0 = li[0][0]
      y0 = li[0][1]
      x1 = li[1][0]
      y1 = li[1][1]
      x2 = li[2][0]
      y2 = li[2][1]
      #y go up
      for y3 in range(int(y1), int(y2)):
        xl = (y3 - y2) * (x0 - x2) / (y0 - y2) + x2
        xr = (y3 - y2) * (x1 - x2) / (y1 - y2) + x2
        cv2.line(img, (int(xl), int(y3)), (int(xr), int(y3)), (10, 100, 210), 1)
      for y3 in range(int(y0), int(y1)):
        xl = (y3 - y2) * (x0 - x2) / (y0 - y2) + x2
        xr = (y3 - y1) * (x1 - x0) / (y1 - y0) + x1
        cv2.line(img, (int(xl), int(y3)), (int(xr), int(y3)), (10, 100, 210), 1)
      #cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (10, 100, 210), 5)
  def coloring(self, img, vertices):
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
    minX, minY, maxX, maxY = GetBorder(vertices, 5)
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
          cv2.circle(img, (x, y), 1, color, 0)

        

  def draw(self):
    img = np.zeros((self.height, self.width, 3), np.uint8)
    v = []
    for index in self.indexes:
      for i in range(3):
        x1, y1 = self.MapCoords(self.vertices[index[i]][0] / self.vertices[index[i]][3], self.vertices[index[i]][1] / self.vertices[index[i]][3])
        v.extend((x1, y1))
        v.extend(self.color_attr[i%3])
        #x2, y2 = self.MapCoords(self.vertices[index[(i+4) % 3]][0] / self.vertices[index[(i+4) % 3]][3], self.vertices[index[(i+4) % 3]][1] / self.vertices[index[(i+4) % 3]][3])
        #cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (10, 100, 210), 1)
      self.coloring(img, v)
    cv2.imshow('render: ', img)
    cv2.waitKey(0)



def rotate_mat(theta, vec):
  cos = math.cos(theta)
  sin = math.sin(theta)
  u = vec[0]
  v = vec[1]
  w = vec[2]
  assert(abs(u**2 + v**2 + w**2 - 1) < 0.0001)
  mat = np.array([[u**2+(1-u**2)*cos, u*v*(1-cos)-w*sin, u*w*(1-cos)+v*sin, 0],
                  [u*v*(1-cos)+w*sin, v**2+(1-v**2)*cos, v*w*(1-cos)-u*sin, 0],
                  [u*w*(1-cos)-v*sin, v*w*(1-cos)+u*sin, w**2+(1-w**2)*cos, 0],
                  [0,                                 0,                 0, 1]], np.float)
  return mat

def normolize_vec(vec):
  de = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
  return np.array([[vec[0]/de, vec[1]/de, vec[2]/de]]).T

def perspective_mat(FOV, aspect, zNear, zFar):
  return np.array([[1.0 / (math.tan(FOV/2) * aspect), 0.0, 0.0, 0.0],
                   [0.0, 1.0 / math.tan(FOV/2), 0.0, 0.0],
                   [0.0, 0.0, (zNear + zFar) / (zNear - zFar), -1.0],
                   [0.0, 0.0, 2.0 * zFar * zNear / (zNear - zFar), 0.0]], np.float)

#left up most and right bottom most
def GetBorder(vertices, step=2):
  minX = 99999
  maxX = -minX
  minY = 99999
  maxY = -minY
  for i in range(0, len(vertices), step):
      minX = min(minX, vertices[i])
      maxX = max(maxX, vertices[i])
      minY = min(minY, vertices[i+1])
      maxY = max(maxY, vertices[i+1])
  return minX, minY, maxX, maxY

def EdgeFunction(veca, vecb, vecc):
  return (vecc[0] - veca[0]) * (vecb[1] - veca[1]) - (vecc[1] - veca[1]) * (vecb[0] - veca[0])

if __name__ == '__main__':
  renderer = MyRenderer()
  verts0 = np.array([
             [-0.5, -0.5, -0.5, 1],
             [-0.5,  0.5, -0.5, 1],
             [ 0.5,  0.5, -0.5, 1],
             [ 0.5, -0.5, -0.5, 1],
             [-0.5, -0.5,  0.5, 1],
             [-0.5,  0.5,  0.5, 1],
             [0.5,   0.5,  0.5, 1],
             [0.5,  -0.5,  0.5, 1]]).transpose()
  indices0 = [[0, 1, 2], [2, 3, 0], [0, 1, 5], [0, 4, 5], [4, 5, 6], [4, 6, 7], [2, 3, 6], [3, 6, 7]]

  verts1 = np.array([
    [-0.5, -0.5, -50.0, 1],
    [ 0.5, -0.5, -0.2, 1],
    [ 0.0,  0.8, 0, 1]
  ])
  indices1 = [[0, 1, 2]]
  colors1 = [
      [1, 0, 0],
      [0, 1, 0],
      [0, 0, 1]
    ]
  model = rotate_mat(math.radians(0), normolize_vec([1, 0, 0]))
  view = np.array([[1.0, 0.0,  0.0,  0.0],
                   [0.0, 1.0,  0.0,  0.0],
                   [0.0, 0.0,  1.0, -3.0],
                   [0.0, 0.0,  0.0,  1.0]], np.float)
  #verts = np.dot(view, np.dot(model, verts1.T))
  verts = np.dot(view, verts1.T)
  #verts = np.dot(proj.T, tmp)

  renderer.SetVertices(verts)
  renderer.SetIndices(indices1)
  renderer.SetColors(colors1)
  #renderer.SetScreen(800, 600)
  renderer.Draw()
    