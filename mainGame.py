import initGame
import levelClass
import objectClass
import time
import random
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import sys, os, traceback
from math import *
#if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
screen_size = [800,600]

pygame.init()

def getG(x,y,data):
    g = 0
    for mass in data.currentLevel.masses:
        if mass.z>0:
            g += mass.mass/((d(x,y,0, mass.x,mass.y,mass.z))**2)
        else:
            g -= mass.mass/((d(x,y,0, mass.x,mass.y,mass.z))**2)
    return g

def d(x,y,z,xi,yi,zi):
    a = (x-xi)**2
    b = (y-yi)**2
    c = (z-zi)**2
    return (a+b+c)**(.5)

def resetCamera(data):
    if data.cameramode == 'first':
        data.camera_radius = 5
        data.camera_center = [data.me.x+data.me.radius,data.me.y,data.me.z]
        data.cameraPos = [data.camera_center[0]+data.camera_radius*cos(data.cameraAngle), data.camera_center[1]+ data.camera_radius * sin(data.cameraAngle), data.camera_center[2]+ data.camera_radius*sin(data.vertCamAngle)]
    else:
        data.camera_radius = data.cameraradius2
        data.camera_center = [data.me.x-18,data.me.y,6]#[data.me.x+(data.rows/4)*3,-data.cameraradius2,data.currentZ + 20] #data.camera_radius*cos(radians(30))*sin(radians(30))
        data.cameraPos = [data.me.x+10,data.me.y,0]#[data.me.x+(data.rows/4)*3,data.rows//2,data.currentZ]
def moveCamera(data,keysPressed):
    if keysPressed[K_u] and data.vertCamAngle< pi/2:
        data.vertCamAngle +=.1
        resetCamera(data)
    if keysPressed[K_d] and data.vertCamAngle>= -pi/2:
        data.vertCamAngle -=.1
        resetCamera(data)

def sizeMass(data,sign):
    if len(data.masses)>0 and data.masses[-1].x>data.me.x+data.rows:
        data.masses[-1].mass += sign*3
        data.masses[-1].radius += sign/10
        data.masses[-1].createObject()
        data.me.resetMe(data)

POINTS = 0

def get_input(data):
    global POINTS
    mouse_position = pygame.mouse.get_pos()
    keysPressed = pygame.key.get_pressed()
    data.me.move(data,keysPressed)
    moveCamera(data,keysPressed)
    if keysPressed[K_UP]:
        pass
        #sizeMass(data, +1)
    elif keysPressed[K_DOWN]:pass
        #data.jumpTime = data.gameTime  
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                POINTS += data.points
                return False
            if event.key == pygame.K_RETURN and data.dead:
                POINTS += data.points
                initGame.GravInit(data)
                data.dead = False
            if event.key == pygame.K_p:
                data.pause = not data.pause
            if event.key == K_o:
                data.depth -= 1
                data.cols += 1
                data.currentLevel.depth -=1
                data.currentLevel.getColor()
                data.been.append((data.depth,0))
            if event.key == pygame.K_RSHIFT:
                if data.cameramode == 'first': data.cameramode = 'third'
                else: data.cameramode = 'first'
                resetCamera(data)
            # if event.key == pygame.K_UP:
            #     if not data.jumpBool:   #no double jumps
            #         data.jumpTime = data.gametime
            #         data.jumpBool = True
            #         data.jumpX = data.me.x
            if event.key == pygame.K_SPACE:
                if data.mode==1:
                    data.me.z -= 2*data.me.radius
                    data.mode = -1
                else: 
                    data.mode=1 
                    data.me.z += 2*data.me.radius   
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:pass
                #mouseX,mouseY = pygame.mouse.get_pos()
                #data.pointerx,data.pointery,data.pointerz = get3DPos(mouseX,mouseY)
                #print(abs(data.pointerz-data.currentZ))
                #createMass(data)
    return True

def get3DPos(mouseX,mouseY):
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    win_x,win_y = mouseX,screen_size[1]-mouseY
    win_z = glReadPixels(win_x,win_y,1,1,GL_DEPTH_COMPONENT,GL_FLOAT)
    cursor_x,cursor_y,cursor_z = gluUnProject(win_x,win_y,win_z,modelview,projection,viewport)
    return cursor_x,cursor_y,cursor_z
####################################################################

def drawGround(data):
    for i in range(len(data.edgex)):
        pair1 = data.edgex[i]
        glVertex3fv(pair1[0])
        glVertex3fv(pair1[1])
    for i in range(len(data.edgey)):
        pair2 = data.edgey[i]
        glVertex3fv(pair2[0])
        glVertex3fv(pair2[1])
      
