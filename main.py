import pygame
import json

from gameobject import BaseMapObject

object_dict = {
    type(BaseMapObject((0,0))) :  "ground"
}
output = {}

pygame.init()
pygame.display.init()

width = 1920
height = 1080

display_surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
width, height = display_surface.get_size()
display_surface.fill('white')

size = 50

editor_surface =  pygame.surface.Surface((width, height))

terrian_group = pygame.sprite.Group()

running = True

while running:
    display_surface.fill('white')
    for x in range(0, width, size):
        pygame.draw.line(display_surface, (0, 0, 0), (x, 0), (x, height))
    for y in range(0, height, size):
        pygame.draw.line(display_surface, (0, 0, 0), (0, y), (width, y))
    terrian_group.draw(display_surface)
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False

            if event.key == pygame.K_e:
                with open("level", "w+") as map_file:
                    del output
                    output = {}
                    output['level'] = "Test"
                    output['size'] = size
                    output['mapdata'] = []
                    for i in terrian_group.sprites():
                        output['mapdata'].append({"type" : object_dict[type(i)] , "x" : i.rect.x, 'y' : i.rect.y})
                    json.dump(output, map_file)

                        


        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = event.dict["pos"]
            terrian_group.add(BaseMapObject((int(pos_x / 50 ) * 50, int(pos_y / 50 ) * 50)))
            
