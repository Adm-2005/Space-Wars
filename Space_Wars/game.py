import pygame, sys, os, random, math

from pygame.locals import *
from utils import load_sprite, get_random_position, print_text
from models import spaceShip, Asteroid, Bullet

class SpaceWars():
    MIN_ASTEROID_DISTANCE = 250
    def __init__(self):
        self._init_pygame()

        #global variables for game
        self.Width = 800
        self.Height = 600
        self.time = 0
        self.fps = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.Width,self.Height),0,32)
        self.font = pygame.font.Font(None, 100)
        self.message = ""

        #loading sprites
        self.background = load_sprite("bg",False)
        self.debris = load_sprite("debris",True)
        
        #defining objects
        self.bullets = []
        self.ship = spaceShip((400,300), self.bullets.append)
        self.asteroids = []

        for _ in range(5):
            while True:
                position = get_random_position(self.window)
                if (
                    position.distance_to(self.ship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position))

    def title_loop(self):
        #TO-DO = Add title screen
        pass

    def main_loop(self):
        while True:
            self._draw()
            self._handle_input()
            self._game_logic()
            self.update_screen()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption('Space Wars')

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif (
                self.ship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.ship.shoot()

            if self.ship:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_LEFT:
                        self.ship.rotate(clockwise=False,stop=False)
                    elif event.key == K_RIGHT:
                        self.ship.rotate(clockwise=True, stop=False)
                    if event.key == K_UP:
                        self.ship.accelerate(deaccelerate=False)

                elif event.type == pygame.KEYUP:
                    if event.key == K_LEFT:
                        self.ship.rotate(clockwise=False,stop=True)
                    elif event.key == K_RIGHT:
                        self.ship.rotate(clockwise=True, stop=True)
                    elif event.key == K_UP:
                        self.ship.accelerate(deaccelerate=True)

    def _game_logic(self):
        for game_object in self._get_game_objects():
            game_object.motion(self.window)

        if self.ship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.ship):
                    self.ship = None
                    self.message = "You Lost!"
                    break

        if not self.asteroids and self.ship:
            self.message = "You Won!"
        
        for bullet in self.bullets[:]:
            if not self.window.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)   

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    break         

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.ship:
            game_objects.append(self.ship)

        return game_objects

    def _draw(self):
        self.window.blit(self.background,(0,0))
        self.window.blit(self.debris,(self.time*.3,0))
        self.window.blit(self.debris,(self.time*.3-self.Width,0))

        for game_object in self._get_game_objects():
            game_object.draw(self.window)
        
        if self.message:
            print_text(self.window, self.message, self.font)

        self.time += 1
        pygame.display.flip()

    def update_screen(self):
        pygame.display.update()
        self.fps.tick(60)


