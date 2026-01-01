"""
missile:
	spawn
	track
	
plane:
	controls
	blow up

"""
import random
import math
import time
import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vector

from missile import Missile , Missiles
from plane import Plane,control_plane
from consts import *



def make_grid():
	surf= pygame.Surface((750,1550))
	surf.fill((255,255,255))
	for i in range(0,75,2):
		for j in range(0,155,2):
			pygame.draw.rect(surf,(230,230,230),(10*i,10*j,10,10))
		
	return surf
			

class Camera:
	def __init__(self):
		self.x = 0
		self.target_x= 0
		self.y = 0
		self.target_y= 0
		
		
		
		self.dead_x= 200
		self.dead_y= 200

	   

	def apply(self, position):
		
		return (position.x-self.x+360,position.y-self.y+740)

	def update(self, plane):	
		# Horizontal scrolling
		screen_x,screen_y= self.apply(plane.position)
		if screen_x< 360-self.dead_x:
			self.target_x= self.x-100
		elif screen_x> 360+self.dead_x:
			self.target_x= self.x+100

		# Vertical scrolling
		if screen_y   < 740-self.dead_y:
			self.target_y= self.y-100
		elif screen_y> 740+self.dead_y:
			self.target_y= self.y+100
		   
		if abs(self.x-self.target_x)>5:
			self.x-= (self.x-self.target_x)/100
		if abs(self.y-self.target_y)>5:
			self.y-= (self.y-self.target_y)/100
	  
def main():
	
	pygame.init()
	myfont = pygame.font.SysFont("Arial", 64)

	win = pygame.display.set_mode((720, 1480))
	clock = pygame.time.Clock()
	camera = Camera()
	
	
	
	plane= Plane(pygame.math.Vector2(0,0))
	missiles= Missiles()
	missiles.spawn_missile(plane)
	grid= make_grid()
	while True:
		
		camera.update(plane)
		
		label = myfont.render(f"{plane.hits},{plane.position}{camera.x}{camera.y}", 1, (128, 255, 128))
		control_plane(plane, missiles.get_visable(plane))
		x= plane.position.x%20
		y= plane.position.y%20
		win.blit(grid, (20-x,20-y))
		
		if len(missiles.missiles) <1:
			missiles.spawn_missile(plane)
			
		plane.update(missiles.missiles[0])
		missiles.update(plane)
				
		
	
		#plane.draw(win)
		win.blit(plane.get_image(), camera.apply(plane.position))
		
	#	missiles.draw(win, Vector(350-plane.x, 740-plane.y))
		missiles.new_draw(win, camera)
		win.blit(label,(10,10))
		pygame.display.flip()
		clock.tick(120)		
		win.fill((255,255,255))
		

main()