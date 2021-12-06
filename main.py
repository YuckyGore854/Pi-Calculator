import pygame # gets pygame in here

pygame.init() # starts pygame in here

screen = pygame.display.set_mode((500,500))#creates a big screen
clock = pygame.time.Clock() # starts clock, used for framerate

pygame.display.set_caption("Calculate Pi!") # captions screen

font = pygame.font.Font("freesansbold.ttf", 32) # starts up font for text generation

doExit = False # our exit variable for the main loop

class block: # block that has a weight, velocity, x and y positions
    def __init__(self, weight, x, y):
        self.weight = weight
        self.x = x # constructor holds position, weight, and horizontal velocity
        self.y = y
        self.xVel = 0
    def draw(self,sizex,sizey):
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y-sizey, sizex, sizey)) # renders the blocks and subtracts the height in order to render them at the same level
    def move(self):#updates the position of the block
        self.x += self.xVel
    def collide(self, x):#
        if self.x < x: # if the left side of the block touches given argument
            return True
        else:
            return False

count = 0 # used for storing number of collisions

# variable that lets us set how heavy the big block is and therefore how many digits are caluculated
digits = 100**6 # n-1 digits calculated
# takes a lot longer to calculate the higher you go

firstBlock = block(1, 50, 50)# creates one block with weight of 1, position at 50,50
secondBlock = block(digits, 100, 50)# creates one block with a weight of 100^n as defined above


timestoRun = 10000 # lets us run this accurately, runs the collisions this many times per game loop
                   # if calculation is wrong, increase this number

firstBlock.xVel = 0 / timestoRun # sets velocity / timestoRun so we can actually see it
secondBlock.xVel = -2 / timestoRun # lets us actually see the blocks


while not doExit:#GAME LOOP########
    for event in pygame.event.get(): #grabs any events (mouse movement, keyboard, etc)
        if event.type == pygame.QUIT: #lets you quit the game from the gamescreen(the red x in the corner)
            doExit = True

    #PHYSICS SECTION###########
    clock.tick(60) # sets framerate

    #print(count) # prints number of collisions to console

    for i in range(timestoRun): # runs collision tests a ton of times every game loop
        firstBlock.move() # updates position
        secondBlock.move() # updates position
        if firstBlock.collide(0) == True: # if small block touches the left wall
            firstBlock.xVel *= -1 # reverse velocity
            count +=1 # add a count to the velocity
        if secondBlock.collide(firstBlock.x + 10) == True: # if the left side of the big block touches the small one
        
            oldSpeed = firstBlock.xVel # stores first block's speed, needed for updating velocity of second block later

            # runs calculation to find out the new velocity of the small block
            firstBlock.xVel = ((firstBlock.weight-secondBlock.weight)/(firstBlock.weight + secondBlock.weight)*firstBlock.xVel) + (2*secondBlock.weight)/(firstBlock.weight+secondBlock.weight)*secondBlock.xVel
            # equation is just what you would use to specifically find the first velocity
            # adapted from elastic collision page on wikipedia

            # same as above but adjusted to calculate the second velocity
            secondBlock.xVel = ((2*firstBlock.weight)/(firstBlock.weight + secondBlock.weight)*oldSpeed) + (secondBlock.weight - firstBlock.weight)/(firstBlock.weight + secondBlock.weight)*secondBlock.xVel
            
            count += 1 # adds one to collision counter
    # END PHYSICS#############################

    # START RENDER#############################################
    screen.fill((255,255,255)) # fills the screen to avoid smearing

    text = font.render(str(count), False, (25, 25, 25)) # renders number of collisions as text
    pitext = font.render("Pi equals:", False, (25,25,25))
    periodtext = font.render(("."), False, (25,25,25))
    smallblocktext = font.render("Mass of small block: ", False, (25,25,25))
    smallblocknumber = font.render(str(1), False, (25,25,25))
    bigblocknumber = font.render(str(digits), False, (25,25,25))
    bigblocktext = font.render("Mass of large block: ", False, (25,25,25))

    screen.blit(text, (260,70)) # blits number of collisions to screen
    screen.blit(pitext, (100, 70))
    screen.blit(periodtext, (274, 70))
    screen.blit(smallblocktext, (10, 150))
    screen.blit(smallblocknumber, (330,150))
    screen.blit(bigblocknumber, (10,230))
    screen.blit(bigblocktext, (10, 200))
    firstBlock.draw(10,10) # draw the first block with a size of 10, 10
    secondBlock.draw(50,50) # draw the second block with a size of 50, 50

    pygame.display.flip() # end render section

pygame.quit()
