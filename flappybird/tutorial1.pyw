import pygame
from pygame.locals import * #importing all public names

pygame.init()

clock = pygame.time.Clock()
fps = 60 #set frames per second to control the game speed

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird')

#defining game variables
ground_scroll = 0
scroll_speed = 4
flying = False 
game_over = False

#load images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')




class Bird(pygame.sprite.Sprite): #draws upon an existing class Sprite from pygame library
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #Sprite class initizalization *THEY ALREADY HAVE INBUILT SPRITE FUNCTION* we are INHERITING from that!
        self.images = [] #list to hold multiple images for animation
        self.index = 0 #indexer to keep track of the current image index
        self.counter = 0 #counter to control the speed at which the animation RUNS/CYCLES whateverrrr
        for num in range(3):
            image = self.image = pygame.image.load(f'img/bird{num+1}.png')
            self.images.append(image) #append each loaded image to the images list
        
        self.image = self.images[self.index] #set the current image to the first image in the list 
        self.rect = self.image.get_rect() #get the rectangle area of the image, create a rect from the BOUNDARIES OF bird image
        self.rect.center = [x, y] #set the center of the rectangle to the x and y passed as arguments during instantiation
        self.velocity = 0 #fancy word for how fast the y value increases and all


    def update(self, keys): #overiding an adding to the empty update function in Sprites class
        #cap the velocity to a max of 8
        if flying == True:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
        
        #jump
        if pygame.K_SPACE in keys: #if space key is pressed
            self.velocity = -10 #negative velocity to move the bird up
            self.press = True

    

        print(self.velocity)
        """Over here we change the velocity(y coordinate) of the bird to simulate gravity
        and make it fall down the screen. we use our previous image rectangle stored in
        self.rect and increase its y value by the velocity calculated above"""

        self.rect.y += int(self.velocity) if self.rect.bottom < 768 else 0
        
        if game_over == False:
            #jump
            if keys[pygame.K_SPACE]: #if left mouse button is pressed
                self.velocity = -10 #negative velocity to move the bird up
            
            print(self.velocity)
            




            #handling the animation, using counter which  countrols the animation cycle
            self.counter += 1 #increment by one everytime update is called
            flap_cool = 5

            if self.counter > flap_cool:
                self.counter = 0 #reset counter
                self.index += 1  #move to the next image index
                self.index = 0 if self.index > 2 else self.index #reset index to 0 if it exceeds 2 (since we have 3 images indexed 0,1,2)
            self.image = self.images[self.index] #update the current image to the new index  

            #rotate the bird based on its position
            self.image = pygame.transform.rotate(self.images[self.index], -self.velocity * 2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

"""Constructing the bird GROUP using pygame GROUP using the sprite class"""
bird_group = pygame.sprite.Group()

"""Creating an instance of the Bird class- making the main bird sprite here!"""
flappy = Bird(100, screen_height//2) #positioning the bird at x=100 and y=middle of the screen height
"""Position bird to the right slightly and center vertically"""
bird_group.add(flappy) #adding the bird instance to the bird group





"""Making the game loop with WHILE"""
run = True 
while run:
    #draw the background image at (0,0) which is top left corner
    screen.blit(bg, (0, 0))
    #draw the bird group, draw() is a built in sprite function
    bird_group.draw(screen)
    bird_group.update(pygame.key.get_pressed()) #update the bird group to call the update method in Bird class
    #draw and scroll ground image
    screen.blit(ground, (ground_scroll, 768))
    clock.tick(fps) # here we use fps to ontrol the game speed in loop

    if flappy.rect.bottom >=  768:
        game_over, flying = False, False

    if not game_over:
        ground_scroll -= scroll_speed # keep on decreasing and moving the ground to the left
        if abs(ground_scroll) > 35: #reset the ground scroll to 0 after it moves 35 pixels to left
            ground_scroll = 0
    
    #handle the loop run with event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True 

    
    
    pygame.display.update()
pygame.quit()

