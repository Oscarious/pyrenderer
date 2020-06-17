import numpy as np

class FrameBuffer:
  def __init__(self):
    self.width = 256
    self.height = 256
    self.pixel_data = np.zeros((self.height, self.width, 3), np.uint8)
    self.depth_clear_value = np.finfo(np.float32).max
    self.depth_data = np.full((self.height, self.width), self.depth_clear_value, dtype=np.float32)
  def Resize(self, width, height):
    self.width = width
    self.height = height
    self.half_width = ((self.width - 1.0) / 2.0)
    self.half_height = ((self.height - 1.0) / 2.0)

    self.pixel_data = np.zeros((self.height, self.width, 3), np.uint8)
    self.depth_data = np.full((self.height, self.width), self.depth_clear_value, dtype=np.float32)

    self.Clear()

  def Clear(self):
    self.pixel_data.fill(0)
    self.depth_data.fill(self.depth_clear_value)