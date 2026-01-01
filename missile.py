import random
import math
import pygame
from pygame.math import Vector2 as Vector
from consts import *	
			
def random_vector():
		t = random.uniform(0, 2*math.pi)
		return Vector(math.cos(t), math.sin(t))


def distance(this, that):
	a= this.position
	b= that.position
	return math.hypot(a.x-b.x,a.y-b.y)
	
	
class Missile:
	def __init__(self, position, velocity):
		self.position= position
		self.velocity= velocity
		self.acceleration= Vector(0,0)
		self.has_seen_plane= False
		self.active= True
		self.been_hit= False
		self.lifetime=random.randint(300,1000)
		
		self.heading= 0
		self.target_heading= 0
	
		self.rect= pygame.Rect(self.x,self.y,20,20)
		
	def get_image(self):
		surface = pygame.Surface((40, 40), pygame.SRCALPHA)

		surface.fill((255, 0, 0, 0))
		vel= self.velocity*5
		
		pygame.draw.line(surface, (111,111,111), (20-vel.x/2,20-vel.y/2),(20+vel.x/2,vel.y/2+20),5)
		
		
		
		pygame.draw.circle(surface, (255,128,255), (20+vel.x, 20+vel.y),2)
		
		
		return surface
		
		
	@property
	def x(self):
		return self.position.x
	
	@property
	def y(self):
		return self.position.y
	
	
		
		
	def draw(self, win, adjustment):
		
		pos= self.position +adjustment
		vel= self.velocity*2
		velx,vely = vel.x,vel.y
		pygame.draw.line(win, (0,0,0), (pos.x,pos.y),(pos.x+velx,vely+pos.y),3)
		
		new_x= math.sin(self.heading*(math.pi*2/360))*10
		new_y = math.cos(self.heading*(math.pi*2/360))*10
		
		pygame.draw.circle(win, (255,128,255), (pos.x+new_x, pos.y+new_y),5)
		
		
	def update_heading(self):
		dheading= self.target_heading-self.heading
		
		if abs(dheading)<MISSILE_TURNING_RADIUS:
			self.heading+=dheading
		else:
			self.heading+= MISSILE_TURNING_RADIUS * dheading/abs(dheading)
		
		new_x= math.sin(self.heading*(math.pi*2/360))
		new_y = math.cos(self.heading*(math.pi*2/360))
		self.velocity= Vector(new_x,new_y)
		
	def hit(self):
		self.been_hit= True
		self.active= False	
		
	def limit_speed(self):
		self.velocity=self.velocity.normalize()*MISSILE_SPEED
		
	def update(self, plane):
		self.lifetime-= 0
		if self.lifetime<0:
			self.active =False
			return
		if distance(self, plane)> SPAWN_RADIUS*1.5:
			self.active= False
			return
		
		#upate movemnt
		self.update_heading()
		self.limit_speed()
		self.position += self.velocity
		
		if distance(self, plane)<35:
			self.has_seen_plane= True
			
class Missiles:
		def __init__(self):
			self.missiles= []
		
		def add(self, missile):
			self.missiles.append(missile)
		def remove(self, missile):
			self.missiles.remove(missile)
		
		def draw(self, win,adjustment):
			# draw missilss
			for missile in self.missiles:
				missile.draw(win, adjustment)
				
		def new_draw(self, win, camera):
			for missile in self.missiles:
				win.blit(missile.get_image(), camera.apply(missile.position))
			
			
		def update(self, plane):
			removals=[]
			for missile in self.missiles:
				if missile.active:
					control_missile(missile,plane)
					missile.update(plane)
				else:
					removals.append(missile)
			
			for missile in removals:
				self.remove(missile)
				
			self.hits(plane)
		def spawn_missile(self,plane):
			
			position=  random_vector()*SPAWN_RADIUS+plane.position
			missileToPlane = position-plane.position
			#turn a lil bit
			self.add(Missile(position, missileToPlane))
		def hits(self, plane):
			for missile in self.missiles:
				if missile.been_hit:
					continue
				if distance(missile,plane)<5:
					missile.hit()
					plane.hit()
				
				for other in self.missiles:
					if other.been_hit:
						continue
					if missile is other:
						continue
					if distance(missile,other)<5:
						missile.hit()
						other.hit()
						
						
		def get_visable(self,plane):
				visable= []
				for missile in self.missiles:
					dis= distance(missile, plane)
					if dis < PLANE_VISABLE_RANGE:
						visable.append(missile)
					elif dis <= PLANE_VISABLE_RANGE*1.5:
						p2m = missile.position-plane.position
						if abs(plane.velocity.angle_to(p2m))< math.pi/6:
							visable.append(missile)
							
					
				return visable
					
			
		
			
def control_missile(missile,plane):
	m2p= -missile.position+plane.position
		
	t= math.atan2(m2p.x,m2p.y) * 360 / ( 2* math.pi)
	
	
	if not missile.has_seen_plane:
		
		missile.heading= t
		missile.target_heading= t
	
	missile.target_heading= t
	
	
	
		
			

