from .coordinates import Coordinates
from random import randint

class Drawable(object):
   """
   The base class for all drawable objects.
   """
   
   def __init__(self, icon, x, y):
      self.icon = icon
      self.position = Coordinates(x, y)
   
   def draw(self, board):
      board[self.position.y][self.position.x] = self.icon

class UpStairs(Drawable):
   def __init__(self, x, y):
      self.direction = "^"
      super().__init__("^", x, y)

class DownStairs(Drawable):
   def __init__(self, x, y):
      self.direction = "v"
      super().__init__("v", x, y)
   
class Pitfall(Drawable):
   def __init__(self, x, y):
      self.pitfall = "O"
      self.amount = randint(1,10)
      super().__init__("O", x, y)

class Spike(Drawable):
   def __init__(self, x, y):
      self.pitfall = "X"
      self.amount = 5
      super().__init__("X", x, y) 

class Wall(Drawable):
   """
   Wall object for collision only.
   """
   def __init__(self, x, y):
      super().__init__("#", x, y)

class Void(Drawable):
   """
   Void object for collision/void only.
   """
   def __init__(self, x, y):
      super().__init__(" ", x, y)
         
class Shield(Drawable):
   """A shield the hero equips upon pick-up, protecting them from the next few
   hits, determined by its sturdiness
   """

   #determines how sturdy the shield is that you picked up. If its strength is 1,
   #it will break after 1 use (ie hitting a monster) and so on
   MIN = 1
   MAX = 5
   
   def __init__(self, x, y):
      self.used = False
      self.amount = randint(Shield.MIN, Shield.MAX)
      super().__init__("S", x, y)
   
class UndeadRepellent(Drawable):
      """No undead creature can stand the power of this splash potion. Throw it onto the ground
      to hurt all zombies in a 3x3 area."""

      def __init__(self, x, y):

         
         self.used = False
         super().__init__("R", x, y)
         


class HealthPack(Drawable):
   """
   Health Packs that the hero can pick up.
   """
   
   MIN = 5
   MAX = 10
   
   def __init__(self, x, y):
      self.amount = randint(HealthPack.MIN, HealthPack.MAX)
      self.used = False
      super().__init__("H", x, y)

class Alive(Drawable):
   """
   Alive base class for anything that moves and can die.
   Slightly ironic name since zombies inherit from it....
   """
   def __init__(self, icon, hp, ap, x, y):
      self.hp = hp
      self.ap = ap
      super().__init__(icon, x, y)
      
      self.targetPosition = self.position
      
   def isDead(self):
      return self.hp <= 0

   def increaseHP(self, amount):
      self.hp += amount
   
   def decreaseHP(self, amount):
      self.hp -= amount
   
   def attack(self):
      return self.ap

class Zombie(Alive):
   """
   Basic zombie, not very smart
   Will randomly stumble around the room
   """
   
   HP = 4
   AP = 1
   STUMBLE = 2
   
   def __init__(self, x, y):
      super().__init__("Z", Zombie.HP, Zombie.AP, x, y)
   
   def update(self):
      
      self.targetPosition = Coordinates(*self.position)
      
      # randomly move
      choice = randint(0,4 + Zombie.STUMBLE)
      
      if choice == 0:
         # move up
         self.targetPosition.y -= 1
      elif choice == 1:
         # move down
         self.targetPosition.y += 1
      elif choice == 2:
         # move left
         self.targetPosition.x -= 1
      elif choice == 3:
         # move right
         self.targetPosition.x += 1
      else:
         # don't move otherwise
         self.targetPosition = None      

class Mega(Zombie):
   """
   Mega Zombie class that will sometimes head for the hero.
   Other times it behaves like a normal zombie.
   """
   
   HP = 8
   AP = 2
   INTELLIGENCE = 90 # out of 100
   
   def __init__(self, x, y):
      super().__init__(x, y)
      self.icon = "M"
      self.hp = Mega.HP
      self.ap = Mega.AP
   
   # Based on the intelligence value, will move towards the hero
   def update(self, hero):      
      
      choice = randint(1, 100)
      
      # If we are smart
      if choice < Mega.INTELLIGENCE:
         
         self.targetPosition = Coordinates(*self.position)
         
         # Find where the hero is and move one step closer
         # Priority is given to the x axis
         if hero.position.x < self.targetPosition.x:
            self.targetPosition.x -= 1
         elif hero.position.x > self.targetPosition.x:
            self.targetPosition.x += 1
         elif hero.position.y < self.targetPosition.y:
            self.targetPosition.y -= 1
         else:
            self.targetPosition.y += 1
         
      # If we are not smart 
      else:
         super().update()