def drawPath(data):
    if data.cameramode=='first': z = 25
    else: z = 14
    lastX = data.me.x + 100
    lastZ = z
    lasty = data.me.y + 50 
    for i in range(len(data.been)):
        if i != len(data.been)-1:
            thisy = lasty - (data.been[i][1])/2
            thisZ = z - data.been[i+1][0]
            glVertex3fv((lastX,lasty,lastZ))
            glVertex3fv((lastX,thisy,lastZ))
            glVertex3fv((lastX,thisy,lastZ))
            glVertex3fv((lastX,thisy,thisZ))
            lasty = thisy
            lastZ = thisZ
        else:
            thisy = lasty - ((data.been[i][1]) + 1)/2
            thisZ = z - data.been[i][0]
            glVertex3fv((lastX,lasty,lastZ))
            glVertex3fv((lastX,thisy,lastZ))
            glVertex3fv((lastX,thisy,lastZ))
            glVertex3fv((lastX,thisy,thisZ))

def drawText(position, textString,size,data):     
    font = pygame.font.Font (None, size)
    textSurface = font.render(textString, True, data.currentLevel.gc2, data.currentLevel.cC2) 
    #textSurface = deep    
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def oglDraw(data):
    cC = data.currentLevel.cC
    glClearColor(cC[0],cC[1],cC[2],cC[3])
    #glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #necessary
    glViewport(0,0,screen_size[0],screen_size[1]) #non-necessary
    gluPerspective(45, float(screen_size[0])/float(screen_size[1]), 0.1,200.0) #necessary
    glMatrixMode(GL_MODELVIEW) #necessary
    glLoadIdentity() #necessary
    gluLookAt(data.camera_center[0],data.camera_center[1],data.camera_center[2],data.cameraPos[0],data.cameraPos[1],data.cameraPos[2],0,0,1)
    glBegin(GL_LINES)
    glColor3fv((1,.1,1))
    drawPath(data)
    #glColor3fv((1,0,0))
    #data.lineBall.drawObject(data)
    glColor3fv(data.currentLevel.gc)
    drawGround(data)
    glColor3fv((0,0,1))
    data.me.drawObject(data)
    glColor3fv((0,0,0))
    data.currentLevel.draw(data)
    glEnd()
    text(data)
   
    pygame.display.flip()

def text(data):
    drawText((data.me.x+50,data.me.y,15),'Time Remaining: %d' %(data.lifeLength-data.gametime/30),50,data)
    drawText((data.me.x+50,data.me.y,11.5),'Depth: %d' %(data.depth),50,data)
    if data.cameramode=='first':
        drawText((data.me.x+50,data.me.y-11,11.5),'Points: %d' %(data.points),50,data)
    else:
        drawText((data.me.x+50,data.me.y-14.5,11.5),'Points: %d' %(data.points),50,data)
    if data.cameramode == 'first':
        drawText((data.me.x+100,data.me.y+50,30),'MINIMAP',50,data)
    else:
        drawText((data.me.x+100,data.me.y+50,20),'MINIMAP',50,data)
    if data.dead:
        drawText((data.me.x+50,data.me.y+20,5),'GAME OVER',100,data)
        drawText((data.me.x+50,data.me.y+20,2),'Press Enter to play again.',50,data)
        drawText((data.me.x+50,data.me.y+20,-1),'Press Esc to return to main menu.',50,data)

def timerFired(data):
    if not data.pause and not data.dead:
        if (data.me.x+.5)%40==0:
            data.currentLevel.addOrbs(data)
        if (data.me.x+.5)%20==0:
            data.currentLevel.placeMass(data)
        resetEdgex(data)
        resetEdgey(data)
        data.me.move(data)
        #data.lineBall.move(data)
        data.me.collision(data)
        data.been[-1] = (data.been[-1][0],data.been[-1][1] + 1/20)
        resetCamera(data)
        data.currentLevel.removeOrbs(data)
        checkDead(data)

def checkDead(data):
    if data.lifeLength-(data.gametime/30)==0:
        data.dead = True
    if data.depth == 0:
        data.gametime=0
        
def resetEdgex(data):
    x = data.edgex[-1][0][0] + 1
    for col in range(data.cols-1):
        y = col
        g1 = getG(x,y,data)
        g2 = getG(x,y+1,data)
        data.edgex.append(((x,y,g1),(x,y+1,g2)))
        data.edgex.pop(0)

def resetEdgey(data):
    x = data.edgey[-1][1][0]
    for col in range(data.cols):
        y = col
        g1 = getG(x,y,data)
        g2 = getG(x+1,y,data)
        data.edgey.append(((x,y,g1),(x+1,y,g2)))
        data.edgey.pop(0)

def main(lifeLength):
    initGame.displayInit()
    class Struct(object): pass
    data = Struct()
    data.colstart = 0
    data.lifeLength = lifeLength
    initGame.GravInit(data)
    clock = pygame.time.Clock()
    data.seconds = 0
    data.gametime = 0
    tick = 30
    while True:
        if not get_input(data): break
        timerFired(data)
        oglDraw(data)
        if not data.dead:
            data.gametime += 1
        clock.tick(tick)
        

    #pygame.mixer.music.stop()
    #return POINTS
        
    pygame.quit()

lifeLength = 10

if __name__ == "__main__":
    try:
        main(lifeLength)
    except:
        traceback.print_exc()
        pygame.quit()
        input()




