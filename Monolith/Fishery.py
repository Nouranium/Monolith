'''
Created on 1 Aug 2015

@author: NoNotCar
'''
import Img
import Entity
import Object
import Tools
import Buyers
import Mech
import Vehicles
import pygame
from random import randint
def imgref2(fil):
    return Img.imgret2("Fishery/"+fil)
class Fish(Entity.ResourceB):
    img=imgref2("Fish.png")
    value=20
    name="Fish"
class FishSp(Entity.ResourceB):
    img=imgref2("SpFish.png")
    value=300
    name="Special Fish"
class FishPoo(Entity.ResourceB):
    img=imgref2("FWaste.png")
    value=-1000
    name="FishPoo"
class FishingRod(Tools.Tool):
    img=imgref2("Fishingrod.png")
    def use(self,x,y,w,p):
        if w.get_terr(x,y).iswasser and not p.hand:
            if not randint(0,5):
                p.hand=Fish(x,y)
            return True
class Fisher(Object.OObject):
    is3d=True
    img=imgref2("Shocker.png")
    hasio="output"
    updatable=True
    doc="Shocks fish in the water below it and output them. Must be placed in water (obviously). Consumes 100W. IO: Output"
    def __init__(self,x,y,owner):
        Object.OObject.__init__(self,x,y,owner)
        self.idle=randint(360,600)
        self.output=[]
    def update(self,world):
        if self.owner.get_power(100):
            if self.idle:
                self.idle-=1
            else:
                if not self.output:
                    self.output.append(Fish(self.x,self.y) if randint(0,20) else FishSp(self.x,self.y))
                self.idle=randint(360,600)
class FishFarm(Object.OObject):
    is3d=True
    img=imgref2("FISHTANK.png")
    imga=imgref2("ALGALTANK.png")
    hasio="2both"
    updatable=False
    off3d=12
    algal=False
    doc="When a fish is inputed into this machine a lot of fish are produced, with harmful fish waste. 2x2 Object. IO: Both (2 outputs)"
    def __init__(self,x,y,owner):
        Object.OObject.__init__(self,x,y,owner)
        self.delay=randint(2000,4000)
        self.poodelay=randint(1000,2000)
        self.output=[]
        self.output2=[]
    def update(self,world):
        if self.algal:
            self.updatable=False
        self.delay-=1
        self.poodelay-=1
        if self.delay==0:
            self.output.extend([Fish(self.x,self.y) for x in range(randint(64,128))])
            self.updatable=False
            self.delay=randint(2000,4000)
        if self.poodelay==0:
            if not self.output2:
                self.output2.append(FishPoo(self.x,self.y))
                self.poodelay=randint(1000,2000)
            else:
                self.algal=True
    def input(self,ent):
        if ent.name=="Fish" and not self.updatable:
            self.updatable=True
            return True
        return False
    def get_img(self,world):
        if self.updatable and not self.algal:
            imgc=self.img.copy()
            for _ in range(4):
                pygame.draw.rect(imgc,(255,255,255),pygame.Rect(randint(4,58),randint(4,58),2,2))
            return imgc
        elif self.algal:
            return self.imga
        return self.img
class FloatBuyer(Buyers.ObjBuyer):
    def buy(self, world, tx, ty, p):
        if world.is_placeable(tx, ty,True):
            world.spawn_obj(self.objclass(tx, ty, 
             p))
            return True
        return False
class FFBuyer(Buyers.ObjBuyer):
    img=imgref2("FTank.png")
    def buy(self, world, tx, ty, p):
        if all([world.is_placeable(tx, ty), world.is_placeable(tx+1, ty),world.is_placeable(tx, ty+1),world.is_placeable(tx+1, ty+1)]):
            ff=FishFarm(tx, ty, p)
            world.spawn_obj(ff)
            world.spawn_obj(Mech.MultiBlock(tx+1, ty,ff))
            world.spawn_obj(Mech.MultiBlock(tx, ty+1,ff))
            world.spawn_obj(Mech.MultiBlock(tx+1, ty+1,ff))
            return True
        return False
    def get_img(self, world):
        return self.img
class FisheryTab(object):
    img=imgref2("Fish.png")
    iscat=True
    doc="Fishing apparatus"
    def __init__(self):
        self.menu=[FloatBuyer(Fisher,500),FFBuyer(FishFarm,500),Buyers.VBuyer(Vehicles.Boat,500),Buyers.BridgeBuyer()]
            