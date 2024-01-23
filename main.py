import pygame
import sys
from engine.config import *
from engine.map import *
from engine.player import *
from engine.ray import *
from engine.object_renderer import *
from engine.sprite_object import *
from engine.object_handler import *
from engine.weapon import *
from engine.audio import *
from engine.pathfinding import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(RES)
        pygame.event.set_grab(True)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        try:
            self.sound = Sound(self)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print("Warning: Unable to initialize audio. The game will continue without sound.")
            self.sound = None
        self.pathfinding = PathFinding(self)
        

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        
        self.object_renderer.draw()
        self.weapon.draw()
        

    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()