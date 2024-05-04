import pymunk
from pymunk import Vec2d
from pymunk.pygame_util import *

import pygame
from pygame.locals import *
from time import time

import random
import os.path
import math

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

pymunk.pygame_util.positive_y_is_up = False
class App():
    def __init__(self):
        #параметры PyGame
        self.RES = self.WIDTH, self.HEIGHT = 900, 720
        self.FPS = 60

        pygame.init()
        self.surface = pygame.display.set_mode(self.RES)
        self.surface.set_alpha(128)
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)

        #настройки Pymunk
        self.space = pymunk.Space()
        self.space.gravity = 0, 2500
        self.circles_list = []
        self.list_size = [15]
        self.offset_circle = 0
        self.bg = pygame.image.load('background.png').convert()
        self.big_x = pygame.image.load('big_x.png').convert()

    def

    def slab(self):
        #платформа
        segment_shape = pymunk.Segment(self.space.static_body, (2, self.HEIGHT), (self.WIDTH, self.HEIGHT), 26)
        self.space.add(segment_shape)
        segment_shape.elasticity = 0
        segment_shape.friction = 1

        bebra_shape = pymunk.Segment(self.space.static_body, (2, 1), (2, 900), 26)
        self.space.add(bebra_shape)
        bebra_shape.elasticity = 0
        bebra_shape.friction = 1

        be_shape = pymunk.Segment(self.space.static_body, (625, 1), (625, 900), 26)
        self.space.add(be_shape)
        be_shape.elasticity = 0
        be_shape.friction = 1

        b_shape = pymunk.Segment(self.space.static_body, (900, 1), (900, 900), 26)
        self.space.add(b_shape)
        b_shape.elasticity = 0
        b_shape.friction = 1

    def draw_background(self):
        self.surface.blit(self.bg, (0, 0))
        self.surface.blit(self.big_x, (690,530))



    def create_circle(self,pos, size, image_name):

        if self.offset_circle == 0:
            pos_list = [pos[0]-0.1, pos[1]-0.1]
            self.offset_circle = 1
        elif self.offset_circle == 1:
            pos_list = [pos[0] + 0.1, pos[1] + 0.1]
            self.offset_circle = 0
        self.circle_mass = 1
        self.circle_moment = pymunk.moment_for_circle(self.circle_mass,30,30)
        self.circle_body = pymunk.Body(self.circle_mass, self.circle_moment)
        self.circle_body.position = pos_list
        self.circle_shape = pymunk.Circle(self.circle_body, size)
        self.circle_shape.elasticity = 0.4
        self.circle_shape.friction = 1
        self.circle_shape.color = [255,255,255,0]
        self.circles_list.append((self.circle_shape, image_name))
        self.space.add(self.circle_body,self.circle_shape)







#Отрисовка
    def main(self):

        # Store the last rotation angle for each circle
        last_rotation_angles = {}
        size = 15
        start = time()
        amount_placed = 0

        self.slab()
        while True:

            self.draw_background()

            self.space.step(1 / self.FPS)
            self.space.debug_draw(self.draw_options)

            for circle_shape, image_name in self.circles_list:
                # Calculate the position for the image
                p = Vec2d(circle_shape.body.position.x, circle_shape.body.position.y)

                # Calculate the current rotation angle
                angle_degrees = math.degrees(circle_shape.body.angle) + 180

                # Invert the rotation direction
                angle_degrees *= -1

                # Load the image based on the size of the ball
                image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), image_name)
                image = pygame.image.load(image_path)

                scale_factor = circle_shape.radius / 15

                # Scale the image based on the scaling factor
                scaled_image = pygame.transform.scale(image, (
                    int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

                # Rotate the image to match the circle's orientation
                rotated_image = pygame.transform.rotate(scaled_image, angle_degrees)

                # Calculate the offset to center the image on the circle
                offset = Vec2d(*rotated_image.get_size()) / 2
                p = p - offset

                # Draw the image on the surface
                self.surface.blit(rotated_image, (round(p.x), round(p.y)))

                # Update the last rotation angle
                last_rotation_angles[circle_shape] = angle_degrees

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    end = time()
                    print(i.pos)
                    if end - start >= 0.4:
                        if i.button == 1 and (i.pos[0])+size <= 600 and (i.pos[0])-size >= 30 and i.pos[1] <= 200:
                            # Determine the image name based on the size of the ball
                            if size == 15:
                                image_name = "image1.png"
                            elif size == 17.5:
                                image_name = "image2.png"
                            elif size == 22.5:
                                image_name = "image3.png"
                            amount_placed += 1
                            self.create_circle(i.pos, size, image_name)
                            size = self.list_size[random.randint(0, len(self.list_size)-1)]
                            print(i.pos)
                            start = time()
                            if amount_placed == 10:
                                self.list_size.append(17.5)
                            elif amount_placed == 5:
                                self.list_size.append(22.5)
                    if i.button == 1 and i.pos[0]>=690 and i.pos[0]<=840 and i.pos[1]>=530 and i.pos[1]<=680:
                        exit()


            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    app = App()
    app.main()