"""
missile:
	spawn
	track
	
plane:
	controls
	blow up

"""
SPAWN_RADIUS=50
MISSILE_SPEED= 1.2

class Vector:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	@classmethod
	def random():
			angle= random.random()*math.pi
			return Vector(math.cos(angle),math.sin(angle))
			
	def __mul__(self,other):
		return Vector(self.x*other, self.y*other)
	def __add__(self,other):
		return Vector(self.x+other.x, self.y+other.y)
	def __len__(self):
		return math.sqrt(self.x**2+self.y**2)
		
	def dot(self,other):
		return self.x*other.x+ self.y*other.y
	
	def normalise(self):
		return self* (1/len(self))
		
class Missile:
	def __init__(self, position, velocity):
		self.position= position
		self.velocity= velocity
		self.acceleration= Vector(0,0)
		self.has_seen_plane= False
		
	def limit_speed(self):
		self.velocity=self.velocity.normalise()*MISSILE_SPEED)
		
	def update(self, plane):
		self.velocity += self.acceleration
		self.acceleration *= 1/2
		self.limit_speed()
		self.position += self.velocity
		
		
		if self.has_seen_plane:
			pass
		else:
			missileToPlane = position- plane.position
			self.acceleration+= self.velocity.dot(missileToPlane)

class Missiles:
		def __init__(self):
			self.missiles= []
		
		def add(self, missile):
			self.missiles.append(missle)
		ded remove(self, missile):
			self.missiles.remove(missile)
		
		def update(self, plane):
			removals=[]
			for missile in self.missiles:
				if missile.active:
					missile.update(plane)
				else:
					removals.append(missile)
			
			for missile in removals:
				self.remove(missile)
		def spawn_missile(plane):
			position= SPAWN_RADIUS* Vector.random()+plane.position
			missileToPlane = position- plane.position
			#turn a lil bit
			self.add(Missile(position, missileToPlane))
		
		
			
		
class Plane:
	def __init__(self, position):
		self.position= position
		self.velocity=Vector(0,1)
	def update(self):
		self.position += self.velocity



	

def main():
	plane= Plane(Vector(0,0))
	missiles= Missiles()
	missiles.spawn_missile(plane)