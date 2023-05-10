from GameSequence import *
from piCode import *
import pygame
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup([gLight, rLight], GPIO.OUT)

pygame.init()
WIDTH = 1024
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Guitar Hero - Menu")

pygame.mixer.init()     
pygame.mixer.music.load("ILoveRockNRoll.mp3")
pygame.mixer.music.set_volume(0.7)

# menu, game, & gameOver images 
menu = pygame.image.load("images/menu.gif")
menu = pygame.transform.scale(menu, (WIDTH, HEIGHT))
gameImg = pygame.image.load("images/background.gif")
gameImg = pygame.transform.scale(gameImg, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

class Button():
    def __init__(self, image, pos, textInput, font, baseColor, hoverColor):
        self.image = image
        self.xPos = pos[0]
        self.yPos = pos[1]
        self.font = font
        self.baseColor, self.hoverColor = baseColor, hoverColor
        self.textInput = textInput
        self.text = self.font.render(self.textInput, True, self.baseColor)
        self.rect = self.image.get_rect(center = (self.xPos, self.yPos))
        self.textRect = self.text.get_rect(center=(self.xPos, self.yPos))

    # puts image and text on screen
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    # checks if we click button
    def input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    # checks if hover over button if so change color
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.textInput, True, self.hoverColor)
        else:
            self.text = self.font.render(self.textInput, True, self.baseColor)


class Note:
    def __init__(self, x, y, color, image, speed=8.5):
        self.x = x
        self.y = y
        self.color = color
        self.image = image
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Lane:
    def __init__(self, x, y, key, color):
        self.x = x
        self.y = y
        self.key = key
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, 60, 60)

    def draw(self, screen):
       pass
        #pygame.draw.rect(screen, self.color, self.rect, 2)


def handle_input(key, lanes: Lane):
    pThres = 30
    global score
    for lane in lanes:
        if key == lane.key:
            for note in notes:
                if (lane.y-pThres < note.y < lane.y+pThres):
                    #print(lane.y-pThres < note.y < lane.y+pThres)
                    score += 100
                    return True


lanes = [
    Lane(360, 700, 49, (128, 128, 128)),
    Lane(425, 700, 50, (128, 128, 128)),
    Lane(487, 700, 51, (128, 128, 128)),
    Lane(553, 700, 52, (128, 128, 128)),
    Lane(616, 700, 53, (128, 128, 128))
]

score = 0 
notes = []
spawn_timer = 0
spawn_rate = 60

current_song = song["rockNroll"]
song_length = len(current_song)
song_position = 0
endSong = False

green_button = pygame.image.load("images/greenButton.gif")
red_button = pygame.image.load("images/redButton.gif")
yellow_button = pygame.image.load("images/yellowButton.gif")
blue_button = pygame.image.load("images/blueButton.gif")
orange_button = pygame.image.load("images/orangeButton.gif")

button_images = [green_button, red_button, yellow_button, blue_button, orange_button]
frameCount = 0 
frameRate = 85
timer = 65
demoTime = 18

