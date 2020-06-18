import numpy as np


def get_vector_length(vec):
  return np.linalg.norm(vec)

def get_normalized_vector(vec):
  return vec / get_vector_length(vec)
