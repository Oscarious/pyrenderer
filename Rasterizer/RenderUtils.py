import numpy as np
import cv2
import math


def RotateMatrix(theta, vec):
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

def NormolizeVector(vec):
  de = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
  return np.array([[vec[0]/de, vec[1]/de, vec[2]/de]]).T

def PerspectiveMatrix(FOV, aspect, zNear, zFar):
  return np.array([[1.0 / (math.tan(FOV/2) * aspect), 0.0, 0.0, 0.0],
                   [0.0, 1.0 / math.tan(FOV/2), 0.0, 0.0],
                   [0.0, 0.0, (zNear + zFar) / (zNear - zFar), -1.0],
                   [0.0, 0.0, 2.0 * zFar * zNear / (zNear - zFar), 0.0]], np.float).T#why transpose projection matrix?

def GetTriangleBorder(vertices, step=2):
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

view_mat = np.array([[1.0, 0.0,  0.0,  0.0],
                   [0.0, 1.0,  0.0,  0.0],
                   [0.0, 0.0,  1.0, -3.0],
                   [0.0, 0.0,  0.0,  1.0]], np.float)

