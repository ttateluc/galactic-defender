#key codes, mouse codes, event types, etc.
import pygame
import sys
from pygame.locals import *
import random
import math
from pygame import mixer

clock = pygame.time.Clock() # regulates the game's framerate
pygame.init() # initializes pygame


windowSize = 1920,1080 # fullscreen resolution
window = pygame.display.set_mode((windowSize), pygame.FULLSCREEN|SCALED, vsync=1) # fullscreen, scale-to-fit, sync to monitor's refresh rate

# icons
icon = pygame.image.load('assets/icon.png').convert_alpha()  # game logo load optimization (convert_alpha() is used to optimize the image's transparency)
pygame.display.set_caption("GALACTIC DEFENDER") # window title
pygame.display.set_icon(icon) # window icon

# fonts C&C Red Alert [INET]
menuFont = pygame.font.Font("assets/fonts/font.ttf", 100)
font = pygame.font.Font("assets/fonts/font.ttf", 60)
font2 = pygame.font.Font("assets/fonts/font.ttf", 30)

lvl = 1
aliensKilled = 0
nA = 4  # number of aliens every level; level 1: 4
n_bA = 2  # number of blue aliens every level
n_bgA = 1  # number of big aliens every level
n_sA = 2 # number of shooting aliens every level


# stores the game's objects and entities
a3 = [] # big alien segments
alienList = [] # normal alien
blue_alienList = [] # blue alien
big_alienList = [] # big alien
shoot_alienList = [] # shooting alien
alien_bulletList = [] # alien bullet
laserList = [] # laser
rockList = [] # rock
bulletList = [] # protagonist bullet
particleList = [] # particles
particleColors = [(251, 0, 0)] #list of colors for particles

# cursor
cursor = pygame.image.load('assets/cursor.png').convert_alpha() # cursor-image load optimization
crosshair = pygame.image.load('assets/crosshair.png').convert_alpha() # crosshair-image load optimization

# backgrounds
bg = pygame.image.load('assets/bg.png').convert_alpha() # background-image load optimization
start_bg = pygame.image.load('assets/start_bg.png').convert_alpha() # start screen-image load optimization
menu_bg = pygame.image.load('assets/menu_bg.png').convert_alpha() # menu screen-image load optimization
over_bg = pygame.image.load('assets/over_bg.png').convert_alpha() # game over screen-image load optimization

# background music
mixer.init() # initialize mixer
mixer.music.load('assets/music/bg.mp3') # background music load optimization
mixer.music.set_volume(0.1) # set the volume of the background music to 20%
mixer.music.play() # play the background music

#player and enemy
p = pygame.image.load('assets/p.png').convert_alpha() # protagonist-image load optimization
a = pygame.image.load('assets/aliens/a1.png').convert_alpha() # alien-image load optimization
a2 = pygame.image.load('assets/aliens/a2.png').convert_alpha() # alien2-image load optimization
a4 = pygame.image.load('assets/aliens/a4.png').convert_alpha() # alien4-image load optimization

# list that contains three different images that are used to create a "big" alien sprite
for i in range(3):
    img = pygame.image.load(f'assets/aliens/big/aB{i}.png').convert_alpha() # big alien-image load optimization
    a3.append(img)

# bullet
b = pygame.image.load('assets/bullet.png').convert_alpha() # protagonist bullet-image load optimization
a_b = pygame.image.load('assets/aliens/a_b.png').convert_alpha() # alien bullet-image load optimization

# bomb
# bmb = pygame.image.load('assets/bomb.png').convert_alpha() # bomb-image load optimization

# laser
l = pygame.image.load('assets/laser.png').convert_alpha() # laser-image load optimization


rockRandom = [] # list that contains the images of the rocks
for i in range(1, 7): # 6 different rocks
    rockChoose = pygame.image.load(f'assets/rocks/r{i}.png').convert_alpha() # rock-image load optimization w/ random sampling
    rockRandom.append(rockChoose) 

mColor = (110, 69, 206) # menu color

# display text on the screen
def menu(text, font, mColor, x, y): 
    m = font.render(text, True, mColor) # render the text with antialiasing (the text has smoothened edges)
    window.blit(m, (x, y)) # display the text at the specified coordinates

# show cursor for menu
def show_cursor(): 
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)) # set the cursor to a 8x8 transparent image
    cX, cY = pygame.mouse.get_pos() # get the cursor's position
    pos = [cX, cY] # store the cursor's position in a list
    window.blit(cursor, pos) # display the cursor at the specified coordinates

