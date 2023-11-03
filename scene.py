import os
import json
import pygame

from gameobject import BaseMapObject

class AbScene:

    def __init__(self, game):
        self.game = game
        self.screen = pygame.surface.Surface(self.game.screen.get_size())
        self.width, self.height = self.screen.get_size()

    def on_enter(self, old_scene):
        pass

    def on_exit(self, new_scene):
        self.game.prev_scene = self
        self.game.scene = new_scene

    def update(self):
        pass

class SelectScene(AbScene):

    def __init__(self, game):
        super().__init__(game)
        self.selection_list: [BaseMapObject] = []

    def on_enter(self, old_scene):
        image_list = list(old_scene.image_dict.keys())
        y = 50
        for option in image_list:
            self.selection_list.append(BaseMapObject((2, y // 50), "./image/" + option + ".png").set_type(option))
            y += 100


    def on_exit(self, new_scene):
        self.game.scene = self.game.prev_scene
        self.game.prev_scene = None

    def render(self):
        self.screen.fill('white')
        for i in self.selection_list:
            self.screen.blit(i.image, (i.rect.x * 50, i.rect.y * 50))


    def update(self):
        self.render()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                    pygame.quit()
                    exit(0)

                elif event.key == pygame.K_s:
                    self.on_exit(EditorScene)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in self.selection_list:
                    if i.rect.collidepoint((x / 50, y / 50)):
                        self.game.prev_scene.name = i.type
                        self.on_exit(EditorScene)



class EditorScene(AbScene):

    def __init__(self, game):
        super().__init__(game)

        self.size = 25
        self.ratio = 50 / self.size
        self.terrian_group = pygame.sprite.Group()
        self.image_dict = {}
        path = __file__

        for file in os.listdir(path + "/image"):
            if not file.startswith("."):
                name = file.split('.')[0]
                self.image_dict[name] = path + "/image/" + file

        self.name = list(self.image_dict.keys())[0]

    def render(self):
        self.screen.fill('white')
        for x in range(0, self.width, self.size):
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, self.size):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y))
        for i in self.terrian_group:
            self.screen.blit(pygame.transform.scale(i.image, (i.image.get_width() / self.ratio, i.image.get_height() / self.ratio)), (i.rect.x * self.size, i.rect.y * self.size))

    def update(self):
        self.render()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                    pygame.quit()
                    exit(0)

                if event.key == pygame.K_s:
                    self.game.change_scene(SelectScene)
                
                if event.key == pygame.K_0:
                    self.name = list(self.image_dict.keys())[0]
                    print(list(self.image_dict.keys())[0])
                    #print(self.image_dict.keys())

                if event.key == pygame.K_1:
                    self.name = list(self.image_dict.keys())[1]

                if event.key == pygame.K_e:
                    with open("level.json", "w+") as map_file:
                        output = {}
                        output['level'] = "Test"
                        output['size'] = self.size * self.ratio
                        output['mapdata'] = []
                        for i in self.terrian_group.sprites():
                            output['mapdata'].append({"type" : i.type , "x" : i.rect.x * self.size * self.ratio , 'y' : i.rect.y * self.size * self.ratio})
                        json.dump(output, map_file, ensure_ascii = False)
                        del output

            if event.type == pygame.MOUSEMOTION:
                if event.dict['buttons'][0] or event.dict['buttons'][2]:
                    pos_x, pos_y = event.dict["pos"]
                    colide = False
                    col_spr = None
                    for i in self.terrian_group.sprites():
                        if i.rect.collidepoint((pos_x / self.size, pos_y / self.size)):
                            if i.type != self.name:
                                self.terrian_group.remove(i)
                                break
                            colide = True
                            col_spr = i
                            if event.dict['buttons'][2]:
                                self.terrian_group.remove(i)
                            break
                    if (not colide and event.dict['buttons'][0]):
                        self.terrian_group.add(BaseMapObject((int(pos_x / self.size), int(pos_y / self.size)), image = self.image_dict[self.name]).set_type(self.name))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.dict)
                pos_x, pos_y = event.dict["pos"]
                print(pos_x / self.size, pos_y / self.size)
                colide = False
                for i in self.terrian_group.sprites():
                    if i.rect.collidepoint((pos_x / self.size, pos_y / self.size)):
                        print(i.rect)
                        if i.type != self.name:
                            self.terrian_group.remove(i)
                            break
                        if event.dict['button'] == 3:
                            self.terrian_group.remove(i)
                            break
                        colide = True
                        break
                if not colide and event.dict['button'] == 1:
                    self.terrian_group.add(BaseMapObject((int(pos_x / self.size), int(pos_y / self.size)), image = self.image_dict[self.name]).set_type(self.name))