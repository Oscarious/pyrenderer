import cv2

def DrawPoint(framebuffer, x, y, color):
  framebuffer.pixel_data[y][x] = color.GetVector3()

def DrawLine(framebuffer, x0, y0, x1, y1, color):
  cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x1), int(y1)), color.GetVector3().tolist(), 1)


def RenderTriangle(framebuffer, projection_matrix, v0, v1, v2, color):
  width = framebuffer.width
  height= framebuffer.height
  
  v0 = v0.dot(projection_matrix)
  v1 = v1.dot(projection_matrix)
  v2 = v2.dot(projection_matrix)

  v0 /= v0[3]
  v1 /= v1[3]
  v2 /= v2[3]
  
  x0 = (v0[0] + 1) * width / 2
  x1 = (v1[0] + 1) * width / 2
  x2 = (v2[0] + 1) * width / 2

  y0 = (1 - v0[1]) * height / 2
  y1 = (1 - v1[1]) * height / 2
  y2 = (1 - v2[1]) * height / 2
  
  DrawTriangle(framebuffer, x0, y0, x1, y1, x2, y2, color)


def DrawTriangle(framebuffer, x0, y0, x1, y1, x2, y2, color):
  cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x1), int(y1)), color.GetVector3().tolist(), 1)
  cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x2), int(y2)), color.GetVector3().tolist(), 1)
  cv2.line(framebuffer.pixel_data, (int(x1), int(y1)), (int(x2), int(y2)), color.GetVector3().tolist(), 1)
  