# change cursor to crosshair for game
def change_cursor():
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)) # set the cursor to a 8x8 transparent image
    cX, cY = pygame.mouse.get_pos() # get the cursor's position
    pos = [cX, cY] # store the cursor's position in a list
    window.blit(crosshair, pos) # display the crosshair at the specified coordinates


class Button:
    def __init__(self, image, x, y): # x and y are the coordinates of the button
        self.image = image # image of the button
        self.rect = self.image.get_rect() # make a rectangular button
        self.rect.center = (x, y) # center the button at the specified coordinates
        self.click = False # check if the button is clicked, initial state is False
        
    # display the button on the screen
    def draw(self):
        action = False # Set the initial action state to False
        mXY = pygame.mouse.get_pos() # Get the current mouse position

        # If the mouse is hovering over the button
        if self.rect.collidepoint(mXY):
            # If the left mouse button is pressed and the button has not already been clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True # Set the click state to True
                action = True # Set the action state to True

            # If the left mouse button is not pressed
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False # Set the click state to False

        window.blit(self.image, (self.rect.x, self.rect.y)) # Draw the button on the screen at its current position
        return action # Return the current action state


# buttons
bP = pygame.image.load('assets/resume_button.png').convert_alpha() # play button-image load optimization
bQ = pygame.image.load('assets/quit_button.png').convert_alpha() # quit button-image load optimization

playButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40) # create a play button
quitButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140) # create a quit button
play_overButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40) # create a play button at the end of the game (URGENCY)
quit_overButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140) # create a quit button at the end of the game
play_pauseButton = Button(bP, round(window.get_width()/2), round(window.get_height()/2)+40) # create a play(resume) button at the pause menu
quit_pauseButton = Button(bQ, round(window.get_width()/2), round(window.get_height()/2)+140) # create a quit button at the pause menu


class Player:
    # player initialization
    def __init__(self, x, y, location):
        pygame.sprite.Sprite.__init__(self) # initialize the sprite
        self.image = p # player image
        self.lives = 6 # player lives (how many times the player can be shot by an alien, or max aliens allowed to reach the left side of the screen)
        self.flip = False # flips player image (URGENCY)
        self.directionx = 0 # player's x-direction
        self.directiony = 0 # player's y-direction
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.location = location # player's location (left or right)
        self.rate = 0 # player's fire rate (how many frames must pass before the player can shoot again)
    
    # alter game state based on existing variables
    def update(self):
        # decrement shot rate if greater than 0 for advantage sake
        if self.rate > 0:
            self.rate -= 1

        mXY = pygame.mouse.get_pos() # get position of mouse as (x, y) coordinate tuple
        angle = 360-math.atan2(mXY[1]-300, mXY[0]-400)*180/math.pi # calculate the angle between the mouse position and the center of the screen (300,400) in degrees

        image = self.image.copy() # copy the player image
        self.rotated_image = pygame.transform .rotate(image, angle) # rotate the player image based on angle between image and mouse coordinates 

        angle += 1 % 360 # increment the angle by 1 degree

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False) # check for collisions between player and rocks

        # if collided with a rock, decrement lives to 0 to emulate instant death
        for _ in collisionsRock: 
            if self.lives != 0: 
                self.lives = 0

        
        collisionsLaser = pygame.Rect.colliderect(self.rect, laser.rect) # check for collisions between player and laser

        # if collided with a laser, decrement lives to 0 to emulate instant death
        if collisionsLaser:
            if self.lives != 0:
                self.lives = 0

    # frame-by-frame movement
    def move(self, moveR, moveL, moveU, moveD):
        x = 0
        y = 0

        if moveR: 
            x = self.location # move right
            self.directionx = 1 # set x-direction to 1
            self.flip = True # flip player image
            y = 0 # set y-direction to 0 (for the current frame)

        if moveL:
            x = -self.location # move left
            self.directionx = -1 # set x-direction to -1
            self.flip = True # flip player image
            y = 0 # set y-direction to 0 (for the current frame)

        if moveU:
            y = -self.location # move up
            self.directiony = 1 # set y-direction to 1
            x = 0 # set x-direction to 0 (for the current frame)

        if moveD:
            y = self.location # move down
            self.directiony = -1 # set y-direction to -1
            x = 0 # set x-direction to 0 (for the current frame)

        if self.rect.bottom + y > window.get_height()-81: # if the player's bottom edge is greater than the bottom edge of the screen
            y = window.get_height()-81 - self.rect.bottom # set y to the difference between the bottom edge of the screen and the player's bottom edge (to prevent the player from moving off the screen)

        if self.rect.top + y < 81: # if the player's top edge is less than the top edge of the screen
            y = 81 - self.rect.top # set y to the difference between the top edge of the screen and the player's top edge (to prevent the player from moving off the screen)

        if self.rect.left + x > window.get_width()-20: # if the player's left edge is greater than the left edge of the screen
            x = window.get_width()-20 - self.rect.left # set x to the difference between the left edge of the screen and the player's left edge (to prevent the player from moving off the screen)

        if self.rect.right + x <= 20: # if the player's right edge is less than the right edge of the screen
            x = 20 - self.rect.right # set x to the difference between the right edge of the screen and the player's right edge (to prevent the player from moving off the screen)

        self.rect.x += x # update the player's horizontal position
        self.rect.y += y # update the player's vertical position

    def show(self):
        window.blit(pygame.transform.flip( 
            self.rotated_image, False, False), self.rect) # show the player image at the player's position


