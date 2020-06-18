from pyrenderer import PyRenderer
from primitive import Primitive
from camera import Camera
from scene import Scene
from tinyloader import TinyLoader

if __name__ == '__main__':
  renderer = PyRenderer()
  camera = Camera()
  scene = Scene()
  loader = TinyLoader()
  model_data = loader.load('sora/cube.json')
  prim = Primitive(model_data)
  prim.LoadTexture('sora/cube.png')
  scene.AddPrimitive(prim)
  scene.AddAmbientLights(loader.ambient_lights)
  scene.AddDirectionalLights(loader.directional_lights)
  renderer.Render(scene, camera)