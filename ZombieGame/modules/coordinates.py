
# Quick coordinate class to contain both x and y
# Overrides == for easy comparison
class Coordinates(object):
   def __init__(self, x, y):
      self.x = x
      self.y = y
      
   def __eq__(self, other):
      return self.x == other.x and self.y == other.y
   
   def __sub__(self, other):
      if type(other) == int:
         return Coordinates(self.x - other, self.y - other)
      if type(other) == Coordinates:
         return Coordinates(self.x - other.x, self.y - other.y)
      if type(other) == tuple:
         return Coordinates(self.x - other[0], self.y - other[1])
   
   def __add__(self, other):
      if type(other) == int:
         return Coordinates(self.x + other, self.y + other)
      if type(other) == Coordinates:
         return Coordinates(self.x + other.x, self.y + other.y)
      if type(other) == tuple:
         return Coordinates(self.x + other[0], self.y + other[1])
   
   
   def __len__(self):
      return 2
   
   def __iter__(self):
      self.current = 0
      return self

   def __next__(self):
      if self.current >= len(self):
         raise StopIteration
      else:
         self.current += 1
         if self.current == 1:
            return self.x
         else:
            return self.y



if __name__ == '__main__':
   
   c = Coordinates(5,6)
   
   print(*c)
   
   
   