player = Player(round(window.get_width()/2), round(window.get_height()/2), 5) # create a player at the center of the screen

lives = [] # list of health images
for x in range(7):
    healthImage = pygame.image.load(f'assets/health/{x}.png').convert_alpha() # load health images (emulates lives, decreased health)
    lives.append(healthImage) # add health images to list


class HealthBar:
    def __init__(self, image, x, y, scale):
        width = image.get_width() # get width of image
        height = image.get_height() # get height of image
        self.image = pygame.transform.scale(
            image, (int(width*scale), int(height*scale))) # scale image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates

    def show(self):
        window.blit(lives[player.lives], (self.rect.x, self.rect.y)) # show the health image at the specified coordinates


HEALTH = HealthBar(lives[player.lives], round(window.get_width()/2), window.get_height()-45, 0.7) # create a health bar at the bottom of the screen

class Bullet:
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = b # set image to bullet image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.dx = dx # set horizontal speed
        self.dy = dy # set vertical speed

    def update(self):
        self.rect.x += self.dx # update the bullet's horizontal position
        self.rect.y += self.dy # update the bullet's vertical position

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) # show the bullet image at the bullet's position


def bullet_move():
    sX, sY = pygame.mouse.get_pos() # get mouse position

    distanceX = sX - player.rect.x # get horizontal distance between mouse and player
    distanceY = sY - player.rect.y # get vertical distance between mouse and player

    angle = math.atan2(distanceY, distanceX) # get angle between mouse and player

    speedX = int(16 * math.cos(angle)) # get horizontal speed
    speedY = int(16 * math.sin(angle)) # get vertical speed

    if player.rate == 0: # if the player's rate is 0
        player.rate = 20 # set the player's rate to 20
        bulletList.append(Bullet(player.rect.centerx, player.rect.centery, speedX, speedY)) # add a bullet to the bullet list

def bullet_check(): # check if bullets are off screen
    if not len(bulletList) == 0: # if the bullet list is not empty
        for bullet in bulletList:  # for each bullet in the bullet list
            if not bullet.rect.x >= 0 and bullet.rect.x <= window.get_width() and bullet.rect.y >= 60 and bullet.rect.y <= window.get_height()-60: # if the bullet is not on the screen
                try:
                    bulletList.remove(bullet) # remove the bullet from the bullet list
                except ValueError: 
                    pass # if the bullet is not in the bullet list, pass

class AlienBullet:
    def __init__(self, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = a_b # set image to alien bullet image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = 6 # set speed
        self.rate = 0 # set rate
        self.dx = dx # set horizontal speed
        self.dy = dy # set vertical speed

    def update(self):
        self.rect.x += self.dx # update the bullet's horizontal position
        self.rect.y += self.dy # update the bullet's vertical position

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect) # check for alien bullet collisions with player
        if collisionsPlayer:
            alien_bulletList.remove(self) # remove alien bullet from alien bullet list (disappears)
            player.lives -= 1 # decrease player lives

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) # show the bullet image at the bullet's position

