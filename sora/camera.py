import numpy as np
import matrix

class Camera:
  def __init__(self):
    self.position = np.array([0.0, 0.0,  3.0])
    self.up_vector = np.array([0.0, 1.0, 0.0])
    self.view_matrix = np.identity(4)
    self.projection_matrix = np.identity(4)
    self.vertical_fov = 70.0
    self.aspect_ratio = 1.0
    self.near_z = 0.1
    self.far_z = 100.0
    self.forward_vector = np.array([0.0, 0.0, -1.0])
    self.right_vector = np.array([1.0, 0.0, 0.0])
    self.up_vector = np.array([0.0, 1.0, 0.0])
    self.move_speed = 2.0

  def update_projection_matrix(self, aspect_ratio):
    """
    Update the internal projection matrix.

    :param float aspect_ratio: The new aspect ratio of the display.
    """
    self.aspect_ratio = aspect_ratio
    self.projection_matrix = matrix.create_projection_matrix(self.vertical_fov, self.aspect_ratio, self.near_z, self.far_z)

  def update(self, key_pressed=None):
    if (key_pressed == ord('w')):
      self.postion += self.forward_vector * self.move_speed
    elif (key_pressed == ord('s')):
      self.postion -= self.forward_vector * self.move_speed
    elif (key_pressed == ord('a')):
      self.position += self.right_vector * self.move_speed
    elif (key_pressed == ord('d')):
      self.position -= self.right_vector * self.move_speed
    elif (key_pressed == ord('e')):
      self.position += self.up_vector * self.move_speed
    elif (key_pressed == ord('q')):
      self.position -= self.up_vector * self.move_speed

    rotation_matrix_x = np.identity(4)
    rotation_matrix_y = np.identity(4)
    translation_matrix = matrix.create_translation_matrix(-self.position[0], -self.position[1], -self.position[2])
    self.view_matrix = rotation_matrix_x.dot(rotation_matrix_y).dot(translation_matrix)

  

  

