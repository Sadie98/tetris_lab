import os, time, pygame
from pygame.locals import *


class ResManager:
    def __init__(self,
                 data_dir = 'data',
                 image_dir = 'image',
                 sound_dir = 'sound',):
        self.data_dir = data_dir
        self.image_dir = image_dir
        self.sound_dir = sound_dir

    def get_image(self, name):
        fullname = os.path.join(self.data_dir,
                                os.path.join(self.image_dir, name))

        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image: {0}'.format(name))
            raise SystemExit(message)
        else:
            image = image.convert_alpha()
            return image
