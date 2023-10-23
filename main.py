import pygame
import json
import os

from gameobject import BaseMapObject

output = {}

image_dict = {}

path = os.path.abspath(os.path.curdir)

for file in os.listdir(path + "/image"):
    if not file.startswith("."):
        name = file.split('.')[0]
        image_dict[name] = path + "/image/" + file

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
        display_surface.blit(pygame.transform.scale(i.image, (size, size)), (i.rect.x * size, i.rect.y * size))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False
            
            if event.key == pygame.K_0:
                name = list(image_dict.keys())[0]
                print(list(image_dict.keys())[0])
                print(image_dict.keys())

            if event.key == pygame.K_1:
                name = list(image_dict.keys())[1]
                print(name)

            if event.key == pygame.K_e:
                with open("level", "w+") as map_file:
                    output = {}
                    output['level'] = "Test"
                    output['size'] = size*ratio
                    output['mapdata'] = []
                    for i in terrian_group.sprites():
                        output['mapdata'].append({"type" : i.type , "x" : i.rect.x * size * ratio , 'y' : i.rect.y * size * ratio})
                    json.dump(output, map_file, ensure_ascii = False)
                    del output

        if event.type == pygame.MOUSEMOTION:
            if event.dict['buttons'][0] or event.dict['buttons'][2]:
                pos_x, pos_y = event.dict["pos"]
                colide = False
                col_spr = None
                for i in terrian_group.sprites():
                    if i.rect.collidepoint((pos_x / size, pos_y / size)):
                        if i.type != name:
                            terrian_group.remove(i)
                            break
                        colide = True
                        col_spr = i
                        if event.dict['buttons'][2]:
                            terrian_group.remove(i)
                        break
                if (not colide and event.dict['buttons'][0]):
                    terrian_group.add(BaseMapObject((int(pos_x / size), int(pos_y / size)), image = image_dict[name]).set_type(name))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.dict)
            pos_x, pos_y = event.dict["pos"]
            colide = False
            for i in terrian_group.sprites():
                if i.rect.collidepoint((pos_x / size, pos_y / size)):
                    if i.type != name:
                        terrian_group.remove(i)
                        break
                    if event.dict['button'] == 3:
                        terrian_group.remove(i)
                        break
                    colide = True
                    break
            if not colide and event.dict['button'] == 1:
                terrian_group.add(BaseMapObject((int(pos_x / size), int(pos_y / size)), image = image_dict[name]).set_type(name))
            
