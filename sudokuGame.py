from sudokuSolver import isValid, solver
import pygame
import numpy


class Grid:
	def __init__(self):
		self.board = [[3, 0, 6, 5, 0, 8, 4, 0, 0], 
				[5, 2, 0, 0, 0, 0, 0, 0, 0], 
				[0, 8, 7, 0, 0, 0, 0, 3, 1], 
				[0, 0, 3, 0, 1, 0, 0, 8, 0], 
				[9, 0, 0, 8, 6, 3, 0, 0, 5], 
				[0, 5, 0, 0, 9, 0, 6, 0, 0], 
				[1, 3, 0, 0, 0, 0, 2, 5, 0], 
				[0, 0, 0, 0, 0, 0, 0, 7, 4], 
				[0, 0, 5, 2, 0, 6, 3, 0, 0]]

		self.width = 450
		self.height = 450
		self.cells = []
		self.lives = 5

	def drawGrid(self, screen):
		#Set the size of the big grid blocks
		big_blockSize = 150
		# Draw bigger box areas
		start = 100
		end = 550
		for x in range(start,end):
			for y in range(start,end):

				if x == start or x == start+big_blockSize or x == start+(big_blockSize*2):
					if y == start or y == start+big_blockSize or y == start+(big_blockSize*2):
						rect = pygame.Rect(x, y, big_blockSize, big_blockSize)
						pygame.draw.rect(screen, (255,255,255), rect, 5)

		#Set the size of the big grid blocks
		small_blockSize = 50
		# Draw inner boxes
		for x in range(start,end):
			for y in range(start,end):
				if x % small_blockSize == 0:
					if y % small_blockSize == 0:
						rect = pygame.Rect(x, y, small_blockSize, small_blockSize)
						pygame.draw.rect(screen, (255,255,255), rect, 1)
						# Creating a cell at each box drawn
						value = self.board[(y-start)//50][(x-start)//50]
						if value == 0:
							cell = Cell(small_blockSize, small_blockSize, x, y, value, -1)
							self.cells.append(cell)
						else:
							cell = Cell(small_blockSize, small_blockSize, x, y, value, -2)
							self.cells.append(cell)
							font = pygame.font.Font('freesansbold.ttf', 30)
							text = font.render(str(cell.value), True, (0,255,0))
							screen.blit(text, (cell.xs+cell.width/3, cell.ys+cell.height/3))

		# Draw life count and hint
		font = pygame.font.Font('freesansbold.ttf', 20)
		text = font.render(f"Lives Remaining: {self.lives}", True, (0,255,0))
		screen.blit(text, (0, 0))

		text = font.render("Hint: Press the spacebar to complete the entire board.", True, (0, 0, 200))
		screen.blit(text, (self.width-385, self.height+150))


	def play(self):
		# Initialize pygame
		pygame.init()
		# Open a new window
		SCREEN_HEIGHT = 650
		SCREEN_WIDTH = 650
		screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Ultimate Sudoku")

		# Whether the game should continue running
		run = True
		screen.fill((100, 100, 100))
		self.drawGrid(screen)
		# Continues running the game
		selected = False
		while run:
			pygame.time.wait(100)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if selected:
						pygame.draw.rect(screen, (100, 100, 100), highlighted_box, 2)
						selected = False
					pos = event.pos
					for cell in self.cells:
						if cell.xe >= pos[0] >= cell.xs and cell.ye >= pos[1] >= cell.ys:
							highlighted_box = pygame.Rect(cell.xs+2, cell.ys+2, cell.width-5, cell.height-5)
							pygame.draw.rect(screen, (0,0,0), highlighted_box, 2)
							selected = True
							selected_cell = cell
				if event.type == pygame.KEYUP and selected:
					number = -1
					if event.key >= 0x100 and event.key <= 0x109:
  						key = event.key - 0xD0
					else:
  						key = event.key
					try:
						number = int(chr(key))
					except ValueError:
						pass

					if number > 0 and selected_cell and selected_cell.value == 0 and selected_cell.temp < 0:
						font = pygame.font.Font('freesansbold.ttf', 20)
						text = font.render(str(number), True, (0,0,255))
						screen.blit(text, (selected_cell.xs+selected_cell.width/3, selected_cell.ys+selected_cell.height/3))
						selected_cell.temp = number

					elif (event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE) and selected_cell and selected_cell.temp > 0:
						selected_cell.temp = -1
						rect = pygame.Rect(selected_cell.xs+4, selected_cell.ys+4, selected_cell.width-8, selected_cell.height-8)
						screen.fill((100, 100, 100), rect)

					elif event.key == pygame.K_RETURN and selected_cell and selected_cell.temp > 0:
						rect = pygame.Rect(selected_cell.xs+4, selected_cell.ys+4, selected_cell.width-8, selected_cell.height-8)
						screen.fill((100, 100, 100), rect)
						if self.checkInput(selected_cell.temp, (selected_cell.ys-100)//50, (selected_cell.xs-100)//50):
							selected_cell.value = selected_cell.temp
							selected_cell.temp = -2
							font = pygame.font.Font('freesansbold.ttf', 30)
							text = font.render(str(selected_cell.value), True, (0, 255, 0))
							screen.blit(text, (selected_cell.xs+selected_cell.width/3, selected_cell.ys+selected_cell.height/3))
						else:
							selected_cell.temp = -1
							self.lives -= 1
							self.incorrect(screen)
							if self.lives == 0:
								font = pygame.font.Font('freesansbold.ttf', 65)
								text = font.render("Game Over", True, (255, 0, 0))
								screen.blit(text, (self.width/3-25, self.height/6-50))
								run = False
				
				if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
					solver(self.board)
					start = 100
					end = 550
					for x in range(start, end):
						for y in range(start, end):
							if x % 50 == 0 and y % 50 == 0:
								for cell in self.cells:
									if cell.xs == x and cell.ys == y:
										value = self.board[(y-start)//50][(x-start)//50]
										cell.value = value
										rect = pygame.Rect(x+4, y+4, 42, 42)
										screen.fill((100, 100, 100), rect)
										font = pygame.font.Font('freesansbold.ttf', 30)
										text = font.render(str(value), True, (0,255,0))
										screen.blit(text, (x+50/3, y+50/3))

			complete = True
			for cell in self.cells:
				if cell.value == 0:
					complete = False
			if complete:
				font = pygame.font.Font('freesansbold.ttf', 65)
				text = font.render("Winner!", True, (0, 255, 0))
				screen.blit(text, (self.width/3+50, self.height/6-75))

			pygame.display.update()
			if self.lives == 0:
				pygame.time.wait(2000)


		pygame.quit()


	def checkInput(self, num, posx, posy):
		temp_board = [[self.board[x][y] for y in range(len(self.board[0]))] for x in range(len(self.board))]
		if isValid(posx, posy, num, temp_board):
			temp_board[posx][posy] = num
			if solver(temp_board):
				return True

		return False


	def incorrect(self, screen):
		rect = pygame.Rect(0, 0, 250, 25)
		screen.fill((100, 100, 100), rect)
		font = pygame.font.Font('freesansbold.ttf', 25)
		text = font.render(f"Lives Remaining: {self.lives}", True, (0,255,0))
		screen.blit(text, (0, 0))



class Cell:
	def __init__(self, width, height, x, y, value, temp):
		self.width = width
		self.height = height
		self.xs = x
		self.ys = y
		self.xe = x+width
		self.ye = y+width
		self.temp = temp
		self.value = value


	def setTempt(self, num):
		self.temp = num

def main():
	grid = Grid()
	grid.play()


if __name__ == "__main__":
	main()