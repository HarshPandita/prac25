from collections import deque

class SnakeGame:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.directions = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
        }

        # Snake body: tail at front (left), head at end (right)
        self.snake = deque([(0, 0), (0, 1), (0, 2)])  # initial size = 3
        self.snake_set = set(self.snake)  # for O(1) collision checks
        self.move_count = 0
        self.game_over = False

    def moveSnake(self, direction: str):
        if self.game_over:
            return

        dx, dy = self.directions[direction]
        head_x, head_y = self.snake[-1]
        new_head = (head_x + dx, head_y + dy)

        # collission handling
        # new_head = (
        # new_head[0] % self.board_size,
        # new_head[1] % self.board_size
        # )

        # Check wall collision
        if not (0 <= new_head[0] < self.board_size and 0 <= new_head[1] < self.board_size):
            self.game_over = True
            return
            

        # If not growing, remove tail temporarily for collision check
        grow = (self.move_count + 1) % 5 == 0
        if not grow:
            tail = self.snake.popleft()
            self.snake_set.remove(tail)

        # Self collision
        if new_head in self.snake_set:
            self.game_over = True
            return

        # Move head
        self.snake.append(new_head)
        self.snake_set.add(new_head)
        self.move_count += 1

        # If growing, re-attach the tail we skipped removing
        if grow:
            self.snake.appendleft(tail)
            self.snake_set.add(tail)

    def isGameOver(self) -> bool:
        return self.game_over

    def getSnake(self) -> list:
        return list(self.snake)




