import pygame
from pygame.locals import * #importing all public names
import random


pygame.init()

clock = pygame.time.Clock()
fps = 60 #set frames per second to control the game speed

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

#define colors
white = (255, 255, 255)
black=(0,0,0)

#defining game variables and system variables
ground_scroll = 0
scroll_speed = 4
flying = False 
game_over = False
pipe_gap = 200
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0 #to keep track of the score
pass_pipe = False
game_paused = False
pause_font = pygame.font.SysFont('Bauhaus 93', 60)
#load images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png') #within the imd directory
game_over_img = pygame.image.load('img/PC _ Computer - Undertale - Miscellaneous - Game Over.png') #game over image



#function for text rendering
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function to reset our game yay!
def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height//2
    score = 0 
    return score




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
        self.clicked = False

    def update(self): #overiding an adding to the empty update function in Sprites class
        #cap the velocity to a max of 8
        # Only update bird if game is not paused
        if not game_paused:
            if flying == True:
                self.velocity += 0.5
                if self.velocity > 8:
                    self.velocity = 8
            
        

        

                
                """Over here we change the velocity(y coordinate) of the bird to simulate gravity
                and make it fall down the screen. we use our previous image rectangle stored in
                self.rect and increase its y value by the velocity calculated above"""
                if self.rect.bottom < 768:
                    self.rect.y += int(self.velocity)
            
            #jump
            if game_over == False:
            
                if pygame.mouse.get_pressed()[0] ==1 and self.clicked == False: #if left space is pressed
                    self.clicked = True
                    self.velocity = -10 #negative velocity to move the bird up
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                #print(self.velocity)
            




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

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
           self.image = pygame.transform.flip(self.image, False, True)
           self.rect.bottomleft = [x, y - int(pipe_gap//2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0: # when the pipe touches the border of the screen 
            self.kill() #you will kill the pipe using this

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos): # collides with the mouse 
            if pygame.mouse.get_pressed()[0] == 1: #collides with the mosue when mouse is being clicked
                action = True 

        #draw button 
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action 
class PauseButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (100, 100, 255)
        self.hover_color = (150, 150, 255)
        self.text_color = white
        self.font = pygame.font.SysFont('Bauhaus 93', 30)
    
    def draw(self, screen):
        # Check if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color
            
        # Draw button
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, white, self.rect, 2, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
        return self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

"""Constructing the bird and pipe GROUP using pygame GROUP using the sprite class"""
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()



"""Creating an instance of the Bird class- making the main bird sprite here!"""
flappy = Bird(100, screen_height//2) #positioning the bird at x=100 and y=middle of the screen height
"""Position bird to the right slightly and center vertically"""
bird_group.add(flappy) #adding the bird instance to the bird group

bird_group.add(flappy)

#create restart button instance
button = Button(screen_width//2 -45, screen_height//2 + 100, button_img)
# Create pause button (top right corner)
pause_button = PauseButton(screen_width - 120, 20, 100, 40, "Pause")


"""Making the game loop with WHILE"""
run = True 
while run:
    clock.tick(fps)
    #draw the background image at (0,0) which is top left corner
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pause_button.is_clicked(event):
            game_paused = not game_paused  # Toggle pause state
         # Only handle game events if not paused
        if not game_paused:
        #check if event is keydown and kescape is in event.key
            
            # ADD THIS FOR SPACEBAR
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not flying and not game_over:
                        flying = True
                    if flying and not game_over:
                        flappy.velocity = -10
            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True
    """blit function runs in the while loop endlessly"""
    screen.blit(bg, (0, 0))
    # Draw pause button (always visible)
    is_hovering = pause_button.draw(screen)
     # If game is paused, show pause screen and skip game logic
    if game_paused:
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Draw "PAUSED" text
        pause_text = pause_font.render("PAUSED", True, white)
        screen.blit(pause_text, (screen_width//2 - pause_text.get_width()//2, 
                                screen_height//2 - pause_text.get_height()//2))
        
        # Draw resume instructions
        resume_font = pygame.font.SysFont('Bauhaus 93', 30)
        resume_text = resume_font.render("Click Pause Button to Resume", True, white)
        screen.blit(resume_text, (screen_width//2 - resume_text.get_width()//2, 
                                 screen_height//2 + 60))
        
        pygame.display.update()
        continue 
    #draw the bird group, draw() is a built in sprite function
    bird_group.draw(screen)
    bird_group.update() #update the bird group to call the update method in Bird class
    pipe_group.draw(screen)
    
    #draw and scroll ground image
    screen.blit(ground, (ground_scroll, 768))

    #check the score 
    if len(pipe_group) > 0:
        #groups in pygame behave a lot like lists, you can access them with a specific index
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score +=1 
                pass_pipe = False

    draw_text("SCORE: "+str(score), font, black, int(screen_width/2.7), 20)

    #look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    #check if the bird has hit the ground
    if flappy.rect.bottom >=  768:
        game_over, flying = True, False

    
    # Only run game logic if not paused and game is active
    if not game_paused and not game_over and flying:

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100) #this is random pipe generation
            btm_pipe = Pipe(screen_width, screen_height//2 + pipe_height, -1)
            top_pipe = Pipe(screen_width, screen_height//2 + pipe_height, 1)

            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        
        #draw and scroll the ground
        ground_scroll -= scroll_speed # keep on decreasing and moving the ground to the left
        if abs(ground_scroll) > 35: #reset the ground scroll to 0 after it moves 35 pixels to left
            ground_scroll = 0
        #generate pipes
        pipe_group.update()

    #check for game over and reset
    if game_over == True:
         # Draw game over sprite 
        screen.blit(game_over_img, (screen_width//2 - game_over_img.get_width()//2, screen_height//3 - game_over_img.get_height()//2))
        
        if button.draw() == True:
            game_over = False
            score = reset_game()

    if flappy.rect.bottom >=  768:
        game_over, flying = True, False
    
    
    
    pygame.display.update()
pygame.quit()

