import pygame, json
pygame.init()
class BaseMapObject(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		self.image = pygame.surface.Surface((50, 50))
		self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
		self.image.fill("black")
		

running = True
terrain_group = []
display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
output = {}
type_dict = {
	type(BaseMapObject(0, 0)) : "ground"
}

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e:
				output['level'] = "Test"
				output['size'] = 50
				output['mapdata'] = []
				for block in terrain_group:
					output['mapdata'].append({"x" : block.rect.x, "y" : block.rect.y, "type" : type_dict[type(block)]})
				with open("level.json", "w+") as f:
					json.dump(output, f)
			if event.key == pygame.K_ESCAPE:
				running = False
				pygame.quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos_x, pos_y = event.dict["pos"]
			collide = False
			for block in terrain_group:
				if block.rect.collidepoint((pos_x, pos_y)):
					collide = True
					break

			if not collide:
				terrain_group.append(BaseMapObject(int(pos_x / 50) * 50, int(pos_y / 50) * 50))



		
	display_surface.fill('white')
	for block in terrain_group:
		display_surface.blit(block.image, block.rect)
	pygame.display.update()



