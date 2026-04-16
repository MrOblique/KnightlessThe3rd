import pygame  # importing the pygame library
import button  # importing the button file
import gameStates
import os

scr_width = 1280
scr_height = 720

pygame.init() # initialise pygame
clock = pygame.time.Clock()

# images

screen = pygame.display.set_mode((scr_width, scr_height)) # screen initialised to the pre-initialised values of width and height

# loading images
# the load method from the pygame library takes in the file path and the .convert_alpha() method, maintains transparency, helps improve performance.
# using the os.path method to locate the parent directory of images relative to current script and joining the directory names
computer_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "ComputerPixel.png")).convert_alpha()
play_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "PlayButton.png")).convert_alpha()
settings_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "SettingsButton.png")).convert_alpha()
exit_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "ExitButton.png")).convert_alpha()

controls_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "ControlsButton.png")).convert_alpha()
gameplay_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "Gameplay.png")).convert_alpha()
sound_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "SoundButton.png")).convert_alpha()
video_image = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "VideoButton.png")).convert_alpha()

#scroll_bar = pygame.image.load(
#    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "ScrollBar.png")).convert_alpha()
#scroll_dot = pygame.image.load(
#   os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "ScrollDot.png")).convert_alpha()
vSeperator = pygame.image.load(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "Images", "VerticalSeperator.png")).convert_alpha()

computer_image = pygame.transform.scale(computer_image, (927.5, 703))
play_image = pygame.transform.scale(play_image, (155.5, 52))
settings_image = pygame.transform.scale(settings_image, (320.5, 52))
exit_image = pygame.transform.scale(exit_image, (155.5, 52))

controls_image = pygame.transform.scale(controls_image, (160.25, 26))
gameplay_image = pygame.transform.scale(gameplay_image, (160.25, 26))
sound_image = pygame.transform.scale(sound_image, (98.5, 26))
video_image = pygame.transform.scale(video_image, (98.5, 26))

#scroll_dot = pygame.transform.scale(scroll_dot, (200, 200))
#scroll_bar = pygame.transform.scale(scroll_bar, (175, 460))
vSeperator = pygame.transform.scale(vSeperator, (100, 460))
# the rotate method takes in the image to be rotated, follow by the anti-clockwise rotation in degrees
hSeperator = pygame.transform.rotate(vSeperator, 90)
hSeperator = pygame.transform.scale(hSeperator, (345, 75))

# buttons
exit_button = button.Button(500, 350, exit_image)
play_button = button.Button(500, 150, play_image)
settings_button = button.Button(500, 210, settings_image)
exit_image = pygame.transform.scale(exit_image, (77.75, 26))
settings_exit_button = button.Button(900, 470, exit_image)
small_exit_button = button.Button(1180, 680, exit_image)
videoSettings_button = button.Button(380, 100, video_image)
gameplaySettings_button = button.Button(380, 200, gameplay_image)
soundSettings_button = button.Button(380, 300, sound_image)
controlsSettings_button = button.Button(380, 400, controls_image)

# sounds

click_sound = pygame.mixer.Sound("C:/Users/yaqub/PycharmProjects/PythonProject7/KnightlessMain/Sounds/click.mp3")
hover_sound = pygame.mixer.Sound("C:/Users/yaqub/PycharmProjects/PythonProject7/KnightlessMain/Sounds/hover.mp3")

running = True # is game running (default true)
game_state = "MainMenu" # what part of game we are on
settingsState = "VideoSettings" # Default settingsState
while running:
    dt = clock.tick()  # time between each frame

    # gamestate refreshes

    # gamestate refreshes
    # all gamestate methods are imported from the gameStates.py file,
    # taking appropiate parameters used to display their menus or displays correctly
    # key variables passed are the screen, to blit things to the same screen,
    # all gamestates return a gamestate
    if game_state == "MainMenu":  # if in main menu gamestate
        # run the main menu and check for it's return gamestate
        game_state = gameStates.mainMenu(screen, computer_image, play_button, settings_button, exit_button)
    if game_state == "Settings":  # if in settings gamestate
        # run the settings menu and check for it's return gamestate
        game_state, settingsState = gameStates.settingsMenu(screen, computer_image, settings_exit_button,
        videoSettings_button, gameplaySettings_button, soundSettings_button, controlsSettings_button,
        vSeperator, hSeperator, pygame.transform.scale(video_image, (197, 52)),
        pygame.transform.scale(gameplay_image, (320.5, 52)), pygame.transform.scale(controls_image, (320.5, 52)),
        pygame.transform.scale(sound_image, (197, 52)), settingsState)
    if game_state == "PlayMenu":
        game_state = gameStates.playMenu(screen, computer_image, play_button, settings_exit_button)
    if game_state == "Playing":
        game_state = gameStates.playing(screen, small_exit_button, dt)
    if game_state == "Paused":
            game_state = gameStates.paused(screen, small_exit_button)
    if game_state == "Quit": # if in the quit gamestate
        running = False # close game
    if game_state == "LevelSelect":
        game_state = gameStates.levelSelect(screen, computer_image, play_button, settings_exit_button)
    if game_state == "CharacterSelect":
        game_state = gameStates.characterSelect(screen, computer_image, play_button, settings_exit_button)
    # if X is pressed then close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


    # update
    pygame.display.flip()

