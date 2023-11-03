import pygame
from gameobject import BaseMapObject

import json

class JsonMapDecoder:

    def __init__(self) -> None:
        self.ground = BaseMapObject((50, 50))

        self.object_mapping = {
            "ground" : BaseMapObject((50, 50))
        }

        self.mapdata = None

        self.decode(f"{__file__}/mapdata/level1.json")

    def decode(self, file: str):
        with open(file, "r") as map_file:
            self.mapdata = json.load(map_file)

    def render(self, game):
        for data in self.mapdata["mapdata"]:
            new_terrian = BaseMapObject((data["x"], data["y"]))
            game.terrian_group.add(new_terrian)