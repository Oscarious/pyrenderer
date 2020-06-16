from pyrenderer import PyRenderer
from primitive import Primitive
from camera import Camera

if __name__ == '__main__':
  prim = Primitive()
  renderer = PyRenderer()
  camera = Camera()
  prim.LoadModel('sora/cube.json')
  renderer.Render(prim, camera)