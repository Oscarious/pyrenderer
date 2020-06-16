import numpy as np

class FrameBuffer:
  def __init__(self):
    self.width = 256
    self.height = 256
    self.pixel_data = np.zeros((self.height, self.width, 3), np.uint8)
    self.depth_clear_value = np.finfo(np.float32).max
  def resize(self, width, height):
    self.width = width
    self.height = height
    self.half_width = ((self.width - 1.0) / 2.0)
    self.half_height = ((self.height - 1.0) / 2.0)

    self.pixel_data = np.empty(self.width * self.height, np.uint32)
    self.depth_data = np.empty(self.width * self.height, np.float32)

    self.clear()

  def clear(self):
    self.pixel_data.fill(0)