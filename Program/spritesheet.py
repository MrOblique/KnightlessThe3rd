import pygame
import json

#Spritesheet class
class Spritesheet:
    def __init__(self, filename): #filepath as parameter
        self.filename = filename #stores file path
        self.sprite_sheet = pygame.image.load(filename) #loads and saves it as image
        self.meta_data = self.filename.replace("png", "json") #replaces the end of the spritesheet, png, with json
        with open(self.meta_data) as f: # abbreviate meta_data to f
            self.data = json.load(f) # load the file into self.data
        f.close() # close the file to ensure that it is saved

    def get_sprite(self, x, y, width, height): #takes in x,y positions and width,height of sprite on the sprite sheet
        sprite = self.sprite_sheet.subsurface((x, y, width, height)) # creates a sprite using a part of the spritesheet
        sprite = pygame.transform.scale(sprite,(256,256)) # scaling the sprites
        return sprite

    def parse_sprite(self, name, frame_number):
        # name is the name of attack fram in metadata
        name = name + "-" + str(frame_number)
        sprite = self.data["frames"][name]["frame"]
        x,y,width,height = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        # uses get method to return the frame of the sprite
        image = self.get_sprite(x, y, width, height)
        return image