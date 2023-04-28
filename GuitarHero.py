from GameSequence import *
import pygame
import sys

pygame.init()
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    def __init__(self, x, y, color, image, speed=5):
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
        # pygame.draw.rect(screen, self.color, self.rect, 2)


def handle_input(key, lanes: Lane):
    pThres = 30
    global score
    for lane in lanes:
        if key == lane.key:
            #print(f"Key {key} pressed")
            for note in notes:
                # 590 < 625 and 625 < 660
                if (lane.y-pThres < note.y < lane.y+pThres):
                    #print(lane.y-pThres < note.y < lane.y+pThres)
                    score += 100
        #print(score)
            


lanes = [
    Lane(352, 625, 49, (128, 128, 128)),
    Lane(415, 625, 50, (128, 128, 128)),
    Lane(475, 625, 51, (128, 128, 128)),
    Lane(539, 625, 52, (128, 128, 128)),
    Lane(602, 625, 53, (128, 128, 128))
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

# Main game LOOP
def gameLoop():
    global song_position
    global song_length
    global spawn_timer
    pygame.mixer.music.play()
    pygame.display.set_caption("Guitar Hero - Game")
    while True:
        screen.fill("Black")
        screen.blit(gameImg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    show_main_menu = True
                    showMainMenu()
                    break
                handle_input(event.key, lanes)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if backButton.input(mousePos):
                        pygame.mixer.music.pause()
                        show_main_menu = True
                        showMainMenu()

        screen.blit(gameImg, (0,0))
        mousePos = pygame.mouse.get_pos()
        backButton = Button(image=pygame.image.load("images/blackRect.gif"), pos=(965, 17),
                        textInput="BACK", font=pygame.font.Font("freesansbold.ttf", 15), baseColor="White", hoverColor="Green")
        backButton.changeColor(mousePos)
        backButton.update(screen)

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
                    if song_length == song_position:
                        #print(score)
                        finishGameMenu()
            else:
                spawn_timer += clock.get_time()

        for note in notes:
            note.update()
            note.draw(screen)

        # Basically where we detect when the notes have reached the limit (around 630pxs)
        if len(notes) > 0 and notes[0].y > 630:
            notes.pop(0)

        pygame.display.flip()
        clock.tick(80)


show_main_menu = True
def showMainMenu():
    global show_main_menu
    while show_main_menu:
        pygame.display.set_caption("Guitar Hero - Menu")


        screen.blit(menu, (0,0))

        menuMousePos = pygame.mouse.get_pos()
        menuTitle = pygame.font.Font("freesansbold.ttf", 100).render("Main Menu", True, "White")
        menuRect = menuTitle.get_rect(center=(WIDTH/2, 100))

        playButton = Button(image=pygame.image.load("images/greyButton.gif"), pos=(WIDTH/2, 250),
                            textInput="PLAY", font=pygame.font.Font("freesansbold.ttf", 75), baseColor="#A90BD7", hoverColor="White")
        quitButton = Button(image=pygame.image.load("images/greyButton.gif"), pos=(WIDTH/2, 600),
                            textInput="QUIT", font=pygame.font.Font("freesansbold.ttf", 75), baseColor="#A90BD7", hoverColor="White")

        screen.blit(menuTitle, menuRect)

        for button in [playButton, quitButton]:
            button.changeColor(menuMousePos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.input(menuMousePos):
                    gameLoop()
                if quitButton.input(menuMousePos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def finishGameMenu():
    global score
    pygame.mixer.music.pause()
    pygame.display.set_caption("Guitar Hero - Game Over")
    screen.blit(menu, (0,0))
    overTitle = pygame.font.Font("freesansbold.ttf", 100).render("Game Over!", True, "White")
    overRect =  overTitle.get_rect(center=(WIDTH/2, 200))
    scoreTitle = pygame.font.Font("freesansbold.ttf", 80).render(f"Your score is {score}", True, "White")
    scoreRect = scoreTitle.get_rect(center=(WIDTH/2, 400))
    screen.blit(overTitle, overRect)
    screen.blit(scoreTitle, scoreRect)

showMainMenu()
