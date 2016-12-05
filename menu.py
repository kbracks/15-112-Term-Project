import mainGame2 
import pygame
import time
import random
import datetime

pygame.init()

display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("KBP Term")
clock = pygame.time.Clock()
tree = pygame.image.load('Pics/home.jpg')
tree = pygame.transform.scale(tree,(display_width,display_height))
login = pygame.image.load('Pics/login.png')
login = pygame.transform.scale(login,(display_width,display_height))
helpPic = pygame.image.load('Pics/help.jpg')
helpPic = pygame.transform.scale(helpPic,(display_width,display_height))
terrain = pygame.image.load('Pics/terrain.jpg')
terrain = pygame.transform.scale(terrain,(display_width,display_height))
deep = pygame.image.load('Pics/999.jpg')
deep = pygame.transform.scale(deep,(display_width,display_height))
warp = pygame.image.load('Pics/warp2.jpg')
warp = pygame.transform.scale(warp,(display_width,display_height))


def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

class Text(object):
    def __init__(self,text,x,y,size,name = None):
        self.name = name
        self.text = text
        self.x = x
        self.originalY = y
        self.y = y
        self.size = size
        self.replace()
    def replace(self):
        self.y = self.originalY
        countLines = len(self.text.splitlines())
        if countLines>1:
            self.y -= self.size*countLines/4
    def textObj(self,text, font):
        textSurface = font.render(text, True, red)
        return textSurface, textSurface.get_rect()
    def draw(self):
        lineNum = 0
        y = self.y
        numLines = len(self.text.splitlines())
        # if self.size*numLines>display_height:
        #     self.size = display_height//numLines
        for line in self.text.splitlines():
            largeText = pygame.font.Font('freesansbold.ttf',self.size)
            TextSurf, TextRect = self.textObj(line, largeText)
            # while TextRect.width>display_width:
            #     self.size -= 5
            #     largeText = pygame.font.Font('freesansbold.ttf',self.size)
            #     TextSurf, TextRect = self.textObj(line, largeText)
            if lineNum >0: y+= self.size #pygame.font.Font.size(largeText)[1]
            TextRect.center = (self.x,y)
            gameDisplay.blit(TextSurf, TextRect)
            lineNum +=1
    def __hash__(self):
        return hash(self.text)


class Screen(object):
    def __init__(self, name, image=None):
        self.name = name
        self.buttons = set()
        self.image = image
        self.addButtons()
        self.texts = set()
    def addTexts(self,text,x,y,size=100,name=None):
        if name==None:
            self.texts.add(Text(text,x,y,size))
        else:
            self.texts.add(Text(text,x,y,size,name))
    def addButtons(self):
        if self.name == 'Home':
            self.buttons.add(Button('Info',20,20))
            self.buttons.add(Button('Play',20,90,))
            self.buttons.add(Button('Logout',20,160))
            self.buttons.add(Button('World\nStats',20,230))
            self.buttons.add(Button('Your\nStats',20,300))
        if self.name == 'Info':
            self.buttons.add(Button('Back',20,20))
            self.buttons.add(Button('Next',680,540))
        if self.name == 'Login':
            self.buttons.add(Button('Input',350,250))
            self.buttons.add(Button('New User',350,320))
            self.buttons.add(Button('Current\nUser',350,390))
        if self.name == 'Stats':
            self.buttons.add(Button('Back',20,20))

    def drawScreen(self):
        gameDisplay.fill(black)
        if self.image != None:
            gameDisplay.blit(self.image, (0,15))
        for text in self.texts:
            text.draw()
        for button in self.buttons:
            button.draw()

class Button(object):
    def __init__(self,message,x,y,action=None):
        self.x = x
        self.y = y 
        self.w = 100
        self.h = 50
        self.message = message
        self.text = Text(message,x+(self.w/2), y+(self.h/2),20)
        self.ac = bright_green
        self.c = green
    def __hash__(self):
        return hash((self.x,self.y,self.message))
    def clickedIn(self,data):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:
            if click[0] == 1:
                if self.message == 'Play':
                    playGame(data)
                if self.message == 'Info':
                    data.prevScreen = data.currentScreen
                    data.currentScreen = data.infoScreen
                if self.message == 'Back':
                    data.currentScreen = data.prevScreen
                if self.message == 'New User':
                    newUserFunction(data)
                if self.message == 'Current\nUser':
                    currentUserFunction(data)
                if self.message == 'Logout':
                    for text in data.statScreen.texts:
                        if text.name == 'user':
                            writeFile('User Database/%s' %(data.username+ '.txt'),text.text)
                    init(data)
                if self.message == 'Setup\nTerrain':
                    data.prevScreen = data.currentScreen
                    data.currentScreen = data.functionScreen
                if self.message == 'Your\nStats':
                    data.prevScreen = data.currentScreen
                    data.currentScreen = data.statScreen
                time.sleep(.2)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:
            pygame.draw.rect(gameDisplay, self.ac,(self.x,self.y,self.w,self.h))
        else:
            pygame.draw.rect(gameDisplay, self.c,(self.x,self.y,self.w,self.h))
        self.text.draw()
def currentUserFunction(data):
    users = readFile('User Database/users.txt')
    if data.username not in users or data.username == '':
        data.loginScreen.addTexts('Username does\nnot exist',550,350,20)
    else:
        text = readFile('User Database/%s' %(data.username+ '.txt'))
        data.statScreen.addTexts(text,display_width/2,100,50,'user') 
        data.currentScreen = data.homeScreen
        data.homeScreen.addTexts('Hey %s' %data.username,400,150)  
def newUserFunction(data):
    users = readFile('User Database/users.txt')
    if data.username in users:
        data.loginScreen.addTexts('Invalid',550,350,20)
    else:
        users += data.username + '\n'
        writeFile('User Database/users.txt',users)
        writeFile('User Database/%s' %(data.username+ '.txt'),'')
        data.statScreen.addTexts('',display_width/2,50,20,'user')
        data.currentScreen = data.homeScreen
        data.homeScreen.addTexts('Hey %s' %data.username,400,150)

def playGame(data):
    for text in data.statScreen.texts:
        if text.name=='user':
            text.text += '\n\n'+datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            gameScore= mainGame2.main(8)
            text.text += '\nScore:%d' %gameScore
            text.replace()

    
    pygame.display.set_mode((display_width,display_height))

def init(data):
    data.loginScreen = Screen('Login',warp)
    data.loginScreen.addTexts('Please Enter\nYour Username',display_width/2,300,50)
    data.statScreen = Screen('Stats')
    data.username = ''
    data.homeScreen = Screen('Home',tree)
    data.infoScreen = Screen('Info',deep)
    data.infoScreen.addTexts(readFile('infoscreen.txt'),display_width/2,display_height/4,25)
    data.currentScreen = data.loginScreen
    data.prevScreen = data.homeScreen

def game_intro(data):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and data.currentScreen==data.loginScreen:
                key = pygame.key.name(event.key)
                if event.key == pygame.K_BACKSPACE:
                    data.username = data.username[:-1]
                elif len(key)==1 and key.isalpha() and len(data.username)<9:
                    data.username += pygame.key.name(event.key)
                if len(data.username)==1: data.username = data.username.upper()
        data.currentScreen.drawScreen() 
        for button in data.currentScreen.buttons:
            if button.message == 'Input':
                button.text = Text(data.username,button.x+(button.w/2), button.y+(button.h/2),20)
            button.clickedIn(data)     
        pygame.display.update()
        clock.tick(15)

def main():
    class Struct(object): pass
    data = Struct()
    init(data)
    game_intro(data)
    pygame.quit()
    quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()