# auto aim bullets at the player
def alien_shoot():
    global alien_bullet  # make alien bullet global
    freq = random.randint(75, 175) # set random frequency of alien shooting

    pX, pY = player.rect.x, player.rect.y # get player position

    distanceX = pX - alienShoot.rect.x # get horizontal distance between player and alien
    distanceY = pY - alienShoot.rect.y # get vertical distance between player and alien

    angle = math.atan2(distanceY, distanceX) # get angle between player and alien

    speedX = int(10 * math.cos(angle)) # get horizontal speed
    speedY = int(10 * math.sin(angle)) # get vertical speed

    if alienShoot.rate == 0:
        alienShoot.rate = freq # set alien shooting rate
        alien_bulletList.append(AlienBullet(alienShoot.rect.centerx, alienShoot.rect.centery, speedX, speedY)) # add a bullet to the bullet list

# check if bullets are off screen
def alien_bullet_check():
    if not len(alien_bulletList) == 0:
        for alien_bullet in alien_bulletList:
            if not  alien_bullet.rect.x >= 0 and alien_bullet.rect.x <= window.get_width() and alien_bullet.rect.y >= 60 and alien_bullet.rect.y <= window.get_height()-60: # if the bullet is not on the screen
                try:
                    alien_bulletList.remove(alien_bullet) # remove the bullet from the bullet list
                except ValueError:
                    pass # if the bullet is not in the bullet list, pass


class Alien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = a # set image to alien image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = 2 # set speed

    def move(self):
        self.rect.x -= self.speed # move the alien left

    def update(self):
        global aliensKilled # make aliens killed global

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False) # check for alien collisions with rocks (to prevent aliens from spawning on rocks)
        for _ in collisionsRock: 
            alienList.remove(self) # remove alien from alien list (disappears)


        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False) # check for alien collisions with player bullets
        for bullet in collisionsBullet: # for each bullet in the bullet list
            if player.lives > 0: # if the player has lives
                bulletList.remove(bullet) # remove the bullet from the bullet list (disappears)
                alienList.remove(self) # remove the alien from the alien list (disappears)
                aliensKilled += 1 # increase aliens killed by 1 (dispalyed on screen)

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect) 
        if collisionsPlayer: # if the alien collides with the player
            alienList.remove(alien) # remove the alien from the alien list (disappears)
            player.lives -= 1 # decrease player lives

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) # show the alien image at the alien's position


for _ in range(nA): # nA is count of aliens at this level
    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create an alien at a random x and y position
    alienList.append(alien) # add the alien to the alien list


class BlueAlien:
    def __init__(self, x, y): 
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = a2 # set image to blue alien image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = 3.5 # set speed slightly faster than normal alien
        self.chance = random.randint(1, 5) # set chance of blue alien moving vs staying still (simulating slower, more methodical movement, symbolizing intelligence)

    def move(self):
        if self.chance == 2: # if the chance is 2
            self.rect.x -= self.speed # move the blue alien left

    def update(self):
        global aliensKilled # make aliens killed global

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False) # check for blue alien collisions with rocks (to prevent blue aliens from spawning on rocks)
        for _ in collisionsRock: 
            blue_alienList.remove(self) # remove blue alien from blue alien list (disappears)


        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False)
        for bullet in collisionsBullet:
            if player.lives > 0:
                bulletList.remove(bullet) # remove the bullet from the bullet list (disappears)
                blue_alienList.remove(self) # remove the blue alien from the blue alien list (disappears)
                aliensKilled += 1 # increase aliens killed by 1 (dispalyed on screen)

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect) # check for blue alien collisions with player
        if collisionsPlayer:
            blue_alienList.remove(self) # remove the blue alien from the blue alien list (disappears)
            player.lives -= 1 # decrease player lives

    def show(self):
        if self.chance == 2: # if the chance is 2
            window.blit(self.image, (self.rect.x, self.rect.y)) # show the blue alien image at the blue alien's position


for _ in range(n_bA): # n_bA is count of blue aliens at this level
    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a blue alien at a random x and y position
    blue_alienList.append(alienBlue) # add the blue alien to the blue alien list


