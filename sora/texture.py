import numpy as np
import cv2

class Texture:
  def __init__(self, image_name):
    self.image = cv2.imread(image_name)
  def Width(self):
    return self.image.shape[1]
  def Height(self):
    return self.image.shape[0]
  def At(self, x, y):
    return self.image[y][x]
