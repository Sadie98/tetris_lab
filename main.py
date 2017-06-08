import pygame
import pygbutton
from pygame.locals import *
import random
from pygame import mixer
import os, time
from tkinter import *

class EndOfGame:
    def __init__(self, points):
        pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.set_caption("Tetris")
        self.width = 500
        self.height = 500
        self.points = points
        self.on_pause = False
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)


    def run(self):
        pygame.init()
        white = (255, 255, 255)
        clock = pygame.time.Clock()
        #button = Button(color=white, height=15, x=30, y=30, length=40, width=15, text="NEW GAME", text_color="BLACK")
        button = Button(text="Hello")
        button.pack()

        self.screen.fill(white)
        font = pygame.font.Font(None, 25)
        black = (0, 0, 0)
        text = font.render("Game over", True, black)
        self.screen.blit(text, [50, 20])
        text = font.render("Your result: " + str(self.points), True, black)
        self.screen.blit(text, [40, 40])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                #elif 'click' in button.handleEvent(event):
                 #   print("Button pressed.")

            pygame.display.update()

        pygame.quit()



#class Button:
    # def __init__(self, surface, color, x, y, length, height, width, text, text_color):
    #     surface = self.draw_button(surface, color, length, height, x, y, width)
    #     surface = self.write_text(surface, text, text_color, length, height, x, y)
    #     self.rect = pygame.Rect(x, y, length, height)
    #     return surface
    #
    # def write_text(self, surface, text, text_color, length, height, x, y):
    #     font_size = int(length // len(text))
    #     myFont = pygame.font.SysFont("Calibri", font_size)
    #     myText = myFont.render(text, 1, text_color)
    #     surface.blit(myText,
    #                     ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
    #     return surface
    #
    # def draw_button(self, surface, color, length, height, x, y, width):
    #     for i in range(1, 10):
    #         s = pygame.Surface((length + (i * 2), height + (i * 2)))
    #         s.fill(color)
    #         alpha = (255 / (i + 2))
    #         if alpha <= 0:
    #             alpha = 1
    #         s.set_alpha(alpha)
    #         pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
    #         surface.blit(s, (x - i, y - i))
    #     pygame.draw.rect(surface, color, (x, y, length, height), 0)
    #     pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
    #     return surface
    #
    # def pressed(self, mouse):
    #     if mouse[0] > self.rect.topleft[0]:
    #         if mouse[1] > self.rect.topleft[1]:
    #             if mouse[0] < self.rect.bottomright[0]:
    #                 if mouse[1] < self.rect.bottomright[1]:
    #                     print
    #                     "Some button was pressed!"
    #                     return True
    #                 else:
    #                     return False
    #             else:
    #                 return False
    #         else:
    #             return False
    #     else:
    #         return False


