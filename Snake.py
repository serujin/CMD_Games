import os
import msvcrt
import random
import time


def cls():
    os.system('cls')


def get_change(difficulty):
    to_return = random.randint(1, 80) / 10000
    if difficulty - to_return < 0:
        return difficulty
    return to_return


class Game:
    HEAD = 0
    BODY = 1
    TAIL = 2
    APPLE = 3
    WALL = 4
    NONE = 5

    CHARACTERS = {
        HEAD: 'O',
        BODY: 'o',
        TAIL: 'x',
        APPLE: '■',
        WALL: '█',
        NONE: ' '
    }

    W = 119
    A = 97
    S = 115
    D = 100

    ESC = 27

    HEIGHT = 30
    WIDTH = HEIGHT * 2

    E_NUMBER = 2.71828

    apple_position = []
    game_map = []
    last_positions = []
    last_direction = 0
    current_points = 0
    difficulty = 0.2

    def __init__(self):
        self.init_window()
        self.init_map()

        while True:
            time.sleep(self.difficulty)
            self.user_input()
            self.check_collisions()
            self.update()
            self.render()

    def init_window(self):
        os.system('mode ' + str(self.WIDTH) + ',' + str(self.HEIGHT + 3))

    def init_map(self):
        self.apple_position = [-1, -1]
        head_position = [random.randint(1, self.WIDTH - 2), random.randint(1, self.HEIGHT - 2)]
        self.last_positions = [head_position]
        self.create_apple()
        self.update_map()

    def update_map(self):
        self.game_map = []
        for i in range(self.HEIGHT):
            row = []
            for j in range(self.WIDTH):
                row.append(self.NONE)
                if i == 0 or i == self.HEIGHT - 1 or j == 0 or j == self.WIDTH - 1:
                    row[j] = self.WALL
                for position in self.last_positions:
                    if j == position[0] and i == position[1]:
                        row[j] = self.BODY
                if j == self.apple_position[0] and i == self.apple_position[1]:
                    row[j] = self.APPLE
                if j == self.last_positions[0][0] and i == self.last_positions[0][1]:
                    row[j] = self.HEAD
            self.game_map.append(row)

    def create_apple(self):
        self.apple_position[0] = random.randint(1, self.WIDTH - 2)
        self.apple_position[1] = random.randint(1, self.HEIGHT - 2)

    def eat_apple(self):
        self.difficulty -= get_change(self.difficulty)
        self.current_points += 1
        self.last_positions.append([-1, -1])
        self.create_apple()
        char_at_apple_position = self.game_map[self.apple_position[1]][self.apple_position[0]]
        while char_at_apple_position != self.NONE:
            self.create_apple()
            char_at_apple_position = self.game_map[self.apple_position[1]][self.apple_position[0]]

    def update_tail(self):
        for i in reversed(range(len(self.last_positions))):
            if i != 0:
                self.last_positions[i] = [self.last_positions[i - 1][0], self.last_positions[i - 1][1]]

    def move(self, direction):
        if direction == self.W:
            self.last_positions[0][1] -= 1
        if direction == self.A:
            self.last_positions[0][0] -= 1
        if direction == self.S:
            self.last_positions[0][1] += 1
        if direction == self.D:
            self.last_positions[0][0] += 1
        self.update_tail()

    def user_input(self):
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == self.ESC:
                quit()
            if key == self.W and self.last_direction != self.S:
                self.last_direction = self.W
            if key == self.A and self.last_direction != self.D:
                self.last_direction = self.A
            if key == self.S and self.last_direction != self.W:
                self.last_direction = self.S
            if key == self.D and self.last_direction != self.A:
                self.last_direction = self.D

    def check_collisions(self):
        next_position = [-1, -1]
        if self.last_direction == self.W:
            next_y = self.last_positions[0][1] - 1
            next_position = self.game_map[next_y][self.last_positions[0][0]]
        if self.last_direction == self.A:
            next_x = self.last_positions[0][0] - 1
            next_position = self.game_map[self.last_positions[0][1]][next_x]
        if self.last_direction == self.S:
            next_y = self.last_positions[0][1] + 1
            next_position = self.game_map[next_y][self.last_positions[0][0]]
        if self.last_direction == self.D:
            next_x = self.last_positions[0][0] + 1
            next_position = self.game_map[self.last_positions[0][1]][next_x]
        if next_position == self.WALL or next_position == self.BODY:
            self.end_game()

    def update(self):
        self.move(self.last_direction)
        if self.apple_position[0] == self.last_positions[0][0] and self.apple_position[1] == self.last_positions[0][1]:
            self.eat_apple()
        for i in range(len(self.last_positions)):
            position = self.last_positions[i]
            if i == len(self.last_positions) - 1:
                self.game_map[position[1]][position[0]] = self.TAIL
            if i == 0:
                self.game_map[position[1]][position[0]] = self.HEAD
            else:
                self.game_map[position[1]][position[0]] = self.BODY

    def render(self):
        cls()
        self.update_map()
        points = 'POINTS: ' + str(self.current_points)
        speed = (0.5 - self.difficulty) * 100
        difficulty = ' SPEED: ' + '{:.2f}'.format(speed)
        final_map = points + difficulty + '\n'
        for row in self.game_map:
            characters = ''
            for character in row:
                characters += self.CHARACTERS[character]
            characters += '\n'
            final_map += characters
        print(final_map)

    def end_game(self):
        self.update()
        self.render()
        time.sleep(1)
        end_text = '\n  Game Over\n'
        speed = (0.5 - self.difficulty) * 100
        end_text += '\n  TOTAL POINTS: ' + str(self.current_points) + '\n  MAX SPEED: {:.2f}'.format(speed)
        end_text += '\n\n  Thanks for playing\n  You can see more on my github:\n  https://github.com/serujin'
        end_text += ''
        cls()
        print(end_text)
        input('\n\nPress enter to exit\n\n')


Game()