class BigAlien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # initialize sprite
        self.lives = 2 # set lives to 2 (more health than normal alien and blue alien)
        self.image = a3[self.lives] # set image to big alien image based on lives
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = 8 # set speed (faster than normal alien and blue alien)
        self.chance = random.randint(1, 4) # set chance of big alien moving vs staying still (simulating slower, more methodical movement, symbolizing intelligence)

    def move(self):
        if lvl > 4: # if the level is greater than 4
            if self.chance == 3: # if the chance is 3
                self.rect.x -= self.speed # move the big alien left

    def update(self):
        global aliensKilled

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False) # check for big alien collisions with rocks (to prevent big aliens from spawning on rocks)
        for _ in collisionsRock:
            big_alienList.remove(self) # remove big alien from big alien list (disappears)

        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False) # check for big alien collisions with player bullets
        for bullet in collisionsBullet:
            if player.lives > 0:
                self.lives -= 1 # decrease big alien lives by 1
                bulletList.remove(bullet) # remove the bullet from the bullet list (disappears)
                if self.lives < 0: # if the big alien has no more lives
                    big_alienList.remove(self) # remove the big alien from the big alien list (disappears)
                    aliensKilled += 1 # increase aliens killed by 1 (displayed on screen)

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect) # check for big alien collisions with player
        if collisionsPlayer: # if the big alien collides with the player
            self.lives -= 1 # decrease big alien lives by 1
            if self.lives < 0: # if the big alien has no more lives
                big_alienList.remove(self) # remove the big alien from the big alien list (disappears)
                player.lives -= 1 # decrease player lives

    def show(self):
        if lvl > 4: # if the level is greater than 4
            if self.chance == 3: # if the chance is 3
                window.blit(a3[self.lives], (self.rect.x, self.rect.y)) # show the big alien image at the big alien's position


for _ in range(n_bgA): # n_bgA is count of big aliens at this level
    alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a big alien at a random x and y position
    big_alienList.append(alienBig) # add the big alien to the big alien list


class ShootAlien:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = a4 # set image to shoot alien image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = 3  # set speed (slower than normal alien and blue alien)
        self.chance = random.randint(1,2) # set chance of shoot alien moving vs staying still (simulating slower, more methodical movement, symbolizing intelligence)
        self.rate = 0 # set rate to 0 (used to control how often the shoot alien shoots)

    def move(self):
        if lvl > 2: # if the level is greater than 2
            if self.chance == 2: # if the chance is 2
                self.rect.x -= self.speed # move the shoot alien left
                if self.rect.x < window.get_width(): # if the shoot alien is on the screen
                    alien_shoot() # shoot
                    alien_bullet_check() # check if the shoot alien's bullet has collided with anything

    def update(self):

        global aliensKilled

        if self.rate > 0: # if the rate is greater than 0
            self.rate -= 1 # decrease the rate by 1

        collisionsRock = pygame.sprite.spritecollide(self, rockList, False) # check for shoot alien collisions with rocks (to prevent shoot aliens from spawning on rocks)
        for _ in collisionsRock:
            shoot_alienList.remove(self) # remove shoot alien from shoot alien list (disappears)

        collisionsBullet = pygame.sprite.spritecollide(self, bulletList, False) # check for shoot alien collisions with player bullets
        for bullet in collisionsBullet:
            if player.lives > 0: # if the player has lives
                bulletList.remove(bullet) # remove the bullet from the bullet list (disappears)
                shoot_alienList.remove(self) # remove the shoot alien from the shoot alien list (disappears)
                aliensKilled += 1 # increase aliens killed by 1 (displayed on screen)

        collisionsPlayer = pygame.Rect.colliderect(self.rect, player.rect) # check for shoot alien collisions with player
        if collisionsPlayer: 
            shoot_alienList.remove(self) # remove the shoot alien from the shoot alien list (disappears)
            player.lives -= 1 # decrease player lives

    def show(self): 
        if lvl > 2: # if the level is greater than 2
            if self.chance == 2: # if the chance is 2
                window.blit(self.image, (self.rect.x, self.rect.y)) # show the shoot alien image at the shoot alien's position

for _ in range(n_sA):
    alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a shoot alien at a random x and y position
    shoot_alienList.append(alienShoot) # add the shoot alien to the shoot alien list


class Laser:
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = l # set image to laser image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speedx = 2 # set vertical speed 
        self.speedy = 2 # set horizontal speed
        self.directiony = random.choice([1, -1]) # set direction of movement (up or down)

    def update(self):
        slowdown = random.randint(1, 2) # set slowdown to 1 or 2 (used to control how often the laser slows down, simulating sentience)
        self.speedx += lvl/8 # increase speed by 1/8 of the level (increases difficulty)
        self.speedy += lvl/12 # increase speed by 1/12 of the level (increases difficulty)

        if self.speedx > 6 or self.speedy > 6: # if the speed is greater than 6
            if slowdown == 1: # if slowdown is 1
                self.speedx = 3 # set horizontal speed to 3
                self.speedy = 3 # set vertical speed to 3


    def moveLR(self):
        self.rect.x += self.speedx # move the laser right

        if self.rect.top < 10: # if the laser is at the top of the screen
            self.directiony = 1 # set direction to down (bounce off top of screen)
        if self.rect.bottom > window.get_height()-10: # if the laser is at the bottom of the screen
            self.directiony = -1 # set direction to up (bounce off bottom of screen)

        self.rect.y += self.speedy * self.directiony 


    def moveRL(self):
        self.rect.x = (self.rect.x * -1) + self.speedx # move the laser left

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) # show the laser image at the laser's position

