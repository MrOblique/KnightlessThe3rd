import game
import pygame
import tilemap # to draw level
import os
from spritesheet import Spritesheet # to draw sprite animations

pygame.init()

#(index,animation)
knight_anims = []
# (0,Attack1), (1,Attack2), (2,Attack3), (3,Dead), (4,Hurt), (5,Idle), (6,Jump), (7,Run), (8,Walk)
gangster_melee_anims = []
# (0,Attack1), (1,Dead), (2,Hurt), (3,Idle), (4,Run), (5,Walk)
gangster_ranged_anims = []
# (0,Dead), (1,Hurt), (2,Idle), (3,Run), (4,Shoot), (5,Walk)

# Knight anims
for (path,_,i) in os.walk(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Knight")):
    for file in i:
        if ".png" in file:
            # creates spritesheet object which passes the ".png" spritesheet using the os library to trace the path
            mySpritesheet = Spritesheet(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Knight", file))
            image = pygame.image.load(os.path.join(path, file))
            w = image.get_width()
            # parses sprites from spritesheets, creates list, extends list for each animation with each frame using list comprehension
            knight_anims.append([mySpritesheet.parse_sprite(file.removesuffix(".png"), frame_number) for frame_number in range(int(w/128))])
# Melee gangster anims
for (path,_,i) in os.walk(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Gangster", "Melee")):
    for file in i:
        if ".png" in file:
            # creates spritesheet object which passes the ".png" spritesheet using the os library to trace the path
            mySpritesheet = Spritesheet(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Gangster", "Melee", file))
            image = pygame.image.load(os.path.join(path, file))
            w = image.get_width()
            # parses sprites from spritesheets, creates list, extends list for each animation with each frame using list comprehension
            gangster_melee_anims.append([mySpritesheet.parse_sprite(file.removesuffix(".png"), frame_number) for frame_number in range(int(w/128))])
# Ranged gangster anims
for (path,_,i) in os.walk(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Gangster", "Ranged")):
    for file in i:
        if ".png" in file:
            # creates spritesheet object which passes the ".png" spritesheet using the os library to trace the path
            mySpritesheet = Spritesheet(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Gangster", "Ranged", file))
            image = pygame.image.load(os.path.join(path, file))
            w = image.get_width()
            # parses sprites from spritesheets, creates list, extends list for each animation with each frame using list comprehension
            gangster_ranged_anims.append([mySpritesheet.parse_sprite(file.removesuffix(".png"), frame_number) for frame_number in range(int(w/128))])
print(knight_anims)
print(len(knight_anims))
#creating both the player object and enemy object

player = game.Knight(knight_anims)
ranged_gangster = game.GangsterRanged(gangster_ranged_anims)
melee_gangster = game.GangsterMelee(gangster_melee_anims)

# Level Design
# sort of like an encryption variable
o1 = "00000000000000000000000000000000"
o2 = "0000000000000000"
o3 =  "00000000"
i1 = "11111111111111111111111111111111"
i2 = "1111111111111111"

level = []

for i in range(18):
    # fill top of level with air
    if i < 10:
        level.append(o1)
    if i == 10:
        level.append("00111111000000000000000011111100")
    if i == 11:
        level.append(o1)
    if i == 12:
        level.append(o1)
    if i == 13:
        level.append("00000000001111111111110000000000")
    if i == 14:
        level.append("00000000011111111111111000000000")
    # add a hump to the floor in the middle
    if i == 15:
        level.append(o3+i2+o3)
    elif i > 15:
    # fill floor with tiles
        level.append(i1)

Level1 = tilemap.TileMap(level)
