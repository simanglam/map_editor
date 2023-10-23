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
mode = 'edit'
display_surface = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
width, height = display_surface.get_size()
display_surface.fill('white')

size = 25

ratio = 2

editor_surface =  pygame.surface.Surface((width, height))

terrian_group = pygame.sprite.Group()

running = True

while running:
    display_surface.fill('white')
    for x in range(0, width, size):
        pygame.draw.line(display_surface, (0, 0, 0), (x, 0), (x, height))
    for y in range(0, height, size):
        pygame.draw.line(display_surface, (0, 0, 0), (0, y), (width, y))
    for i in terrian_group:
        display_surface.blit(pygame.transform.scale(i.image, (25, 25)), (i.rect.x * size, i.rect.y * size))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False

            if event.key == pygame.K_e:
                with open("level", "w+") as map_file:
                    output = {}
                    output['level'] = "Test"
                    output['size'] = size*ratio
                    output['mapdata'] = []
                    for i in terrian_group.sprites():
                        output['mapdata'].append({"type" : object_dict[type(i)] , "x" : i.rect.x * size * ratio , 'y' : i.rect.y * size * ratio})
                    json.dump(output, map_file)
                    del output

    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = event.dict["pos"]
            colide = False
            for i in terrian_group.sprites():
                if i.rect.collidepoint((pos_x / size, pos_y / size)):
                    colide = True
                    break
            if not colide:
                terrian_group.add(BaseMapObject((int(pos_x / size), int(pos_y / size))))


        if event.type == pygame.MOUSEMOTION:
            if event.dict['buttons'][0]:
                pos_x, pos_y = event.dict["pos"]
                colide = False
                for i in terrian_group.sprites():
                    if i.rect.collidepoint((pos_x / size, pos_y / size)):
                        colide = True
                        break
                if not colide:
                    terrian_group.add(BaseMapObject((int(pos_x / size), int(pos_y / size))))
    
                
            
