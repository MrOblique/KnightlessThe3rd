import pygame

pygame.init()

selection_icon = pygame.image.load(
    "C:/Users/yaqub/PycharmProjects/PythonProject7/KnightlessMain/Images/SelectIcon.png")

class Button(): # button class
    def __init__(self, x, y, image): # takes x,y coords and image
        self.image = image # stores image
        self.rect = self.image.get_rect() # gets rect based of image
        self.rect.topleft = (x, y) # sets rect's top-left position to x,y
        self.clicked = False # initialised a button clicked to false
        self.selection_icon = pygame.transform.scale(selection_icon, ((self.rect.height / 52)* 31.5, self.rect.height))

    def draw(self, surface):
        action = False # button doesn't do anything when not pressed
        mouse_pos = pygame.mouse.get_pos() # position of mouse
        dist = self.selection_icon.get_height() # distance between selection icon and button
        if self.rect.collidepoint(mouse_pos): # checks if mouse is with self.rect
            surface.blit(self.selection_icon, (self.rect.x-dist, self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:  # left mouse button click detection
                self.clicked = True # then button has been clicked
                action = True # button does something

            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:  # left mouse button release detection
                self.clicked = False # button is no longer being clicked

        surface.blit(self.image, self.rect) # draw button using button image and rect
        return action # return True if button has been clicked (does something)