laser = Laser(1, round(window.get_height()/2)) # create a laser at the center of the screen


class Rock:
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.image = random.choice(rockRandom) # set image to a random rock image
        self.tmp_image = self.image # set temporary image to the image
        self.rect = self.image.get_rect() # make a rectangular hitbox
        self.rect.center = (x, y) # center the hitbox at the specified coordinates
        self.speed = speed # set speed
        self.angle = 10 # set angle
        self.directionx = random.choice([1, -1]) # set direction of movement (left or right)
        self.directiony = random.choice([1, -1]) # set direction of movement (up or down)

    def update(self):

        self.tmp_image = pygame.transform.rotate(self.image, self.angle) # rotate the rock
        self.angle += 1 % 360 # increase the angle by 1

        if self.rect.right < -random.randint(100, 300): # if the rock is off the left side of the screen
            self.directionx = 1 # set direction to right (bounce off left side of screen)

        if self.rect.right > window.get_width()+random.randint(100, 300): # if the rock is off the right side of the screen
            self.directionx = -1  # set direction to left (bounce off right side of screen)

        if self.rect.top < -random.randint(100, 300): # if the rock is off the top of the screen
            self.directiony = 1 # set direction to down (bounce off top of screen)

        if self.rect.bottom > window.get_height()+random.randint(100, 300): # if the rock is off the bottom of the screen
            self.directiony = -1 # set direction to up (bounce off bottom of screen)

        self.rect.x += self.speed * self.directionx # move the rock horizontally
        self.rect.y += self.speed * self.directiony # move the rock vertically

        collisionsLaser= pygame.Rect.colliderect(self.rect, laser.rect) # check for collisions between the rock and the laser
        if collisionsLaser: 
            rockList.remove(self) # remove the rock from the rock list (disappears)

    def show(self):
        window.blit(self.tmp_image, (self.rect.x, self.rect.y)) # show the rock image at the rock's position


for i in range(4):
    x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)]) # set x to a random x position
    y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)]) # set y to a random y position

    rock = Rock(x, y, random.randint(1, 3)) # create a rock at the random x and y position with a random speed
    rockList.append(rock) # add the rock to the rock list


# game loop

