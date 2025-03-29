import math

og_width = 500
og_height = 500

class DynamicScreen():
  instance = None
  
  def __new__(cls, *args, **kwargs):
    if cls.instance is None:
        cls.instance = super().__new__(cls)
    return cls.instance
  
  def adjust(self, frame):
    width, height, _ = frame.shape
    self.scalar = (width / og_width, height / og_height)

  def get_static_distance(self, normalized_start : tuple[int, int], normalized_end : tuple[int, int]):
    adjusted_start = (normalized_start[0] * self.scalar[0], normalized_start[1] * self.scalar[1])
    adjusted_end = (normalized_end[0] * self.scalar[0], normalized_end[1] * self.scalar[1])
    return math.sqrt((adjusted_end[0] - adjusted_start[0]) ** 2 + (adjusted_end[1] - adjusted_start[1]) ** 2)