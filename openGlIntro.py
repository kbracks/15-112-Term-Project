from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import sys, os, traceback
screen_size = [800,600]
import objectClass

pygame.init()
# login = pygame.image.load('Pics/terrain.jpg')
# login = pygame.transform.scale(login,(screen_size[0],screen_size[1]))
tree = pygame.image.load('Pics/tree.png')
tree = pygame.transform.scale(tree,(screen_size[0],screen_size[1]))
home = pygame.image.load('Pics/home.jpg')
home = pygame.transform.scale(home,(screen_size[0],screen_size[1]))
# login = pygame.image.load('Pics/terrain.jpg')
# login = pygame.transform.scale(login,(screen_size[0],screen_size[1]))



def init1():
    pygame.display.init()
    #pygame.font.init()
    
    #screen_size = [1280,680]
    multisample = 0
    icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
    if multisample:
        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,multisample)
    pygame.display.set_mode(screen_size,OPENGL|DOUBLEBUF)
    #fpsClock = pygame.time.Clock()
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

def init2(data):
    data.cameraCenter = [0,0,0]
    data.cameraAnglex = 0
    data.cameraAngley = 0
    data.cameraRadius = 10
    data.cameraPos = [data.cameraRadius,0,0]
    data.login = objectClass.Object('up',5,10,0,0)




def drawText(position, textString,data):     
    font = pygame.font.Font (None, 60)
    textSurface = font.render(textString, True, (255,0,0,0), (0,0,0,0))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def drawImage(position, path,data):     
    font = pygame.font.Font (None, 60) 
    textSurface = path  
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def draw(data):
    #cC = data.currentLevel.cC
    glClearColor(0,0,0,0)
    #glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #necessary
    glViewport(0,0,screen_size[0],screen_size[1]) #non-necessary
    gluPerspective(45, float(screen_size[0])/float(screen_size[1]), 0.1,200.0) #necessary
    glMatrixMode(GL_MODELVIEW) #necessary
    glLoadIdentity() #necessary
    gluLookAt(data.cameraCenter[0],data.cameraCenter[1],data.cameraCenter[2],data.cameraPos[0],data.cameraPos[1],data.cameraPos[2],0,0,1)
    drawText((10,0,0),'hey!',data)
    # drawImage((10,0,0),login,data)
    # drawImage((10,-15,0),tree,data)
    # drawImage((10,15,0),home,data)
    #drawImage((10*cos(1),10*sin(1),0),login,data)
    glBegin(GL_LINES)
    data.login.drawObject(data)
    glEnd()
    pygame.display.flip()


def getInput(data):
    mouse_position = pygame.mouse.get_pos()
    keysPressed = pygame.key.get_pressed()
    if keysPressed[K_UP]:
        data.cameraCenter[0]+= cos(data.cameraAnglex)
        data.cameraCenter[1]+= sin(data.cameraAnglex)
        resetCamera(data)
    elif keysPressed[K_DOWN]:
        data.cameraCenter[0]-= cos(data.cameraAnglex)
        data.cameraCenter[1]-= sin(data.cameraAnglex)
        resetCamera(data)
    elif keysPressed[K_LEFT]:
        data.cameraAnglex += radians(1)
        resetCamera(data)
    elif keysPressed[K_RIGHT]:
        data.cameraAnglex -=radians(1)
        resetCamera(data)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
def resetCamera(data):
    x = data.cameraCenter[0]+ data.cameraRadius*cos(data.cameraAnglex)
    y = data.cameraCenter[1] + data.cameraRadius*sin(data.cameraAnglex)
    data.cameraPos[0],data.cameraPos[1],data.cameraPos[2] = x,y,0

def main():
    class Struct(object): pass
    data = Struct()
    init2(data)
    init1()
    clock = pygame.time.Clock()
    while True:
        getInput(data)
        draw(data)
        clock.tick(30)
    pygame.quit()
    quit()

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()