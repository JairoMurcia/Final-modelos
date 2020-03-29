import sys
sys.path.append('./Personaje')
from Personaje import Personaje
from Personaje import *
import pygame as py
class Controlador_vp:
    fabrica=Personaje.Fabrica_deku().getInstance()
    p=fabrica.getPersonaje()
    fabrica.setProyectil(2)
    p=Personaje.Escudo(p)
    nombre=["deku","goron","gerudo","zora"]
    i=0
    k=1
    def correr_indice(self,ind):
        if self.i+ind<0:
            self.i=len(self.nombre)-1
        else:    
            self.i=(self.i+ind)%len(self.nombre)
        if(self.nombre[self.i]=="deku"):
            self.fabrica=Personaje.Fabrica_deku.getInstance()
        elif (self.nombre[self.i]=="goron"):
            self.fabrica=Personaje.Fabrica_goron.getInstance()
        elif (self.nombre[self.i]=="gerudo"):
            self.fabrica=Personaje.Fabrica_gerudo.getInstance()
        elif (self.nombre[self.i]=="zora"):
            self.fabrica=Personaje.Fabrica_zora.getInstance()
        self.p=self.fabrica.getPersonaje()
        self.p=Personaje.Escudo(self.p)
        self.fabrica.setProyectil(1)
        self.k=1
            
    def correr_pro(self):
        if self.k==1:
            self.k=2
        else:
            self.k=1
            
        self.fabrica.setProyectil(self.k)
        
    def getPersonaje(self):    
        return self.p.getSprite()
    def getProyectil(self):
        
        return self.p.get_proyectil().get_sprite()
    def getEscudo(self):
        
        return self.p.get_escudo()
    def iniciar(self):
        print("asd")