class BabyZombie(Zombie):
     
   #moves faster but less damage
   HP = 2
   AP = 1
   #if the baby zombie is upset, it will cry and harm the hero more
   cryState = 2
   cryChance = randint(1, 4)
      
   def __init__(self, x, y):
      super().__init__(x, y)
      self.icon = "z"
      self.hp = BabyZombie.HP
      self.ap = BabyZombie.AP
      
   def update(self):
      #determines if the baby will cry

      if Zombie.cryChance > Zombie.cryState:
         self.counter = 5
         while self.counter > 0:
            AP = 5
            self.counter -=1
      
      self.targetPosition = Coordinates(*self.position)
      choice = randint(0,4)
      
      if choice == 0:
         # move up
         self.targetPosition.y -= 1
         self.targetPosition.y -= 1
      elif choice == 1:
         # move down
         self.targetPosition.y += 1
         self.targetPosition.y += 1
      elif choice == 2:
         # move left
         self.targetPosition.x -= 1
         self.targetPosition.x -= 1
      elif choice == 3:
         # move right
         self.targetPosition.x += 1
         self.targetPosition.x += 1
      else:
         # don't move otherwise
         self.targetPosition = None



class Boss(Alive):

   HP = 30
   AP = 8

##   ARROWCHANCE = 3
##   MELEECHANCE = 3
   MOVETURN = 0
   
##   ISCHARGING = False
   
   def __init__(self, x, y):
      super().__init__("B", Boss.HP, Boss.AP, x, y)

   
   def update(self, hero):
      self.targetPosition = Coordinates(*self.position)

##      #charge forward
##      while charging:
##         if hero.position.x < self.targetPosition.x -= 1:
##            self.targetPosition.x -= 1
##            Boss.ISCHARGING = True
##            self.targetPosition.x -= 1
##            Boss.ISCHARGING = True
##            AP = 8
##         elif hero.position.x > self.targetPosition.x += 1:
##            self.targetPosition.x += 1
##            Boss.ISCHARGING = True
##            self.targetPosition.x += 1
##            Boss.ISCHARGING = True
##            AP = 8
##         elif hero.position.y < self.targetPosition.y += 1:
##            self.targetPosition.y -= 1
##            Boss.ISCHARGING = True
##            self.targetPosition.y -= 1
##            Boss.ISCHARGING = True
##            AP = 8
##         elif hero.position.y > self.targetPosition.y += 1:
##            self.targetPosition.y += 1
##            Boss.ISCHARGING = True
##            self.targetPosition.y += 1
##            Boss.ISCHARGING = True
##            AP = 8
##      Boss.ISCHARGING = False
            
         

##      if Boss.ARROWCHANCE <= randint(1,11):
##         self.icon = arrow
##         arrow = "-"
##      
##         self.arrowPosition = Coordinates(*self.position)
##      
##      
##         if hero.position.x < self.arrowPosition.x:
##            self.arrowPosition.x -= 1
##            self.arrowPosition.x -= 1
##         elif hero.position.x > self.arrowPosition.x:
##            self.arrowPosition.x += 1
##            self.arrowPosition.x += 1
##         elif hero.position.y < self.arrowPosition.y:
##            self.arrowPosition.y -= 1
##            self.arrowPosition.y -= 1
##         elif hero.position.y > self.arrowPosition.y:
##            self.arrowPosition.y += 1
##            self.arrowPosition.y += 1
##         
##      else:
##         null
         
      #to move every other turn
      if Boss.MOVETURN % 2 == 0:
         if hero.position.x < self.targetPosition.x:
            self.targetPosition.x -= 1
         elif hero.position.x > self.targetPosition.x:
            self.targetPosition.x += 1
         elif hero.position.y < self.targetPosition.y:
            self.targetPosition.y -= 1
         else:
            self.targetPosition.y += 1
         Boss.MOVETURN += 1
         
      else:
         self.targetPosition = None
         Boss.MOVETURN += 1
                   
   

class Hero(Alive):
   """
   The hero class.
   Makes moves based on a command from the keyboard.
   """
   
   HP = 100
   AP = 2
   
   def __init__(self, x, y):
      super().__init__("@", Hero.HP, Hero.AP, x, y)
      self.targetPosition = None
   
   def update(self, command):
      # Do something based on the command character
      
      self.targetPosition = Coordinates(*self.position)
      
      if command == "w":
         # Move up
         self.targetPosition.y -= 1 
      elif command == "s":
         # Move down
         self.targetPosition.y += 1
      elif command == "a":
         # Move left
         self.targetPosition.x -= 1
      elif command == "d":
         # Move right
         self.targetPosition.x += 1
      else:
         self.targetPosition = None
