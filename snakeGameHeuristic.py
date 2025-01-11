import random
import tkinter as tk
import time

def heuristicPolicy(snake, orb, gridSize, barriers):
    """
    A heuristic algorithm to automate Snake game based on a unified policy formula.

    Parameters:
        snake (list of tuples): The coordinates of the snake's body (head is the first element).
        orb (tuple): The coordinate of the current orb to collect.
        gridSize (tuple): The width and height of the game grid.
        barriers (set of tuples): The coordinates of all barriers on the grid.

    Returns:
        str: The direction for the next move ('UP', 'DOWN', 'LEFT', 'RIGHT').
    """
    def isValid(coord):
        """Check if a coordinate is within bounds, not colliding with the snake, or barriers."""
        x, y = coord
        return 0 <= x < gridSize[0] and 0 <= y < gridSize[1] and coord not in snake[:-1] and coord not in barriers

    def manhattanDistance(a, b):
        """Calculate the Manhattan distance between two points."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Define possible moves and their offsets
    moves = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    # Compute valid moves
    validMoves = []
    for direction, offset in moves.items():
        newHead = (snake[0][0] + offset[0], snake[0][1] + offset[1])
        if isValid(newHead):
            validMoves.append((direction, manhattanDistance(newHead, orb)))

    # Select the best move
    if validMoves:
        # Avoid game-over scenarios first, then prioritize reaching the orb
        bestMove = min(validMoves, key=lambda x: x[1])[0]
    else:
        # Failsafe: Choose a random direction if no valid moves
        bestMove = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

    return bestMove

def generateBarriers(gridSize, snake, orb):
    """Generate random barriers within the grid, ensuring the game is playable at start."""
    totalCells = gridSize[0] * gridSize[1]
    maxBarrierCells = int(0.25 * totalCells)  # 25% of the grid

    barriers = set()
    while len(barriers) < maxBarrierCells:
        barrierSize = random.randint(1, 3)
        startX = random.randint(0, gridSize[0] - 1)
        startY = random.randint(0, gridSize[1] - 1)

        for i in range(barrierSize):
            for j in range(barrierSize):
                x, y = startX + i, startY + j
                if (0 <= x < gridSize[0] and 0 <= y < gridSize[1]
                        and (x, y) not in snake and (x, y) != orb):
                    barriers.add((x, y))

                if len(barriers) >= maxBarrierCells:
                    break

            if len(barriers) >= maxBarrierCells:
                break

    return barriers

def generateOrb(gridSize, snake, barriers):
    """Generate a new orb location that does not overlap with the snake or barriers."""
    while True:
        orb = (random.randint(0, gridSize[0] - 1), random.randint(0, gridSize[1] - 1))
        if orb not in snake and orb not in barriers:
            return orb

def updateGui(canvas, snake, orb, barriers, cellSize, gridSize, score, highscore, elapsedTime):
    """Update the GUI to reflect the current game state."""
    canvas.delete("all")

    # Draw the barriers
    for barrier in barriers:
        bx, by = barrier
        canvas.create_rectangle(
            bx * cellSize, by * cellSize,
            (bx + 1) * cellSize, (by + 1) * cellSize,
            fill="gray"
        )

    # Draw the orb
    orbX, orbY = orb
    canvas.create_rectangle(
        orbX * cellSize, orbY * cellSize,
        (orbX + 1) * cellSize, (orbY + 1) * cellSize,
        fill="red"
    )

    # Draw the snake
    for segment in snake:
        segX, segY = segment
        canvas.create_rectangle(
            segX * cellSize, segY * cellSize,
            (segX + 1) * cellSize, (segY + 1) * cellSize,
            fill="green"
        )

    # Draw the snake's head
    headX, headY = snake[0]
    canvas.create_rectangle(
        headX * cellSize, headY * cellSize,
        (headX + 1) * cellSize, (headY + 1) * cellSize,
        fill="blue"
    )

    # Display score, high score, and elapsed time
    canvas.create_text(
        10, 10, anchor="nw", text=f"Score: {score}", fill="white", font=("Arial", 14, "bold")
    )
    canvas.create_text(
        10, 30, anchor="nw", text=f"High Score: {highscore}", fill="white", font=("Arial", 14, "bold")
    )
    canvas.create_text(
        10, 50, anchor="nw", text=f"Time: {elapsedTime:.2f} s", fill="white", font=("Arial", 14, "bold")
    )

def main():
    # Start timer
    startTime = time.time()

    # Game state
    gridSize = (20, 20)
    cellSize = 20
    snake = [(5, 5), (5, 6), (5, 7)]  # Head is at (5, 5), tail at (5, 7)
    barriers = generateBarriers(gridSize, snake, (0, 0))  # Temporary orb value
    orb = generateOrb(gridSize, snake, barriers)

    # Score tracking
    score = 0
    highscore = 0

    # Initialize GUI
    window = tk.Tk()
    window.title("Snake")
    canvas = tk.Canvas(window, width=gridSize[0] * cellSize, height=gridSize[1] * cellSize, bg="black")
    canvas.pack()

    def resetGame():
        nonlocal snake, orb, barriers, score, startTime
        snake = [(5, 5), (5, 6), (5, 7)]
        barriers = generateBarriers(gridSize, snake, (0, 0))
        orb = generateOrb(gridSize, snake, barriers)
        score = 0
        startTime = time.time()
        gameLoop()

    def gameLoop():
        nonlocal snake, orb, score, highscore

        # Compute the best move
        nextMove = heuristicPolicy(snake, orb, gridSize, barriers)

        # Move the snake
        moves = {
            'UP': (0, -1),
            'DOWN': (0, 1),
            'LEFT': (-1, 0),
            'RIGHT': (1, 0)
        }
        offset = moves[nextMove]
        newHead = (snake[0][0] + offset[0], snake[0][1] + offset[1])

        # Reduce the score for movement
        score -= 1

        # Check for collisions
        if newHead in snake or newHead in barriers:

            # Calculate elapsed time
            elapsedTime = time.time() - startTime

            print("Game Over")
            print(f"Final Score: {score}")
            print(f"Elapsed Time: {elapsedTime:.2f} seconds")
            highscore = max(highscore, score)
            updateGui(canvas, snake, orb, barriers, cellSize, gridSize, score, highscore, elapsedTime)
            window.after(2000, resetGame)  # Restart after 2 seconds
            return

        snake = [newHead] + snake[:-1]

        # Check if the orb is collected
        if newHead == orb:
            snake.append(snake[-1])  # Grow the snake
            orb = generateOrb(gridSize, snake, barriers)
            score += 100

        # Update the GUI
        elapsedTime = time.time() - startTime
        updateGui(canvas, snake, orb, barriers, cellSize, gridSize, score, highscore, elapsedTime)

        # Schedule the next iteration
        window.after(200, gameLoop)

    # Start the game loop
    gameLoop()
    window.mainloop()

if __name__ == "__main__":
    main()