def main(): 

    global lvl, nA, n_bA, n_bgA, n_sA, bulletList, alienList, blue_alienList, big_alienList, alien_bulletList,aliensKilled, alien, alienBlue, alienBig, alienShoot, laser, player, laserNUM, rock # global variables

    # game variables
    gamePause = False
    gameOver = False
    gameStart = False

    tiles = math.ceil(window.get_width() / bg.get_width()) + 1 # number of tiles needed to fill the screen
    scroll = 0 

    moveR = False
    moveL = False
    moveU = False
    moveD = False
    shoot = False

    while True: # game loop

        if gameStart == False: # if the game hasn't started
            window.blit(start_bg, (0, 0)) # show the start screen
            if playButton.draw(): # if the play button is clicked
                gameStart = True # start the game

            if quitButton.draw(): # if the quit button is clicked
                pygame.quit() # quit pygame
                sys.exit() # exit the program

        if gameOver == True: # if the game is over
            gameStart = False # stop the game
            window.blit(over_bg, (0, 0)) # show the game over screen
            menu("YOU DIED...", font, mColor, round(window.get_width()/2)-110, (window.get_height()/2)-150) 
            menu("GAME OVER", font, mColor, round(window.get_width()/2)-110, (window.get_height()/2)-70) # show the game over text
            if play_overButton.draw():
                # reset variables(URGENCY)
                lvl = 0 # change level to 0 to fix off by one error when starting a new game with main()
                aliensKilled = 0
                nA = 4  # number of aliens every level; level 1: 4
                n_bA = 2  # number of blue aliens every level
                n_bgA = 1  # number of big aliens every level
                n_sA = 2 # number of shooting aliens every level
                bulletList = []
                alienList = []
                blue_alienList = []
                big_alienList = []
                alien_bulletList = []

                laser = Laser(1, round(window.get_height()/2)) 
                player = Player(round(window.get_width()/2), round(window.get_height()/2), 5)
                laserNUM = 0            
                main()
                
            if quit_overButton.draw(): # if the quit button is clicked
                pygame.quit() # quit pygame
                sys.exit() # exit the program

        if gamePause == True: # if the game is paused
            if gameOver == True: # if the game is over
                pass # do nothing
            else:
                window.blit(menu_bg, (0, 0)) # show the pause screen
                menu("PAUSE MENU", font, mColor, round(window.get_width()/2)-130, (window.get_height()/2)-200) # show the pause menu text

                if play_pauseButton.draw(): # if the play button is clicked
                    gamePause = False # unpause the game

                if quit_pauseButton.draw(): # if the quit button is clicked
                    pygame.quit() # quit pygame
                    sys.exit() # exit the program

        if gameStart == True and gamePause == False: # if the game is started and not paused

            change_cursor() # change the cursor to the crosshair

            if player.lives <= 0: # if the player has no lives left
                gameOver = True # end the game
                gameStart = False # stop the game

            for i in range(0, tiles): # show the background image
                window.blit(bg, (i*bg.get_width() + scroll, 0)) # show the background image at the scroll position

            scroll -= 5 # move the background image to the left
            if abs(scroll) > bg.get_width(): # if the background image is off the screen
                scroll = 0 # reset the scroll position (loop the background image)

            if len(alienList) == 0: # if there are no aliens left
                lvl += 1 # increase the level
                nA += 1 # increase the number of aliens
                n_bA += 1 # increase the number of blue aliens

                if lvl > 2: # if the level is greater than 2
                    n_sA += 2 # increase the number of shooting aliens
                    if n_sA > 6: # if the number of shooting aliens is greater than 6
                        n_sA = 3 # reset the number of shooting aliens

                if lvl > 4: # if the level is greater than 4
                    n_bgA += 1 # increase the number of big aliens
                    if n_bgA > 5: # if the number of big aliens is greater than 5
                        n_bgA = 0 # reset the number of big aliens

                for _ in range(nA):
                    alien = Alien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create an alien at a random x and y position
                    alienList.append(alien) # add the alien to the alien list

                for _ in range(n_bA):
                    alienBlue = BlueAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a blue alien at a random x and y position
                    blue_alienList.append(alienBlue) # add the blue alien to the blue alien list

                if lvl > 4:
                    for _ in range(n_bgA): # if the level is greater than 4
                        alienBig = BigAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a big alien at a random x and y position
                        big_alienList.append(alienBig) # add the big alien to the big alien list

                if lvl > 2: 
                    for _ in range(n_sA): # if the level is greater than 2
                        alienShoot = ShootAlien((random.randint(window.get_width()+200, window.get_width()+400)), (random.randint(100, window.get_height()-120))) # create a shooting alien at a random x and y position
                        shoot_alienList.append(alienShoot) # add the shooting alien to the shooting alien list

                laser.update() # update the laser

            laser.show() # show the laser
            laser.moveLR() # move the laser left to right
            if laser.rect.x >= window.get_width()+200: # if the laser is off the screen
                laser.moveRL() # move the laser right to left

            for rock in rockList: # for every rock in the rock list
                rock.show() # show the rock
                rock.update() # update the rock

                if len(rockList) < 3: # if there are less than 3 rocks
                    for i in range(random.randint(4, 6)): # create 4 to 6 rocks
                        x = random.choice([random.randint(-window.get_width()+200, -window.get_width()+800), random.randint(window.get_width()+200, window.get_width()+800)]) # create a rock at a random x position
                        y = random.choice([random.randint(window.get_height()+200, window.get_height()+800), random.randint(-window.get_height()+200, -window.get_height()+800)]) # create a rock at a random y position
                        rock = Rock(x, y, random.randint(1, 6)) # create a rock at the random x and y position
                        rockList.append(rock) # add the rock to the rock list

                if len(rockList) > 6: # if there are more than 6 rocks
                    rockList.remove(rock) # remove the rock from the rock list

            player.update() # update the player
            player.show() # show the player
            player.move(moveR, moveL, moveU, moveD) # move the player

            if player.lives <= 6 and player.lives > 0: # if the player has 6 or less lives
                if shoot: # if the player is shooting
                    bullet_move() # move the bullet
                    bullet_check() # check if the bullet is off the screen

            for bullet in bulletList: # for every bullet in the bullet list
                bullet.update() # update the bullet
                bullet.show() # show the bullet

            for alien in alienList: # for every alien in the alien list
                alien.show() # show the alien
                alien.update() # update the alien
                alien.move() # move the alien
                if player.lives > 0: # if the player has lives left
                    if alien.rect.x + alien.image.get_width() < 10: # if the alien is off the screen
                        player.lives -= 1 # remove a life from the player (because the alien got past the player)
                        alienList.remove(alien) # remove the alien from the alien list
            
            for alienBlue in blue_alienList: # for every blue alien in the blue alien list
                alienBlue.show() # show the blue alien
                alienBlue.update() # update the blue alien
                alienBlue.move() # move the blue alien

                if player.lives > 0: # if the player has lives left
                    if alienBlue.rect.x + alienBlue.image.get_width() < 10: # if the blue alien is off the screen
                        player.lives -= 1 # remove a life from the player (because the blue alien got past the player)
                        blue_alienList.remove(alienBlue) # remove the blue alien from the blue alien list

            for alienBig in big_alienList: # for every big alien in the big alien list
                alienBig.show() # show the big alien
                alienBig.update() # update the big alien
                alienBig.move() # move the big alien

                if player.lives > 0: # if the player has lives left
                    if alienBig.rect.x + alienBig.image.get_width() < 10: # if the big alien is off the screen
                        player.lives -= 1 # remove a life from the player (because the big alien got past the player)
                        big_alienList.remove(alienBig) # remove the big alien from the big alien list


            for alien_bullet in alien_bulletList: # for every alien bullet in the alien bullet list
                alien_bullet.update() # update the alien bullet
                alien_bullet.show() # show the alien bullet

            for alienShoot in shoot_alienList: # for every shooting alien in the shooting alien list
                alienShoot.show() # show the shooting alien
                alienShoot.update() # update the shooting alien
                alienShoot.move() # move the shooting alien

                if player.lives > 0: # if the player has lives left
                    if alienShoot.rect.x + alienShoot.image.get_width() < 64: # if the shooting alien is off the screen
                        player.lives -= 1 # remove a life from the player (because the shooting alien got past the player)
                        shoot_alienList.remove(alienShoot) # remove the shooting alien from the shooting alien list
           
            clock.tick() # measure the time between frames
            menu(f"FPS: {int(clock.get_fps())}", font2, mColor, 75, 20) # show the fps
            HEALTH.show() # show the health bar
            menu(f"ALIENS KILLED: {aliensKilled}", font2, mColor, window.get_width()-220, window.get_height()-50) # show the aliens killed
            menu(f"LEVEL: {lvl}", font2, mColor, 50, window.get_height()-50) # show the level

        else: # if the game is paused
            show_cursor() # show the cursor

        for event in pygame.event.get(): # for every event in the event list
            if event.type == QUIT: # if the event is quit
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN: # if a key is pressed
                if event.key == K_ESCAPE: # if the escape key is pressed
                    gamePause = True # pause the game
                if event.key == K_RIGHT or event.key == K_d: # if the right key or d is pressed
                    moveR = True # move right
                if event.key == K_LEFT or event.key == K_a: # if the left key or a is pressed
                    moveL = True # move left
                if event.key == K_UP or event.key == K_w: # if the up key or w is pressed
                    moveU = True # move up
                if event.key == K_DOWN or event.key == K_s: # if the down key or s is pressed
                    moveD = True # move down

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if the left mouse button is pressed
                shoot = True # shoot

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # if the left mouse button is released
                shoot = False # stop shooting

            if event.type == KEYUP: # if a key is released
                if event.key == K_RIGHT or event.key == K_d: # if the right key or d is released
                    moveR = False # stop moving right
                if event.key == K_LEFT or event.key == K_a: # if the left key or a is released
                    moveL = False # stop moving left
                if event.key == K_UP or event.key == K_w: # if the up key or w is released
                    moveU = False # stop moving up
                if event.key == K_DOWN or event.key == K_s: # if the down key or s is released
                    moveD = False # stop moving down

        if not gamePause and not gameOver and gameStart: # if the game is not paused, not over, and has started
            change_cursor() # change the cursor

        pygame.display.update() # update the display
        clock.tick(60) # limit the fps to 60


main() # run the main function