class TetrisGame:
    def __init__(self, width, height, cell_size, speed = 2):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.on_pause = False
        self.screen_size = width, height
        pygame.display.set_icon(pygame.image.load("icon.png"))
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode(self.screen_size)
        mixer.init()
        self.sound_onpause = pygame.mixer.Sound('onpause.wav')
        #self.screen.set_icon()


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
                elif event.type == pygame.KEYDOWN:
                    if event.key == eval("pygame.K_DOWN") or event.key == eval("pygame.K_UP"):
                        if not self.on_pause:
                            this_cell_list.rotate()
                            this_cell_list.draw()
                            self.draw_grid()
                    if event.key == eval("pygame.K_p"):
                        if self.on_pause == True:
                            self.sound_onpause.stop()
                            this_cell_list.sound_game.play()
                            self.on_pause = False
                        else:
                            this_cell_list.sound_game.stop()
                            self.sound_onpause.play()
                            self.on_pause = True
                    if event.key == eval("pygame.K_RIGHT"):
                        if not self.on_pause:
                            this_cell_list.move_right()
                            this_cell_list.draw()
                            self.draw_grid()
                    if event.key == eval("pygame.K_LEFT"):
                        if not self.on_pause:
                            this_cell_list.move_left()
                            this_cell_list.draw()
                            self.draw_grid()
                    if event.key == eval("pygame.K_SPACE"):
                        if not self.on_pause:
                            this_cell_list.move_down()
                            this_cell_list.draw()
                            self.draw_grid()
            if not self.on_pause:
                self.speed += this_cell_list.delta_speed
                this_cell_list.delete_row()
                this_cell_list.draw()
                self.draw_grid()
                this_cell_list.update_list()
                if this_cell_list.end_came == True:
                    running = False
                pygame.display.flip()
                clock.tick(self.speed)
                pygame.display.update()
        pygame.quit()

        return this_cell_list.points


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

        #mixer.init()
        self.sound_game = pygame.mixer.Sound('tik.wav')
        self.sound_delete = pygame.mixer.Sound('fullrow.wav')
        self.sound_game_over = pygame.mixer.Sound('gameover.wav')
        self.sound_game.play()
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
            #self.end_came = not self.game_over()
            return True

        else:
            self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 1
            self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 1
            self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 1
            self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 1
            self.end_came = not self.game_over()
            return False


    def update_list(self):
        self.sound_game.stop()
        self.sound_game.play()
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
            if not self.end_came:
                self.moving_figure, self.type_of_figure = new_figure()

    def rotate(self):
        self.result[self.moving_figure[0][0]][self.moving_figure[0][1]] = 0
        self.result[self.moving_figure[1][0]][self.moving_figure[1][1]] = 0
        self.result[self.moving_figure[2][0]][self.moving_figure[2][1]] = 0
        self.result[self.moving_figure[3][0]][self.moving_figure[3][1]] = 0
        if self.type_of_figure == 1:
            if self.moving_figure[0][0] == self.moving_figure[1][0]:
                if  self.result[self.moving_figure[0][0] - 2][self.moving_figure[0][1] + 2] == 0 and \
                    self.result[self.moving_figure[1][0] - 1][self.moving_figure[1][1] + 1] == 0 and \
                    self.result[self.moving_figure[3][0] + 1][self.moving_figure[3][1] - 1] == 0:
                    self.moving_figure[0][0] -= 2
                    self.moving_figure[0][1] += 2
                    self.moving_figure[1][0] -= 1
                    self.moving_figure[1][1] += 1
                    self.moving_figure[3][0] += 1
                    self.moving_figure[3][1] -= 1
            elif self.result[self.moving_figure[0][0] + 2][self.moving_figure[0][1] - 2] == 0:
                if  self.result[self.moving_figure[1][0] + 1][self.moving_figure[1][1] - 1] == 0 and \
                    self.result[self.moving_figure[3][0] - 1][self.moving_figure[3][1] + 1] == 0:
                    self.moving_figure[0][0] += 2
                    self.moving_figure[0][1] -= 2
                    self.moving_figure[1][0] += 1
                    self.moving_figure[1][1] -= 1
                    self.moving_figure[3][0] -= 1
                    self.moving_figure[3][1] += 1


        elif self.type_of_figure == 2:
            if self.moving_figure[0][0] == self.moving_figure[2][0]:
                if self.result[self.moving_figure[0][0] + 1][self.moving_figure[0][1] + 1] == 0:
                    self.moving_figure[0][0] += 1
                    self.moving_figure[0][1] += 1
            elif self.moving_figure[3][1] == self.moving_figure[0][1]:
                if self.result[self.moving_figure[3][0] + 1][self.moving_figure[3][1] - 1] == 0:
                    self.moving_figure[3][0] += 1
                    self.moving_figure[3][1] -= 1
            elif self.moving_figure[3][0] == self.moving_figure[2][0]:
                if self.result[self.moving_figure[2][0] - 1][self.moving_figure[2][1] - 1] == 0:
                    self.moving_figure[2][0] -= 1
                    self.moving_figure[2][1] -= 1
            elif  self.result[self.moving_figure[0][0] - 1][self.moving_figure[0][1] - 1] == 0:
                if self.result[self.moving_figure[2][0] + 1][self.moving_figure[2][1] + 1] == 0  and \
                    self.result[self.moving_figure[3][0] - 1][self.moving_figure[3][1] + 1] == 0:
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
                if self.result[self.moving_figure[3][0] + 2][self.moving_figure[3][1] + 2] == 0  and \
                    self.result[self.moving_figure[2][0] + 2][self.moving_figure[2][1]] == 0:
                    self.moving_figure[3][0] += 2
                    self.moving_figure[3][1] += 2
                    self.moving_figure[2][0] += 2
            elif self.moving_figure[0][0] == self.moving_figure[2][0] - 1:
                if self.result[self.moving_figure[3][0]][self.moving_figure[3][1] - 3] == 0  and \
                    self.result[self.moving_figure[0][0] + 2][self.moving_figure[0][1] - 1] == 0:
                    self.moving_figure[3][1] -= 3
                    self.moving_figure[0][0] += 2
                    self.moving_figure[0][1] -= 1
            elif self.moving_figure[2][1] == self.moving_figure[0][1]:
                if self.result[self.moving_figure[2][0] - 2][self.moving_figure[2][1]] == 0  and \
                    self.result[self.moving_figure[0][0] - 2][self.moving_figure[0][1] - 2] == 0:
                    self.moving_figure[2][0] -= 2
                    self.moving_figure[0][0] -= 2
                    self.moving_figure[0][1] -= 2
            elif self.moving_figure[2][0] < self.moving_figure[3][0]:
                if self.result[self.moving_figure[0][0]][self.moving_figure[0][1] + 3] == 0  and \
                    self.result[self.moving_figure[3][0] - 2][self.moving_figure[3][1] + 1] == 0:
                    self.moving_figure[0][1] += 3
                    self.moving_figure[3][0] -= 2
                    self.moving_figure[3][1] += 1

        elif  self.type_of_figure == 5:
            if self.moving_figure[0][1] == self.moving_figure[1][1]:
                if self.result[self.moving_figure[0][0]][self.moving_figure[0][1] - 2] == 0  and \
                    self.result[self.moving_figure[1][0] + 1][self.moving_figure[1][1] - 1] == 0 and \
                    self.result[self.moving_figure[3][0] + 1][self.moving_figure[3][1] + 1] == 0:
                    self.moving_figure[0][1] -= 2
                    self.moving_figure[1][0] += 1
                    self.moving_figure[1][1] -= 1
                    self.moving_figure[3][0] += 1
                    self.moving_figure[3][1] += 1
            elif self.result[self.moving_figure[0][0]][self.moving_figure[0][1] + 2] == 0:
                if self.result[self.moving_figure[1][0] - 1][self.moving_figure[1][1] + 1] == 0 and \
                    self.result[self.moving_figure[3][0] - 1][self.moving_figure[3][1] - 1] == 0:
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
                self.sound_game.stop()
                self.sound_delete.play()

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
        if not clear:
            self.sound_game.stop()
            self.sound_game_over.play()
            time.sleep(4)
        return clear



if __name__ == '__main__':
    game = TetrisGame(width=240, height=480, cell_size=20)
    points = game.run()
    EndOfGame = EndOfGame(12)
    EndOfGame.run()