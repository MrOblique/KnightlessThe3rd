import pygame
import game
from entities import Level1
from entities import player # player object
from game import all_sprites
from game import enemies # all enemy objects
from game import projectiles # all active projectile objects

def mainMenu(screen, computer_image, play_button, settings_button, exit_button):
    screen.fill("Black") # fill bg black
    screen.blit(computer_image, (200,10)) # draw computer bg
    action = play_button.draw(screen) # draw and check return of play button
    if action:
        return "LevelSelect"
    action = settings_button.draw(screen) # draw and check return of settings button
    if action:
        print("Settings")
        return "Settings" # return the settings gamestate
    action = exit_button.draw(screen) # draw and check return of exit button
    if action:
        print("Exit")
        return "Quit" # return the quit gamestate
    return "MainMenu" # return the current gamestate by default

def settingsMenu(screen, computer_image, exit_button, videoSettings_button, gameplaySettings_button,
soundSettings_button, controlsSettings_button, vSeperator, hSeperator,
video_image, gameplay_image, controls_image, sound_image, settingsState):
    screen.fill("Black") # fill bg black
    screen.blit(computer_image, (200,10)) # draw computer bg

    #settings state checker to blit settings state title and display settings
    if settingsState == "VideoSettings":
        screen.blit(video_image, (700, 100))
    elif settingsState == "GameplaySettings":
        screen.blit(gameplay_image, (645, 100))
    elif settingsState == "ControlsSettings":
        screen.blit(controls_image, (645, 100))
    elif settingsState == "SoundSettings":
        screen.blit(sound_image, (700, 100))

    action = videoSettings_button.draw(screen)
    if action:
        print("VideoSettings")
        settingsState = "VideoSettings" # set settingsState to VideoSettings
    action = gameplaySettings_button.draw(screen)
    if action:
        print("GameplaySettings")
        settingsState = "GameplaySettings" # set settingsState to GameplaySettings
    action = soundSettings_button.draw(screen)
    if action:
        print("SoundSettings")
        settingsState = "SoundSettings" # set settingsState to SoundSettings
    action = controlsSettings_button.draw(screen)
    if action:
        print("ControlsSettings")
        settingsState = "ControlsSettings" # set settingsState to ControlsSettings

    action = exit_button.draw(screen) # draw and check return of exit button
    if action:
        print("Exit")
        return "MainMenu", "VideoSettings" # return the mainmenu gamestate

    screen.blit(vSeperator, (520, 59)) # draw vertical seperator
    screen.blit(hSeperator, (630, 145)) # draw horizontal seperator

    return "Settings", settingsState # return the current gamestate by default

def playMenu(screen, computer_image, play_button, exit_button):
    screen.fill("Black")
    screen.blit(computer_image, (200, 10))
    action = play_button.draw(screen) # draw and check return of play button
    if action:
        return "Playing"
    action = exit_button.draw(screen) # draw and check return of exit button
    if action:
        print("Exit")
        return "MainMenu"
    return "PlayMenu"


def playing(screen, exit_button, dt):
    game_state = "Playing"
    screen.fill("Black") # fill bg black
    Level1.draw(screen)
    key_pressed = pygame.key.get_pressed() # returns the states of all the keys
    mouse_pressed = pygame.mouse.get_pressed() # returns the states of all the mouse buttons
    state = all_sprites.update(key_pressed, mouse_pressed, Level1.tiles, player, screen, dt) # updates all sprites
    if state == "Dead":
        pass
    if key_pressed[pygame.K_p]:
        game_state = "Paused"
    # check collisions
    print(projectiles)
    game.hCollisionHandler(player, enemies, projectiles)
    # draw all sprites
    for sprite in all_sprites:
        sprite.draw(screen)
    action = exit_button.draw(screen) # draw and check return of exit button
    print(f"X-coords : {player.getProperties()[0]}, Y-coords : {player.getProperties()[1]}")
    if action:
        print("Exit")
        return "PlayMenu"
    return game_state # return playing gamestate

def paused(screen, exit_button):
    action = exit_button.draw(screen)  # draw and check return of exit button
    key_pressed = pygame.key.get_pressed()  # returns the states of all the keys
    if key_pressed[pygame.K_o]:
        return "Playing"
    if action:
        print("Exit")
        return "Playing"
    return "Paused"

def levelSelect(screen, computer_image, play_button, exit_button):
    screen.fill("Black")
    screen.blit(computer_image, (200, 10))
    levels = pygame.Rect(415,200, 500, 200)
    pygame.draw.rect(screen, (255,255,255), levels)
    action = play_button.draw(screen)  # draw and check return of play button
    if action:
        return "CharacterSelect"
    action = exit_button.draw(screen)  # draw and check return of exit button
    if action:
        print("Exit")
        return "MainMenu"
    return "LevelSelect"

def characterSelect(screen, computer_image, play_button, exit_button):
    screen.fill("Black")
    screen.blit(computer_image, (200, 10))
    action = play_button.draw(screen)  # draw and check return of play button
    if action:
        return "Playing"
    action = exit_button.draw(screen)  # draw and check return of exit button
    if action:
        print("Exit")
        return "MainMenu"
    return "CharacterSelect"
