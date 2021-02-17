import pygame
import math
from random import randint
from queue import PriorityQueue

pygame.init()

ROWS = 50

WIDTH = 700
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Screen Size
pygame.display.set_caption("A* Path Finding Algorithm")

# COLORS
START_COLOR = (124, 32, 49)
END_COLOR = (0, 255, 0)
WALL_COLOR = (12, 53, 71)
VISITED_COLOR = (63, 203, 223)
VISITED_OUTER_COLOR = (197, 114, 255)
UNVISITED_COLOR = (255, 255, 255)
WALL_BOUNDARY_COLOR = (175, 216, 248)
PATH_COLOR = (255, 255, 0)
WIN_BACKGROUND_COLOR = (255, 255, 255)

# defining a font and a text
smallfont = pygame.font.SysFont('Corbel',35)
text = smallfont.render('Start Visualizing' , True , UNVISITED_COLOR) 

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = UNVISITED_COLOR
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == VISITED_COLOR

	def is_open(self):
		return self.color == VISITED_OUTER_COLOR

	def is_barrier(self):
		return self.color == WALL_COLOR

	def reset(self):
		self.color = UNVISITED_COLOR

	def make_start(self):
		self.color = START_COLOR

	def make_closed(self):
		self.color = VISITED_COLOR

	def make_open(self):
		self.color = VISITED_OUTER_COLOR

	def make_barrier(self):
		self.color = WALL_COLOR

	def make_end(self):
		self.color = END_COLOR

	def make_path(self):
		self.color = PATH_COLOR

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		#DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.col])
		#UP
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.col])
		#RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col + 1])
		#LEFT
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False



# Heuristic Function
def hf(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#Mahattan Distance
	return abs(x1 - x2) + abs(y1 - y2)
	#Euclidean Distance
	#return ( (x1 - x2)**2 + (y1 - y2)**2 )**1/2

def reconstruct_path(grid, came_from, current):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		print((current.row, current.col))
		draw(WIN, grid, ROWS, WIDTH)

def performAStartAlgorithm(win, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = hf(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(grid, came_from, end)
			end.make_end()
			start.make_start()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + hf(neighbor.get_pos(), end.get_pos())

				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw(win, grid, ROWS, WIDTH)

		if current != start:
			current.make_closed()

	return False

def performDijkstrasAlgorithm(draw, grid, start, end):
	pass

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, WALL_BOUNDARY_COLOR, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, WALL_BOUNDARY_COLOR, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	#print("Function DRAW")
	win.fill(WIN_BACKGROUND_COLOR)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True

	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				run = False
			
			if pygame.mouse.get_pressed()[0]: #LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()

				if spot == start: start = None
				elif spot == end: end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					performAStartAlgorithm(win, grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
					print("Grid Cleared")

	pygame.quit()
	print("Successfully Visualized")

main(WIN, WIDTH) 

'''
while True: 
	
	for ev in pygame.event.get(): 
		
		if ev.type == pygame.QUIT: 
			pygame.quit() 
			
		#checks if a mouse is clicked 
		if ev.type == pygame.MOUSEBUTTONDOWN: 
			
			#if the mouse is clicked on the 
			# button the game is terminated 
			if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
				pygame.quit() 
				
	# fills the screen with a color 
	screen.fill((60,25,60)) 
	
	# stores the (x,y) coordinates into 
	# the variable as a tuple 
	mouse = pygame.mouse.get_pos() 
	
	# if mouse is hovered on a button it 
	# changes to lighter shade 
	if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
		pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
		
	else: 
		pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
	
	# superimposing the text onto our button 
	screen.blit(text , (width/2+50,height/2)) 
	
	# updates the frames of the game 
	pygame.display.update() 

'''
