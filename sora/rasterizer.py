import cv2
from shader import *
from color import Color

COUNTER_CLOCKWISE = 1
CLOCKWISE = -1
class Rasterizer:
  def __init__(self):
    self.winding = CLOCKWISE 
  def DrawPoint(self, framebuffer, x, y, color):
    framebuffer.pixel_data[y][x] = color.GetVector3()

  def DrawLine(self, framebuffer, x0, y0, x1, y1, color):
    cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x1), int(y1)), color.GetVector3().tolist(), 1)

  def EdgeFunction(self, vec2_a, vec2_b, vec2_c):
    ret = (vec2_c[0] - vec2_a[0]) * (vec2_b[1] - vec2_a[1]) - (vec2_c[1] - vec2_a[1]) * (vec2_b[0] - vec2_a[0])
    return ret * self.winding

  def InterpolateAttributes(self, u, v, texture):
    width = texture.Width()
    height = texture.Height()
    x = u * (width - 1)
    y = v * (height - 1)
    return texture.At(int(x), int(y))


  def RenderTriangle(self, framebuffer, projection_matrix, v0, v1, v2, color):
    width = framebuffer.width
    height= framebuffer.height

    # v0 = projection_matrix.T.dot(v0.T).T
    # v1 = projection_matrix.T.dot(v1.T).T
    # v2 = projection_matrix.T.dot(v2.T).T

    #clip space
    v0Clip = v0.dot(projection_matrix.T)
    v1Clip = v1.dot(projection_matrix.T)
    v2Clip = v2.dot(projection_matrix.T)

    one_over_w0 = 1.0 / v0Clip[3]
    one_over_w1 = 1.0 / v1Clip[3]
    one_over_w2 = 1.0 / v2Clip[3]

    #NDC space
    v0NDC = v0Clip * one_over_w0
    v1NDC = v1Clip * one_over_w1
    v2NDC = v2Clip * one_over_w2
    
    #frame space linear interpolate
    x0 = (v0NDC[0] + 1) * width / 2
    x1 = (v1NDC[0] + 1) * width / 2
    x2 = (v2NDC[0] + 1) * width / 2

    y0 = (1 - v0NDC[1]) * height / 2
    y1 = (1 - v1NDC[1]) * height / 2
    y2 = (1 - v2NDC[1]) * height / 2
    
    self.DrawTriangle(framebuffer, x0, y0, x1, y1, x2, y2, color)


  def DrawTriangle(self, framebuffer, x0, y0, x1, y1, x2, y2, color):
    cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x1), int(y1)), color.GetVector3i().tolist(), 1)
    cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x2), int(y2)), color.GetVector3i().tolist(), 1)
    cv2.line(framebuffer.pixel_data, (int(x1), int(y1)), (int(x2), int(y2)), color.GetVector3i().tolist(), 1)
    # cv2.circle(framebuffer.pixel_data, (int(x0), int(y0)), 30, ())
  
  def Draw(self, framebuffer, projection_matrix, v0, v1, v2, attributes0, attributes1, attributes2, texture):
    width = framebuffer.width
    height= framebuffer.height

    #clip space
    v0Clip = v0.dot(projection_matrix.T)
    v1Clip = v1.dot(projection_matrix.T)
    v2Clip = v2.dot(projection_matrix.T)

    one_over_w0 = 1.0 / v0Clip[3]
    one_over_w1 = 1.0 / v1Clip[3]
    one_over_w2 = 1.0 / v2Clip[3]

    #NDC space
    v0NDC = v0Clip * one_over_w0
    v1NDC = v1Clip * one_over_w1
    v2NDC = v2Clip * one_over_w2
    
    #frame space linear interpolate
    v0Raster = ((v0NDC[0] + 1) * width / 2, (1 - v0NDC[1]) * height / 2)
    v1Raster = ((v1NDC[0] + 1) * width / 2, (1 - v1NDC[1]) * height / 2)
    v2Raster = ((v2NDC[0] + 1) * width / 2, (1 - v2NDC[1]) * height / 2)
    # self.DrawTriangle(framebuffer, v0Raster[0], v0Raster[1], v1Raster[0], v1Raster[1], v2Raster[0], v2Raster[1], Color(0.31, 0.3, 0.56))
    # return
    
    minx = int(min(min(v0Raster[0], v1Raster[0]), v2Raster[0]))
    miny = int(min(min(v0Raster[1], v1Raster[1]), v2Raster[1]))
    maxx = int(max(max(v0Raster[0], v1Raster[0]), v2Raster[0]))
    maxy = int(max(max(v0Raster[1], v1Raster[1]), v2Raster[1]))
    
    triangle_coverage = self.EdgeFunction(v0Raster, v1Raster, v2Raster)
    
    for y in range(miny, maxy+1):
      for x in range(minx, maxx+1):
        sample = (x, y)
        e0 = self.EdgeFunction(v1Raster, v2Raster, sample)
        e1 = self.EdgeFunction(v2Raster, v0Raster, sample)
        e3 = self.EdgeFunction(v0Raster, v1Raster, sample)

        #shared edge not computed! solution: only include left bottom edge
        included = e0 >= 0 and e1 >= 0 and e3 >= 0

        if (included):
          e0 /= triangle_coverage
          e1 /= triangle_coverage
          e2 = 1.0 - e0 - e1
        
          one_over_z = e0 * 1.0 / v0NDC[2] + e1 * 1.0 / v1NDC[2] + e2 * 1.0 / v2NDC[2]
          
          if (one_over_z < framebuffer.depth_data[y][x]):
            framebuffer.depth_data[y][x] = one_over_z
          
          # f0 = e0 * one_over_w0
          # f1 = e1 * one_over_w1
          # f2 = e2 * one_over_w2

          uv = e0 * attributes0 + e1 * attributes1 + e2 * attributes2
          # v = f1 / (f0+f1+f2)
          # v = f1 / (f0+f1+f2)
          texture_attributes = self.InterpolateAttributes(uv[0], uv[1], texture)
          # framebuffer.pixel_data[y][x] = Color(0.31, 0.3, 0.56).GetVector3i()
          framebuffer.pixel_data[y][x] = texture_attributes