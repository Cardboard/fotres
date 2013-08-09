import sys
import math
import pygame

class Vertex:
	def __init__(self, x, y):
		# set initial position
		# values are relative to VertexGroup's (x,y)
		# eg: vertex (0, 10) would be at (50, 35) if VertexGroup
		# position is (50, 25). ie: (0, 10) -> (50+0, 35+10)
		self.x = x
		self.y = y
		self.norm = 1  # normalizing factor

class VertexGroup:
	def __init__(self, (x, y), closed, *args):
		self.x = x # global x position, relative to upper left corner
		self.y = y # global y position, relative to upper left corner
		self.vertices = []
		self.scale = 1.0
		self.color = (255, 255, 255, 255)
		self.closed = closed 
		self.width = 1
		for vertex in args:
			self.vertices.append(vertex)

	def setColor(self, _r,_g,_b_,_a=255):
		self.color = (_r, _g, _b, _a)

	def setScale(self, scale):
		self.scale = scale

	def matrixMul(self, vertex, matrix):
		new_x = vertex.x*matrix[0][0] + vertex.y*matrix[1][0] + vertex.norm*matrix[2][0]
		new_y = vertex.x*matrix[0][1] + vertex.y*matrix[1][1] + vertex.norm*matrix[2][1]
		return new_x, new_y

	# responsible for translating, scaling, and rotating vertices
	def transform(self, transx=0,transy=0,scalex=1,scaley=1,degrees=0):
		for vertex in self.vertices:
			radians = degrees*math.pi/180
			cs = math.cos(radians)
			sn = math.sin(radians)
			# create the transformation matrix
			matrix = [
					[scalex*cs, scalex*-sn, 0],
					[scaley*sn, scaley*cs, 0],
					[transx, transy, 1]
					]
			# apply the transformation
			vertex.x, vertex.y = self.matrixMul(vertex, matrix)

			#radians = degrees*math.pi/180
			#x, y = vertex.x, vertex.y
			#new_x = x * math.cos(radians) - y * math.sin(radians)
			#new_y = y * math.cos(radians) + x * math.sin(radians)
			#vertex.x, vertex.y = new_x, new_y

	def draw(self, window):
		num_vertices = len(self.vertices)
		for i in range(num_vertices):
			# draw a line from current vertex to the next vertex
			# only if a next vertex exists
			if i != num_vertices-1:
				pygame.draw.line(window, self.color,
							(self.vertices[i].x*self.scale+self.x, self.vertices[i].y*self.scale+self.y),
							(self.vertices[i+1].x*self.scale+self.x, self.vertices[i+1].y*self.scale+self.y),
							self.width)
			# close the shape by connecting last point to first
			if i == num_vertices-1 and self.closed == True:
				pygame.draw.line(window, self.color,
							(self.vertices[i].x*self.scale+self.x, self.vertices[i].y*self.scale+self.y),
							(self.vertices[0].x*self.scale+self.x, self.vertices[0].y*self.scale+self.y),
							self.width)


v1 = Vertex(-10,-10)
v2 = Vertex(-10,10)
v3 = Vertex(10,10)
v4 = Vertex(10,-10)
v5 = Vertex(0, -5)

vg1 = VertexGroup((200, 200),True, v1,v2,v3,v4,v5)
vg1.setScale(10.0)

pygame.init()
window = pygame.display.set_mode((500,500))
fps = 30
clock = pygame.time.Clock()


if __name__ == '__main__':
	degrees = 0
	scale = 1
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
					pygame.quit()
				if event.key == pygame.K_RIGHT:
					degrees = 5	
				if event.key == pygame.K_LEFT:
					degrees = -5
				if event.key == pygame.K_UP:
					scale = 1.1
				if event.key == pygame.K_DOWN:
					scale = 0.9
				if event.key == pygame.K_SPACE:
					degrees = 0
					scale = 1
		vg1.transform(scalex=scale,scaley=scale,degrees=degrees)

		window.fill((0, 0, 0))
		pygame.draw.rect(window, (255,0,255), (199,199,3,3))
		vg1.draw(window)
		pygame.display.flip()

		clock.tick(fps)