def displayTimer(time):
    global frameCount
    global frameRate
    # calculate total seconds
    totalSecs = time - (frameCount//frameRate)
    if totalSecs < 0:
        totalSecs = 0
        if totalSecs == 0:
            finishGameMenu()
    # divide by 60 to get total minutes
    mins = totalSecs // 60
    # remainder to get seconds 
    seconds = totalSecs % 60
    outputString = "Time left: {0:02}:{1:02}".format(mins, seconds)
    font = pygame.font.Font(None, 25)
    text = font.render(outputString, True, (255,255,255))
    screen.blit(text, (50,15))
    frameCount += 1
    #clock.tick(frameRate)
    pygame.display.flip()

# Main game LOOP
def gameLoop():
    global song_position
    global song_length
    global spawn_timer
    global endSong
    global timer
    pygame.mixer.music.play()
    pygame.display.set_caption("Guitar Hero - Game")
    while True:
        displayTimer(timer)
        screen.fill((0,0,0))
        screen.blit(gameImg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if handle_input(event.key, lanes) == True:
                    greenLight()
                else:
                    redLight()
       
        for lane in lanes:
            lane.draw(screen)

        if song_position < song_length:
            current_section = current_song[song_position]
            if spawn_timer >= current_section["delay"]:
                spawn_timer = 0
                song_position += 1

                for note in current_section["notes"]:
                    lane_num = int(note)-1
                    if 0 <= lane_num < len(lanes):
                        new_note = Note(lanes[lane_num].x, 0, lanes[lane_num].color, button_images[lane_num])
                        notes.append(new_note)
                    else:
                        print(f"Warning: Invalid lane number {lane_num} found in song data. Skipping this note.")
            else:
                spawn_timer += clock.get_time()

        for note in notes:
            note.update()
            note.draw(screen)

        # Basically where we detect when the notes have reached the limit (around 630pxs)
        if len(notes) > 0 and notes[0].y > 700:
            notes.pop(0)

        clock.tick(100)
        

def demoGame():
    global song_position
    global spawn_timer
    pygame.mixer.music.play()
    pygame.display.set_caption("Guitar Hero - Demo")
    while True:
        displayTimer(demoTime)
        screen.fill((0,0,0))
        screen.blit(gameImg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if handle_input(event.key, lanes) == True:
                    greenLight()
                else:
                    redLight()

        
        for lane in lanes:
            lane.draw(screen)
        
        if song_position < song_length/2:
            current_section = current_song[song_position]
            if spawn_timer >= current_section["delay"]:
                spawn_timer = 0
                song_position += 1

                for note in current_section["notes"]:
                    lane_num = int(note)-1
                    if 0 <= lane_num < len(lanes):
                        new_note = Note(lanes[lane_num].x, 0, lanes[lane_num].color, button_images[lane_num])
                        notes.append(new_note)
                    else:
                        print(f"Warning: Invalid lane number {lane_num} found in song data. Skipping this note.")
            else:
                spawn_timer += clock.get_time()

        for note in notes:
            note.update()
            note.draw(screen)

        # Basically where we detect when the notes have reached the limit (around 630pxs)
        if len(notes) > 0 and notes[0].y > 700:
            notes.pop(0)

        clock.tick(100)

show_main_menu = True
def showMainMenu():
    global show_main_menu
    while show_main_menu:
        pygame.display.set_caption("Guitar Hero - Menu")


        screen.blit(menu, (0,0))

        menuMousePos = pygame.mouse.get_pos()
        menuTitle = pygame.font.Font("freesansbold.ttf", 100).render("Main Menu", True, (255,255,255))
        menuRect = menuTitle.get_rect(center=(WIDTH/2, 100))

        playButton = Button(image=pygame.image.load("images/greyButton.gif"), pos=(WIDTH/2, 250),
                            textInput="PLAY", font=pygame.font.Font("freesansbold.ttf", 75), baseColor=(169,11,215), hoverColor=(255,255,255))
        demoButton = Button(image=pygame.image.load("images/greyButton.gif"), pos=(WIDTH/2, 425),
                            textInput="DEMO", font=pygame.font.Font("freesansbold.ttf", 75), baseColor=(169,11,215), hoverColor=(255,255,255))
        quitButton = Button(image=pygame.image.load("images/greyButton.gif"), pos=(WIDTH/2, 600),
                            textInput="QUIT", font=pygame.font.Font("freesansbold.ttf", 75), baseColor=(169,11,215), hoverColor=(255,255,255))

        screen.blit(menuTitle, menuRect)

        for button in [playButton, demoButton, quitButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.input(menuMousePos):
                    gameLoop()
                if demoButton.input(menuMousePos):
                    demoGame()
                if quitButton.input(menuMousePos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def finishGameMenu():
    global score
    pygame.mixer.music.pause()
    pygame.display.set_caption("Guitar Hero - Game Over")
    screen.blit(menu, (0,0))
    overTitle = pygame.font.Font("freesansbold.ttf", 100).render("Game Over!", True, (255, 255, 255))
    overRect =  overTitle.get_rect(center=(WIDTH/2, 200))
    scoreTitle = pygame.font.Font("freesansbold.ttf", 80).render(f"Your score is {score}", True, (255, 255, 255))
    scoreRect = scoreTitle.get_rect(center=(WIDTH/2, 400))
    screen.blit(overTitle, overRect)
    screen.blit(scoreTitle, scoreRect)

showMainMenu()