# snake

Each .py file is a self-contained snake game, differenciated by search algorithms and policies:

* snakeGameAStar.py is A* Search
* snakeGameHeuristic.py is Heuristic Search
* snakeGameHybrid.py is a comination of Heuristic and Flood-Fill searches to account for issue with looping

No requirements, as imports are all included with standard Python 3

For this purpose, the application is kept as a single Python file, with 3 imports:
  1.	random: 
    a.	to perform any move is no legal removes remain
    b.	to place the orb. Once at the start and after each has been collected
    c.	to add blockers within the confines of the game board, to further reduce movement
  2.	tkinter to add a GUI and visual representation of the algorithm being performed
  3.	time:
    a.	to show how much time has elapsed in any given run
    b.	to print the total time of a run when it ends
Processing the algorithm required the following parameters:
  1.	snake (list of tuples): The coordinates of the snake’s body (head is the first element)
  2.	orb (tuple): The coordinate of the current orb to collect
  3.	gridSize (tuple): The width and height of the game grid
  4.	barriers (set of tuples): The coordinates of all the barriers on the grid.

Despite designing an application around the use of multiple different algorithms, the code between each iteration was able to remain largely the same. Each application will calculate their best move; UP, DOWN, LEFT, RIGHT, based on the policy that was programmed. Each game iteration will then move the snake based on this policy. Successfully obtaining an orb would extend the snake’s length by 1 segment, which will then factor into future decision making as the available space around the head would become smaller.
