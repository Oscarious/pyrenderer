import numpy as np
import cv2
import math
from renderer import MyRenderer
from multiprocessing.dummy import Pool
from data import *
import os

if __name__ == '__main__':
  renderer = MyRenderer()
  #row_diff = pyramid_vertices.shape[0] - pyramid_colors.shape[0]
  #pyramid_colors = np.r_[pyramid_colors, np.zeros((row_diff, 3), np.int)]
  #pyramid_vertices = np.c_[pyramid_vertices, pyramid_colors]
  print(os.getcwd())
  os.chdir('Rasterizer/res')
  texture = cv2.imread('wall.jpg')
  triangle_vertices = np.c_[triangle_vertices, triangle_colors]
  renderer.SetTextureCoord(triangle_texture_coord)
  renderer.SetTexture(texture)
  renderer.SetVertices(triangle_vertices)
  renderer.SetIndices(triangle_indices)
  renderer.SetCanvasSize(256, 256)
  renderer.SetLight(Light())
  renderer.SetNormals(triangle_normals)
  renderer.Draw()
    