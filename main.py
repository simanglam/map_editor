import pygame
import json
import os

from gameobject import BaseMapObject
from scene import AbScene, SelectScene, EditorScene


class game:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.scene: AbScene = EditorScene(self)
        self.prev_scene = None
        self.running = True
        self.clock = pygame.time.Clock()

    def change_scene(self, new_scene: AbScene):
        new = new_scene(self)
        new.on_enter(self.scene)
        self.scene.on_exit(new) 

    def run(self):
        while self.running:
            self.screen.fill('white')
            self.scene.update()
            self.screen.blit(self.scene.screen, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)

main_game = game()

main_game.run()