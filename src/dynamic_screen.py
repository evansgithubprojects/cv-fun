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
    self.width = width
    self.height = height
    self.scalar = (width / og_width, height / og_height)

  def get_pixel_coordinates(self, normalized_position: tuple[float, float]):
    normalized_x, normalized_y = normalized_position
    return (round(normalized_x * self.width), round(normalized_y * self.height))

  def get_static_distance(self, normalized_start : tuple[float, float], normalized_end : tuple[float, float]):
    adjusted_start = (normalized_start[0] * self.scalar[0], normalized_start[1] * self.scalar[1])
    adjusted_end = (normalized_end[0] * self.scalar[0], normalized_end[1] * self.scalar[1])
    return math.sqrt((adjusted_end[0] - adjusted_start[0]) ** 2 + (adjusted_end[1] - adjusted_start[1]) ** 2)