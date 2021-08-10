from random import randint

class Timer(object):
   """
   Object that ticks down from a set value.
   The value is reset to a random amount between
   minValue and maxValue.
   """
   # Timers for zombies and item
   TIMER_ZOMBIE_MIN = 5
   TIMER_ZOMBIE_MAX = 10
   TIMER_ITEM_MIN = 10
   TIMER_ITEM_MAX = 15
   
   
   def __init__(self, minValue, maxValue):
      self.minValue = minValue
      self.maxValue = maxValue
      self.reset()
      
   
   def tick(self):
      self.counter -= 1
   
   def isDone(self):
      return self.counter <= 0

   def reset(self):
      self.counter = randint(self.minValue, self.maxValue)