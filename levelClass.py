import random
import objectClass

class Level(object):
    def __init__(self,depth,data,parent = None):
        self.parent = parent
        self.depth = depth
        self.masses = set() #adding and removing good
        self.numChildren = random.randint(3,4)
        self.downOrb = []
        self.magicOrb = set()
        self.upOrb = set()
        self.getColor()
        self.gc = (random.random(),random.random(),random.random())#(.627,.32,.17)
        self.gc2 = (self.gc[0]*255,self.gc[1]*255,self.gc[2]*255)

    def getColor(self):
        cC = [1,1,1,1]
        for i in range(self.depth):
            for i in range(3):
                cC[i] -= .2
                #if cC[i] < 0: cC[i] = 0
        self.cC = tuple(cC)
        self.cC2 = (self.cC[0]*255,self.cC[1]*255,self.cC[2]*255)
    def placeMass(self,data):
        y = random.randint(1,data.cols-1)
        sign = random.choice([-1,1])
        z = 4*sign
        x = data.me.x+80
        newmass = objectClass.Object('mass',1,x,y,z)
        self.masses.add(newmass)
        z = sign*newmass.mass/(z**2) + (-sign*(newmass.radius))
        return x,y,z
    def addOrbs(self,data):
        x,y,z = self.placeMass(data)
        #####################################
        if self.depth==0: type = 'down'
        elif data.lifeLength-(data.gametime/30)<15:
            type = 'up'
        else: 
            type = random.choice(['up','down'])
        if type == 'down' and self.depthProb():
            newmass = objectClass.Object('magic',1,x,y,z)
            self.magicOrb.add(newmass)
            data.allOrbs.append(newmass)
        else:
            if type == 'up':
                self.placeUpOrb(x,y,z,data)
            else:
                self.placeDownOrb(x,y,z,data)#if self.checkThem(data):
    def placeDownOrb(self,x,y,z,data):
        if self.numChildren!=0:
            print(len(self.downOrb))
            self.numChildren -= 1
            thisOrb = objectClass.Object('down',1,x,y,z)
            self.downOrb.append(thisOrb)
            data.allOrbs.append(thisOrb)
        else: 
            if self.check(data):
                self.downOrb[0].x = x
                self.downOrb[0].y = y
                self.downOrb[0].z = z
                thisOrb = self.downOrb.pop(0)
                thisOrb.createObject()
                self.downOrb.append(thisOrb)
                data.allOrbs.append(thisOrb)
    def placeUpOrb(self,x,y,z,data):
        new = objectClass.Object('up',1,x,y,z)
        self.upOrb.add(new)
        data.allOrbs.append(new)
    def check(self,data):
        orb = self.downOrb[0]
        if orb.x<data.me.x-data.rows/4:
            return True
        return False
    def depthProb(self):
        nums = set()
        while len(nums)<= (self.depth+1)*2:
            num = random.randint(0,15)
            nums.add(num)
        return self.depth in nums
    def draw(self,data):
        for orb in self.downOrb:
            orb.drawObject(data)
        for orb in self.upOrb:
            orb.drawObject(data)
        for orb in self.magicOrb:
            orb.drawObject(data)

    def removeOrbs(self,data):
        for mass in self.masses:
            if mass.x<data.me.x-data.rows/3:
                self.masses.remove(mass)
                break
        for orb in self.magicOrb:
            if orb.x<data.me.x-data.rows/3:
                self.magicOrb.remove(orb)
                break
        for orb in data.allOrbs:
            if orb.x<data.me.x-data.rows/3:
                data.allOrbs.remove(orb)
                break
        for orb in self.upOrb:
            if orb.x<data.me.x-data.rows/3:
                self.upOrb.remove(orb)
                break


