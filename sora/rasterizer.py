import cv2
from shader import *
from color import Color

COUNTER_CLOCKWISE = 1
CLOCKWISE = -1
class Rasterizer:
  def __init__(self):
    self.winding = COUNTER_CLOCKWISE 
  def DrawPoint(self, framebuffer, x, y, color):
    framebuffer.pixel_data[y][x] = color.GetVector3()

  def DrawLine(self, framebuffer, x0, y0, x1, y1, color):
    cv2.line(framebuffer.pixel_data, (int(x0), int(y0)), (int(x1), int(y1)), color.GetVector3().tolist(), 1)

  def EdgeFunction(self, vec2_a, vec2_b, vec2_c):
    ret = (vec2_c[0] - vec2_a[0]) * (vec2_b[1] - vec2_a[1]) - (vec2_c[1] - vec2_a[1]) * (vec2_b[0] - vec2_a[0])
    return ret * self.winding

  def InterpolateAttributes(self, w0, w1, attr0, attr1, attr2):
    attr = w0 * attr0 + w1 * attr1 + (1.0 - w0 - w1) * attr2
    return attr

  def LinearInterpolateTexture(self, attribute_coordinate, texture):
    width = texture.Width()
    height = texture.Height()
    x = attribute_coordinate[0] * (width - 1)
    y = attribute_coordinate[1] * (height - 1)
    return texture.At(int(x), int(y)) 

  def RenderTriangle(self, framebuffer, projection_matrix, v0, v1, v2, color):
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
  
  def Draw(self, framebuffer, scene, camera):
    width = framebuffer.width
    height= framebuffer.height
    primitive = scene.primitive

    VBO = primitive.vertex_buffer
    IBO = primitive.index_buffer
    TBO = primitive.texture_buffer
    NBO = primitive.normal_buffer
    texture = primitive.texture

    #switch to view space 
    for index in IBO:
      #vertex coordinates
      v0, v1, v2 = VBO[index[0][0]-1], VBO[index[1][0]-1], VBO[index[2][0]-1] 
      #texture coorinates
      t0, t1, t2 = TBO[index[0][1]-1], TBO[index[1][1]-1], TBO[index[2][1]-1]
      #normal vector
      n0, n1, n2 = NBO[index[0][2]-1], NBO[index[1][2]-1], NBO[index[2][2]-1]

      v0 = v0.dot(camera.view_matrix.T)
      v1 = v1.dot(camera.view_matrix.T)
      v2 = v2.dot(camera.view_matrix.T)

      #clip space
      v0Clip = v0.dot(camera.projection_matrix.T)
      v1Clip = v1.dot(camera.projection_matrix.T)
      v2Clip = v2.dot(camera.projection_matrix.T)

      #one_over_w = 1 / z 
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
          
            one_over_z = e0 * v0NDC[2] + e1 * v1NDC[2] + e2 * v2NDC[2]
            if (one_over_z < framebuffer.depth_data[y][x]):
              framebuffer.depth_data[y][x] = one_over_z
            
              #  Calculate barycentric coordinates for perspectively-correct interpolation
              f0 = e0 * one_over_w0
              f1 = e1 * one_over_w1
              f2 = e2 * one_over_w2
              
              u = f0 / (f0+f1+f2)
              v = f1 / (f0+f1+f2)

              # incorrect interpolation
              # uv = e0 * t0 + e1 * t1 + e2 * t2
              
              texture_attributes_coordinates = self.InterpolateAttributes(u, v, t0, t1, t2)
              normal_attributes_vector = self.InterpolateAttributes(u, v, n0, n1, n2)
              texture_value = self.LinearInterpolateTexture(texture_attributes_coordinates, primitive.texture)
              texture_color = Color().FromVector3i(texture_value)


              # deal with lightling
              combined_light_color = Color()
              # ambient light
              if (len(scene.ambient_lights)):
                ambient_light = scene.ambient_lights[0]
                ambient_color = ambient_light.color.MultiplyNumber(ambient_light.intensity)
                combined_light_color = combined_light_color.Accumulate(ambient_color)

              # directional light
              for light in scene.directional_lights:
                diffuse_factor = light.diffuse(v0[:3], normal_attributes_vector[:3])
                light_color = light.color.MultiplyNumber(diffuse_factor)
                combined_light_color = combined_light_color.Accumulate(light_color)
              
              final_color = combined_light_color.Multiply(texture_color)
              final_color.Clip(0.0, 1.0)
              framebuffer.pixel_data[y][x] = final_color.GetVector3i()