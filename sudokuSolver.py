import numpy


# Setting up global grid and variables
GRID = [ [3, 0, 6, 5, 0, 8, 4, 0, 0], 
         [5, 2, 0, 0, 0, 0, 0, 0, 0], 
         [0, 8, 7, 0, 0, 0, 0, 3, 1], 
         [0, 0, 3, 0, 1, 0, 0, 8, 0], 
         [9, 0, 0, 8, 6, 3, 0, 0, 5], 
         [0, 5, 0, 0, 9, 0, 6, 0, 0], 
         [1, 3, 0, 0, 0, 0, 2, 5, 0], 
         [0, 0, 0, 0, 0, 0, 0, 7, 4], 
         [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

numRows = len(GRID)
numCols = len(GRID[0])


def main():
	# Calling method to solve the Sudoku
	print(numpy.matrix(GRID))
	print("---------------------------------------------")
	solver(GRID)
	print(numpy.matrix(GRID))


# Method for solving the Sudoku
def solver(grid):
	# Get the first empty cell. If none exist return True
	empty = getEmpty(grid)
	if empty is None:
		return True
	else:
		i, j = empty
		for val in range(1,10):
			# Checking if any of the values between 1-10 work for the current pos
			if isValid(i, j, val, grid):
				# Set current pos to valid value
				grid[i][j] = val
				# Continue completing the rest of the grid until its complete  
				if solver(grid):
					return True
				# Change the current pos back to 0 and try again because that value didn't work
				else:
					grid[i][j] = 0
		# None of the values work so go back one step
		return False


# Method for checking if a value is valid for a pos in the grid
# Params: y of pos, x of pos, value to check
def isValid(y, x, val, grid):
	# Check if ths value exists in the current pos' column
	for i in range(numRows):
		if grid[i][x] == val:
			return False

	# Check if ths value exists in the current pos' row
	for j in range(numCols):
		if grid[y][j] == val:
			return False

	y_prime = int((y//(numRows/3))*3)
	x_prime = int((x//(numCols/3))*3)

	# Check if ths value exists in the current pos' three by three area
	for i in range(y_prime, y_prime+3):
		for j in range(x_prime, x_prime+3):
			if grid[i][j] == val:
				return False

	# The value is valid
	return True


# Method for checking if an empty cell exists and returning it
def getEmpty(grid):
	# Iterating through the entire grid and finding empty cells
	for i in range(numRows):
		for j in range(numCols):
			if grid[i][j] == 0:
				return (i,j)

	return None

if __name__ == "__main__":
	main()
