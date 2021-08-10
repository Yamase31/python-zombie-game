from .gameObjects import *
from os import path

class Room(object):
   """
   Room object contains the walls and dimensions of the area.
   """
   
   # Maximum Numbers
   MAX_ITEMS = 5
   MAX_ENTITIES = 20
   MAX_BOSSES = 2
   
   # Chances for spawning types
   MEGAZ_CHANCE = 25    # out of 100
   BABY_CHANCE = 40
   
   # Room defaults   
   WIDTH_DEFAULT = 30
   HEIGHT_DEFAULT = 16
   HERO_START_DEFAULT = (15,8)
   
   def __init__(self, fileName=None):
      
      self.structures = []
      self.entities = []
      self.items = []
      self.board = []
      
      if fileName == None or not path.exists(fileName):      
         # Make a default room instead
         self.heroStart = Room.HERO_START_DEFAULT
         self.board = [["." for x in range(Room.WIDTH_DEFAULT)] for y in range(Room.HEIGHT_DEFAULT)]
         print(len(self.board), len(self.board[0]))
         
         # Create outer walls
         for x in range(Room.WIDTH_DEFAULT):
            self.structures.append(Wall(x, 0))
            self.structures.append(Wall(x, Room.HEIGHT_DEFAULT - 1))
            
         for y in range(Room.HEIGHT_DEFAULT):
            self.structures.append(Wall(0, y))
            self.structures.append(Wall(Room.WIDTH_DEFAULT - 1, y))

      else:
         file = open(fileName, "r")
         print(fileName)
         y = 0
         for line in file:
            self.heroStart = Room.HERO_START_DEFAULT
            x = 0
            for ch in line:
               if ch == "#":
                  self.structures.append(Wall(x,y))
               if ch == " ":
                  self.structures.append(Void(x,y))
               if ch == "v":
                  self.structures.append(DownStairs(x,y))
               if ch == "^":
                  self.structures.append(UpStairs(x,y))
               if ch == "O":
                  self.structures.append(Pitfall(x,y))
               if ch == "X":
                  self.structures.append(Spike(x,y))
                  
               if ch == "B":
                  self.entities.append(Boss(x,y))
               if ch == "M":
                  self.entities.append(Mega(x,y))
               if ch == "Z":
                  self.entities.append(Zombie(x,y))
               if ch == "z":
                  self.entities.append(BabyZombie(x,y))
               #other monsters here...
                  
               if ch == "H":
                  self.items.append(HealthPack(x,y))
               if ch == "S":
                  self.items.append(Shield(x,y))
               if ch == "R":
                  self.items.append(UndeadRepellent(x,y))
               #other items here...
               x +=1
            y+=1
         self.board = [["." for x in range(x)] for y in range(y)]
         print(len(self.board), len(self.board[0]))
                  
            

      
   # Clear the drawing board, draw everything
   def drawRoom(self):
      # Redraw the room
      for col in range(len(self.board)):
         for row in range(len(self.board[col])):
            if self.board[col][row] != " " and self.board[col][row] != "#":
               self.board[col][row] = "."
      
      # Let each entity and structure draw itself
      for sequence in [self.structures, self.entities, self.items]:         
         for s in sequence:
            #if fileName == None or not path.exists(fileName):
            s.draw(self.board)
            #else:
               #here, if it finds a file, put up that file's board
   
   def positionCheck(self, hero, position):
      """
      Searches through all active objects in the game to detect
      if position would collide with the object.
      """
      # Check to see if it is a valid location
##      if self.board[position.y][position.x] == " ":
##         return "void"
      
      # Search room objects, zombies, hps, and hero
      for sequence in [self.structures,
                       self.entities,
                       self.items,
                       [hero]]:
         for s in sequence:
            if s.position == position:
               return s
      
      return None
   
   def addEntity(self, hero, entity):
      """
      Adds a new active object to the world.
      Entity parameter is a string indicating the
      type of new entity to add.
      
      Will fail if the randomly selected position is
      already occupied.
      """
      
      positionY = randint(1, len(self.board) - 1)
      positionX = randint(1, len(self.board[positionY]) - 1)
      
      position = Coordinates(positionX, positionY)
      
      if self.positionCheck(hero, position) == None:
         if entity == "zombie":
            self.addZombie(position)
            
         elif entity == "item":
            self.addItem(position)
            
   def addZombie(self, position):
      """
      Will attempt to add a zombie if we haven't hit the max
      number. Randomly selects between a normal Zombie or
      Mega Zombie based on MEGAZ_CHANCE.
      
      This is invoked by addEntity.
      """
      if len(self.entities) < Room.MAX_ENTITIES:
         choice = randint(1, 100)
         if choice < Room.MEGAZ_CHANCE:
            self.entities.append(Mega(*position))
         if choice > Room.MEGAZ_CHANCE:
            self.entities.append(Zombie(*position))
         if choice < Room.BABY_CHANCE:
            self.entities.append(Zombie(*position))
         
   
   def addItem(self, position):
      """
      Will attempt to add a health pack if we haven't hit the max
      number.
      
      This is invoked by addEntity.
      """
      if len(self.items) < Room.MAX_ITEMS:
         self.items.append(HealthPack(*position))

      elif len(self.items) < Room.MAX_ITEMS:
         self.items.append(Shield(*position))

      elif len(self.items) < Room.MAX_ITEMS:
         self.items.append(UndeadRepellent(*position))
         
   
      
   def cleanUp(self):
      
      # Clean up dead things
      self.entities = [x for x in self.entities if not x.isDead()]
      
      # Clean up used items         
      self.items = [x for x in self.items if not x.used]
   

      
   
