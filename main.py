import pygame
from random import randrange


class Level(object):
	
	def __init__(self, size, bombCount):
		self.isGenerated = False
		self.size = size
		self.bombCount = bombCount
		self.tiles = []
		self.tilesVisible = []
		self.flags = []
		
	def generate(self, wlX, wlY):
		
		sizeRange = range(self.size)
		
		# init array with empty
		for x in sizeRange:
			self.tiles.append([])
			self.tilesVisible.append([])
			for y in sizeRange:
				self.tiles[x].append(0)
				self.tilesVisible[x].append(False)
		
		# place bombs
		for b in range(self.bombCount):
			valid = False
			while not valid:
				x = randrange(self.size)
				y = randrange(self.size)
				valid = x != wlX and y != wlY and self.tiles[x][y] != -1
				if valid:
					self.tiles[x][y] = -1
		
		# place numbers
		for x in sizeRange:
			for y in sizeRange:
				thisTile = self.tiles[x][y]
				if thisTile == -1:
					continue
				
				val = 0
				if self.isBomb(x - 1, y - 1): val = val + 1
				if self.isBomb(x, y - 1): val = val + 1
				if self.isBomb(x + 1, y - 1): val = val + 1
				if self.isBomb(x - 1, y): val = val + 1
				if self.isBomb(x + 1, y): val = val + 1
				if self.isBomb(x - 1, y + 1): val = val + 1
				if self.isBomb(x, y + 1): val = val + 1
				if self.isBomb(x + 1, y + 1): val = val + 1
				
				self.tiles[x][y] = val
		
		self.isGenerated = True
				
	def isInBounds(self, x, y):
		if x < 0 or x >= self.size:
			return False
		if y < 0 or y >= self.size:
			return False
		return True
		
				
	def isBomb(self, x, y):
		if not self.isInBounds(x, y):
			return False
		return self.tiles[x][y] == -1
	
	def isTileVisible(self, x, y):
		return self.tilesVisible[x][y]
	
	def placeFlag(self, x, y):
		if self.isTileVisible(x, y):
			return
		if (x, y) in self.flags:
			self.flags.remove((x, y))
		else:
			self.flags.append((x, y))
	
	def clickTile(self, x, y):
		if self.tilesVisible[x][y]:
			return False
		thisTile = self.tiles[x][y]
		if thisTile == -1:
			return True
		elif thisTile == 0:
			self.checkNeighbours([], x, y)
		else:
			self.tilesVisible[x][y] = True
			if (x, y) in self.flags:
				self.flags.remove((x, y))
		return False
			
		
	def checkNeighbours(self, visited, x, y):
		if not self.isInBounds(x, y):
			return
		if (x, y) in visited:
			return	
		visited.append((x, y))
		
		thisTile = self.tiles[x][y]
		if thisTile == -1:
			return
		
		self.tilesVisible[x][y] = True
		if (x, y) in self.flags:
			self.flags.remove((x, y))
		
		if thisTile == 0:
			
			self.checkNeighbours(visited, x - 1, y - 1)
			self.checkNeighbours(visited, x, y - 1)
			self.checkNeighbours(visited, x + 1, y - 1)
			self.checkNeighbours(visited, x - 1, y)
			self.checkNeighbours(visited, x + 1, y)
			self.checkNeighbours(visited, x - 1, y + 1)
			self.checkNeighbours(visited, x, y + 1)
			self.checkNeighbours(visited, x + 1, y + 1)
		
	
def loadTile(name, size):
	img = pygame.image.load("img/" + name + ".png").convert_alpha()
	w, h = img.get_size()
	img = pygame.transform.scale(img, (size, size))
	return img
	
	
if __name__ == "__main__":

	GRID_SIZE = 16
	TILE_SIZE = 32
	BOMB_COUNT = 20
	
	screen = pygame.display.set_mode((GRID_SIZE * TILE_SIZE, GRID_SIZE * TILE_SIZE))
	
	TILE_CACHE = {
		'tile': loadTile('tile', TILE_SIZE),
		'flag': loadTile('flag', TILE_SIZE),
		'-1': loadTile('bomb', TILE_SIZE),
		'0': loadTile('0', TILE_SIZE),
		'1': loadTile('1', TILE_SIZE),
		'2': loadTile('2', TILE_SIZE),
		'3': loadTile('3', TILE_SIZE),
		'4': loadTile('4', TILE_SIZE),
		'5': loadTile('5', TILE_SIZE),
		'6': loadTile('6', TILE_SIZE),
		'7': loadTile('7', TILE_SIZE),
		'8': loadTile('8', TILE_SIZE)
	}

	level = Level(GRID_SIZE, BOMB_COUNT)

	clock = pygame.time.Clock()
	
	
	isBomb = False
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONUP:
				x, y = event.pos
				x = int(x / TILE_SIZE)
				y = int(y / TILE_SIZE)
				if event.button == 1: # left click
					if not level.isGenerated:
						level.generate(x, y)
					isBomb = level.clickTile(x, y)
				elif event.button == 3: # right click
					if level.isGenerated:
						level.placeFlag(x, y)
					
		screen.fill((192, 192, 192))
		
		for x in range(level.size):
			for y in range(level.size):
				
				if level.isGenerated and (isBomb or level.isTileVisible(x, y)):
					tile = level.tiles[x][y]
					surf = TILE_CACHE[str(tile)]
				else:
					surf = TILE_CACHE["tile"]
				
				screen.blit(surf, (x * TILE_SIZE, y * TILE_SIZE))
				
		for pos in level.flags:
			
			surf = TILE_CACHE["flag"]
			screen.blit(surf, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))

		pygame.display.flip()
				
	pygame.quit()
	
	
	
	
	
	
	
	
	
	
				