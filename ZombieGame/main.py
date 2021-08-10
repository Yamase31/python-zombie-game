"""
Framework for a mini zombie game
Author: Elizabeth Matthews
For use in CS 111 at Washington and Lee University
"""

from modules.charInput import getch
from modules.clearScreen import clear
from modules.timer import Timer
from modules.gameObjects import *
from modules.room import Room

from os import path, listdir


class GameEngine(object):
  
   
   def __init__(self, roomsLocation=None):
      """
      Initializes the game engine to the starting
      state of the game.
      """
   
      self.turns = 0
      self.score = 0
      
      # Initialize timers with a minimum and maximum number of turns before spawning something
      self.timers = {
         "zombie" : Timer(Timer.TIMER_ZOMBIE_MIN, Timer.TIMER_ZOMBIE_MAX),
         "item" : Timer(Timer.TIMER_ITEM_MIN, Timer.TIMER_ITEM_MAX)
      }
      
      # Set up rooms
      if roomsLocation == None:
         self.rooms = [Room()]
      else:
         # Get files from the directory
         roomList = listdir(roomsLocation)
         roomList.sort()
         self.rooms = []
         for file in roomList:
            self.rooms.append(Room(roomsLocation + "/" + file))
         
      # Select current room
      self.currentRoom = 0
      
      # Place hero in the center of the room
      self.hero = Hero(*self.rooms[self.currentRoom].heroStart)
      #self.boss = 
      
  
   # Displays all active items in the game
   def display(self):
      """
      Displays the game in its current state.
      """
      
      # Draw the room
      self.rooms[self.currentRoom].drawRoom()
      
      # Draw hero in the room
      self.hero.draw(self.rooms[self.currentRoom].board)      
      
      # Clear terminal screen
      ### Disable this if you need to add print statements elsewhere ###
      clear()
      
      # Display game board to screen      
      print("\n".join(["".join(x) for x in self.rooms[self.currentRoom].board]))
      
      # Display HUD
      print("\nTurn:", self.turns)
      print("Health:", self.hero.hp)
      print("Points:", self.score)
      print("Current Room #" + str(self.currentRoom + 1))
      
      
      ### Print stuff here if you need to check a value ###
      
   
   def update(self, command):
      """
      Allows all active objects in the game to
      think and update their states.
      """
      
      
      # Set up and iterate over each sequence of things that can be updated
      for sequence in [[self.hero], self.rooms[self.currentRoom].entities]:
         # Iterate over each entity in the sequenec
         for entity in sequence:
            # Update based on type of entity
            if isinstance(entity, Hero):
               entity.update(command)
            elif isinstance(entity, Mega):
               entity.update(self.hero)
            elif isinstance(entity, Boss):
               entity.update(self.hero)
            else:
               entity.update()               
         
            # If the entity wants to move somewhere, handle collision
            if entity.targetPosition:
               collider = self.rooms[self.currentRoom].positionCheck(self.hero, entity.targetPosition)
               
               # No collider lets the entity move to their target position
               if collider == None:
                  entity.position = entity.targetPosition
               
               # Allow health packs to be used only by the hero
               elif isinstance(collider, HealthPack) and isinstance(entity, Hero):
                  entity.increaseHP(collider.amount)
                  collider.used = True

##               elif isinstance(collider, Shield) and isinstance(entity, Hero):
##                  while self.amount > 0:
##                     Hero.HP = Hero.HP
##                     self.amount -=1
##                  
##                  collider.used = True

##               elif isinstance(collider, UndeadRepellent) and isinstance(entity, Hero):
##                  if command == " ":
##                     
##                  collider.used = True
               
               # Have entities attack each other only if the hero is attacking a zombie or vice versa
               elif (isinstance(collider, Zombie) and isinstance(entity, Hero)) or (isinstance(collider, Hero) and isinstance(entity, Zombie)):
                  
                  collider.decreaseHP(entity.attack())
                  
                  if isinstance(collider, Mega) and (collider.isDead()):
                     self.score += 5

                  elif isinstance(collider, Zombie) and (collider.isDead()):
                     self.score += 1

                  elif isinstance(collider, BabyZombie) and (collider.isDead()):
                     self.score += 1
                     
               elif (isinstance(collider, Boss) and isinstance(entity, Hero)) or (isinstance(collider, Hero) and isinstance(entity, Boss)):
                  collider.decreaseHP(entity.attack())

                  if isinstance(collider, Boss) and (collider.isDead()):
                     self.score += 50
                     RUNNING = False
                     
               
                                                                              
               elif (isinstance(entity, Hero) or isinstance(entity, Mega) or isinstance(entity, Zombie) or isinstance(entity, BabyZombie) or isinstance(Boss)) and isinstance(collider, Spike):
                  entity.decreaseHP(collider.amount)
                  
               elif (isinstance(entity, Hero) and isinstance(collider, UpStairs)):
                  self.currentRoom += 1
                  
               elif (isinstance(entity, Hero) and isinstance(collider, DownStairs)):
                  self.currentRoom -= 1

               elif isinstance(entity, Hero) and isinstance(collider, Pitfall):
                  self.currentRoom -= 1
                  entity.decreaseHP(collider.amount)

               elif (isinstance(entity, Mega) or isinstance(entity, Zombie) or isinstance(entity, BabyZombie)) and isinstance(collider,Pitfall): 
                  entity.decreaseHP(collider.amount)

               
      
      # Update timers by one
      for t in self.timers.keys():
         self.timers[t].tick()
         
         # Add items if need be
         if self.timers[t].isDone():
            self.rooms[self.currentRoom].addEntity(self.hero, t)
            self.timers[t].reset()
   
   
   def run(self):
      """
      Runs the game until either the game is quit
      or the end condition is met.
      """
      
      RUNNING = True
      
      while(RUNNING):
      
         # Display things
         self.display()
         
         # Get action
         command = getch()
         
         # Check for quit command
         if (command in ["q", "Q"]):
            RUNNING = False
         else:
            # Update things
            self.update(command)
         
         # Remove things that are dead or used
         self.rooms[self.currentRoom].cleanUp()         

         #if boss is dead
##         if self.boss.isDead():
##            RUNNING = False
##         self.display()
##         print("\n\nGame Over! Final score: ", self.score)
         
         # Check for game over
         if self.hero.isDead():
            RUNNING = False
         
         # Increase number of turns
         self.turns += 1
         
      
      # Game over!
      self.display()
      print("\n\nGame Over! Score: ", self.score)
   


if __name__ == '__main__':
   game = GameEngine("rooms")
   
   game.run()
