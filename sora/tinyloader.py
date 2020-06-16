import json
import os
class TinyLoader:
  def load(self, filename):
    print(filename)
    with open(filename, 'r') as f:
      data = json.load(f)
    return data


if __name__ == '__main__':
  loader = TinyLoader()
  loader.load('sora/cube.json')

