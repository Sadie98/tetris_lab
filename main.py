import pygame
from pygame.locals import *
import random
from ResManager import *


if __name__ == '__main__':
    # Инициализируем pygame.
    pygame.init()

    # Устанавливаем разрешение экрана.
    pygame.display.set_mode((640,480))

    # Создаем менеджер ресурсов, мы используем значения по умолчанию
    # для функции __init__, так как они нас устраивают.
    manager = ResManager()

    # Устанавливаем иконку.
    pygame.display.set_icon(manager.get_image('icon.png'))
    # Устанавливаем заголовок.
    pygame.display.set_caption("Plambir")

    # А это что бы окно не закрылось сразу.
    time.sleep(10)


class TetrisGame:
    def __init__(self, width, height, cell_size, speed = 2):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)


        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size


        self.speed = speed

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Tetris')
        self.screen.fill(pygame.Color('gray'))
        self.draw_grid()
        running = True
        this_cell_list = CellList(rows=self.height//self.cell_size,cols=self.width//self.cell_size,cell_size=self.cell_size)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if this_cell_list.end_came == True:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == eval("pygame.K_DOWN"):
                        this_cell_list.rotate()
                        this_cell_list.draw()
                        self.draw_grid()
                    if event.key == eval("pygame.K_RIGHT"):
                        this_cell_list.move_right()
                        this_cell_list.draw()
                        self.draw_grid()
                    if event.key == eval("pygame.K_LEFT"):
                        this_cell_list.move_left()
                        this_cell_list.draw()
                        self.draw_grid()
                    if event.key == eval("pygame.K_SPACE"):
                        this_cell_list.move_down()
                        this_cell_list.draw()
                        self.draw_grid()
            self.speed += this_cell_list.delta_speed
            this_cell_list.delete_row()
            this_cell_list.draw()
            self.draw_grid()
            this_cell_list.update_list()
            pygame.display.flip()
            clock.tick(self.speed)
            pygame.display.update()
        pygame.quit()

def new_figure():
    figure = [[], [], [], []]
    num_of_figure = random.randint(1, 5)
    #num_of_figure = 4
    if num_of_figure == 1:
        figure[0].append(0)
        figure[0].append(1)
        figure[1].append(0)
        figure[1].append(2)
        figure[2].append(0)
        figure[2].append(3)
        figure[3].append(0)
        figure[3].append(4)
    elif num_of_figure == 2:
        figure[0].append(1)
        figure[0].append(2)
        figure[1].append(1)
        figure[1].append(3)
        figure[2].append(1)
        figure[2].append(4)
        figure[3].append(0)
        figure[3].append(3)
    elif num_of_figure == 3:
        figure[0].append(1)
        figure[0].append(3)
        figure[1].append(1)
        figure[1].append(4)
        figure[2].append(0)
        figure[2].append(3)
        figure[3].append(0)
        figure[3].append(4)
    elif num_of_figure == 4:
        figure[0].append(2)
        figure[0].append(4)
        figure[1].append(2)
        figure[1].append(3)
        figure[2].append(1)
        figure[2].append(3)
        figure[3].append(0)
        figure[3].append(3)
    elif num_of_figure == 5:
        figure[0].append(2)
        figure[0].append(4)
        figure[1].append(1)
        figure[1].append(4)
        figure[2].append(1)
        figure[2].append(3)
        figure[3].append(0)
        figure[3].append(3)

    return figure, num_of_figure

class CellList:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.result = []
        self.points = 0
        self.delta_speed = 0
        self.end_came = False
        self.moving_figure, self.type_of_figure = new_figure()
        for i in range(rows):
            self.result.append([])
            for j in range(cols):
                self.result[i].append(0)

    def __iter__(self):
        self.i = 0
        self.j = 0
        return self

    def __next__(self):
        if self.j == self.cols:
            self.i += 1
            self.j = 0
        if self.i == self.rows:    # and self.j == self.cols:
            raise StopIteration
        if self.j < self.cols:
            res = self.result[self.i][self.j]
            self.j += 1
            return res

    def __str__(self):
        return str(self.result)

    def __repr__(self):
        return str(self.result)

    def draw(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.result[i][j] == 1:
                    pygame.draw.rect(game.screen, pygame.Color('green'),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                if self.result[i][j] == 0:
                    pygame.draw.rect(game.screen, pygame.Color('white'),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def move_figure(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0
        if not self.on_bottom():
            self.moving_figure[0][0] += 1
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.moving_figure[1][0] += 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.moving_figure[2][0] += 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.moving_figure[3][0] += 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            self.end_came = not self.game_over()
            return True

        else:
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            self.end_came = not self.game_over()
            return False

            self.moving_figure, self.type_of_figure = new_figure()

    def update_list(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0
        if not self.on_bottom():
            self.move_figure()
        else:
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            self.end_came = not self.game_over()
            self.moving_figure, self.type_of_figure = new_figure()

    def rotate(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0
        if self.type_of_figure == 1:
            if self.moving_figure[0][0] == self.moving_figure[1][0]:
                self.moving_figure[0][0] -= 2
                self.moving_figure[0][1] += 2
                self.moving_figure[1][0] -= 1
                self.moving_figure[1][1] += 1
                self.moving_figure[3][0] += 1
                self.moving_figure[3][1] -= 1
            else:
                self.moving_figure[0][0] += 2
                self.moving_figure[0][1] -= 2
                self.moving_figure[1][0] += 1
                self.moving_figure[1][1] -= 1
                self.moving_figure[3][0] -= 1
                self.moving_figure[3][1] += 1


        elif self.type_of_figure == 2:
            if self.moving_figure[0][0] == self.moving_figure[2][0]:
                self.moving_figure[0][0] += 1
                self.moving_figure[0][1] += 1
            elif self.moving_figure[3][1] == self.moving_figure[0][1]:
                self.moving_figure[3][0] += 1
                self.moving_figure[3][1] -= 1
            elif self.moving_figure[3][0] == self.moving_figure[2][0]:
                self.moving_figure[2][0] -= 1
                self.moving_figure[2][1] -= 1
            else:
                self.moving_figure[0][0] -= 1
                self.moving_figure[0][1] -= 1
                self.moving_figure[2][0] += 1
                self.moving_figure[2][1] += 1
                self.moving_figure[3][0] -= 1
                self.moving_figure[3][1] += 1


        elif self.type_of_figure == 3:
            pass


        elif self.type_of_figure == 4:
            if self.moving_figure[3][1] == self.moving_figure[2][1]:
                self.moving_figure[3][0] += 2
                self.moving_figure[3][1] += 2
                self.moving_figure[2][0] += 2
            elif self.moving_figure[0][0] == self.moving_figure[2][0] - 1:
                self.moving_figure[3][1] -= 3
                self.moving_figure[0][0] += 2
                self.moving_figure[0][1] -= 1
            elif self.moving_figure[2][1] == self.moving_figure[0][1]:
                self.moving_figure[2][0] -= 2
                self.moving_figure[0][0] -= 2
                self.moving_figure[0][1] -= 2
            elif self.moving_figure[2][0] < self.moving_figure[3][0]:
                self.moving_figure[0][1] += 3
                self.moving_figure[3][0] -= 2
                self.moving_figure[3][1] += 1

        elif  self.type_of_figure == 5:
            if self.moving_figure[0][1] == self.moving_figure[1][1]:
                self.moving_figure[0][1] -= 2
                self.moving_figure[1][0] += 1
                self.moving_figure[1][1] -= 1
                self.moving_figure[3][0] += 1
                self.moving_figure[3][1] += 1
            else:
                self.moving_figure[0][1] += 2
                self.moving_figure[1][0] -= 1
                self.moving_figure[1][1] += 1
                self.moving_figure[3][0] -= 1
                self.moving_figure[3][1] -= 1

        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1

    def move_right(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0
        if not self.on_bottom():
            self.moving_figure[0][1] += 1
            self.moving_figure[1][1] += 1
            self.moving_figure[2][1] += 1
            self.moving_figure[3][1] += 1


            if self.moving_figure[0][1] == self.cols or self.moving_figure[1][1] == self.cols or \
                            self.moving_figure[2][1] == self.cols or self.moving_figure[3][1] == self.cols  or \
                self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] == 1 or \
                self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] == 1 or \
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] == 1 or \
                self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] == 1:
                self.moving_figure[0][1] -= 1
                self.moving_figure[1][1] -= 1
                self.moving_figure[2][1] -= 1
                self.moving_figure[3][1] -= 1
                self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
                self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
                self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            else:
                self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
                self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
                self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
        else:
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            #self.moving_figure, self.type_of_figure = new_figure()

    def move_left(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0

        if not self.on_bottom():
            self.moving_figure[0][1] -= 1
            self.moving_figure[1][1] -= 1
            self.moving_figure[2][1] -= 1
            self.moving_figure[3][1] -= 1
            if self.moving_figure[0][1] == -1 or self.moving_figure[1][1] == -1 or \
                    self.moving_figure[2][1] == -1 or self.moving_figure[3][1] == -1 or \
                    self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] == 1 or \
                    self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] == 1 or \
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] == 1 or \
                    self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] == 1:
                self.moving_figure[0][1] += 1
                self.moving_figure[1][1] += 1
                self.moving_figure[2][1] += 1
                self.moving_figure[3][1] += 1
                self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
                self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
                self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            else:
                self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
                self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
                self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
                self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
        else:
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            #self.moving_figure, self.type_of_figure = new_figure()

    def on_bottom(self):
        if (self.moving_figure[0][0] == self.rows - 1 or self.moving_figure[1][0] == self.rows - 1 or self.moving_figure[2][
            0] == self.rows - 1 or self.moving_figure[3][0] == self.rows - 1 or \
                        self.result[self.moving_figure[0][0] + 1][self.moving_figure[0][1]] == 1 or \
                        self.result[self.moving_figure[1][0] + 1][self.moving_figure[1][1]] == 1 or \
                        self.result[self.moving_figure[2][0] + 1][self.moving_figure[2][1]] == 1 or \
                        self.result[self.moving_figure[3][0] + 1][self.moving_figure[3][1]] == 1):
            return True
        else:
            return False

    def move_down(self):
        while self.move_figure():
            self.move_figure()
        self.end_came = not self.game_over()
        self.moving_figure, self.type_of_figure = new_figure()

    def delete_row(self):
        self.delta_speed = 0
        for i in range(self.rows):
            is_full = True
            for j in range(self.cols):
                if self.result[i][j] == 0:
                    is_full = False
            if is_full:
                self.points += 1
                self.delta_speed += 0.5
                row = i
                while (row >= 0):
                    for n in range(self.cols):
                        if row != 0:
                            self.result[row][n] = self.result[row-1][n]
                    row -= 1

    def game_over(self):
        clear = True
        for i in range(self.cols):
            if self.result[0][i] == 1:
                clear = False
        return clear



if __name__ == '__main__':
    game = TetrisGame(width=240, height=480, cell_size=20)
    game.run()