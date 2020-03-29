from pygame import image
from abc import ABCMeta
import copy
import sys
sys.path.append('./Personaje')
sys.path.append('./Escenario')
from Personaje import Personaje
from Personaje import *
from Escenario import Escenario
from Escenario import *



class Enemigo:
    __metaclass__=ABCMeta
    x=0
    y=0
    vida=20
    tipo=""
    proyectil=None
    dx=0
    dy=0
    direccion="izquierda"
    proyectil=None
    ruta="Enemigos\imagenes\\"
    indice=1
    estado=None
    accion="pararse"
    rango=4
    nombre=""
    debil=[]
    dvy=2
    cayendo=False
    es_parabolico=False
    def get_proyectil(self):
        p=self.proyectil.clonar()
        if self.direccion[0]=='i':
            p.x=self.x
            p.dx=p.dx*-1
        else:
            p.x=self.x+50
            
        p.y=self.y+25    
        if self.es_parabolico:
            return ProParaE(p)
        return p
    def get_sprite(self):
        return self.estado.getSprite()
    def getSprite(self):
        r=self.ruta+self.direccion[0]+str(self.indice)+".png"
        self.avanza()
        return image.load(r)
    def avanza(self):
        self.indice=((self.indice+1)%self.rango)+1
    def lanza(self):
        pass

    def ia(self,personaje,co):
        if personaje.x<self.x:
            self.direccion="izquierda"
            if self.dx>0:
                self.dx=self.dx*-1
        else:
            self.direccion="derecha"
            if self.dx<0:
                self.dx=self.dx*-1





        if personaje.y+50>self.y:
            self.definir_ataque(personaje,co)
        else:
            self.definir_accion()
             
class Rana(Enemigo):

    def __init__(self,proyectil,x,y):
        self.proyectil=proyectil
        self.dx=0
        self.dy=0
        self.dx1=20
        self.dy1=-32
        self.x=x
        self.y=y
        self.debil=["electrico","piedra"]
        self.accion="pararse"
        self.actual="pararse"
        self.asignarRango()
        self.nombre="rana"
#asignar ruta y rango de la rana        
    def asignarRango(self):
        if self.actual!=self.accion:
            self.actual=self.accion
            self.indice=1
        if self.accion=="pararse":
            self.rango=4
            self.ruta="Enemigos/imagenes/rana/pararse"
            self.dx=0
        elif self.accion=="saltar" :
            self.rango=1
            
            self.ruta="Enemigos/imagenes/rana/saltar"
            if not cayendo:
                self.dy==self.dy1
                cayendo=True
                self.dy=self.dy1
                self.dx=self.dx1
        elif self.accion=="escudarse":    
            self.ruta="Enemigos/imagenes/rana/escudarse"
            self.rango=1
            
            self.dx=0
        elif self.accion=="atacarsaltar" or self.accion=="atacarsaltarparabolico" :
            self.rango=3
            self.indice=1
            if self.accion=="atacarsaltarparabolico":
                self.es_parabolico=True
            else:
                self.es_parabolico=False
            if not self.cayendo:
                self.dy==self.dy1
                cayendo=True
                self.ruta="Enemigos/imagenes/rana/atacarsaltar"
                self.dy=self.dy1
                self.dx=self.dx1
            self.ruta="Enemigos/imagenes/rana/atacarsaltar"
        elif self.accion=="atacar" or  self.accion=="atacarparabolico":
             self.rango=3
             self.ruta="Enemigos/imagenes/rana/atacar"
             
             if self.accion=="atacarparabolico":
                self.es_parabolico=True
             else:
                self.es_parabolico=False

        

#definir ataque
    def definir_ataque(self,personaje,co):
        if personaje.x<self.x:
            n=-1
        else:
            n=1
        atacar=True    
        for c in co:
            if c.x>self.x*n:
                for b in c.bloques:
                    if b.y<=self.y and b.y+50>=self.y:
                        atacar=False
        if atacar:
            self.accion="atacar"
        else:
            self.accion="atacarparabolico"
        self.asignarRango()
#asignar accion        
    def definir_accion(self):
        self.accion="atacarsaltarparabolico"
#saber si lanza
    def lanza(self):
        if self.accion=="atacar" or self.accion=="atacarparabolico" or self.accion=="atacarsaltar" or self.accion=="atacarsaltarparabolico" :
            return self.rango== self.indice 
        self.rango
class Chuchu(Enemigo):

    def __init__(self,proyectil,x,y):
        self.proyectil=proyectil
        self.dx=20
        self.dy=0
        self.dy1=23
        self.x=x
        self.y=y
        self.nombre="chuchu"
        self.debil=["agua","piedra","metal"]
    def asignarRango():
        self.rango=4   

class Mothfire(Enemigo):

    def __init__(self,proyectil,x,y):
        self.proyectil=proyectil
        self.dx=20
        self.dy=0
        self.dy1=23
        self.x=x
        self.y=y
        self.nombre="mothfire"
        self.debil=["agua","electrico"]
    def asignarRango(self):
        if self.accion=="pararse" :
            self.rango=4
            
        elif self.accion=="atacar":
            self.rango=4
        elif self.accion=="escudarse":
            self.rango=1
            
        
class Poblacion:
    poblacion=[]
    def agregar(self,enemigo):
        self.poblacion=self.poblacion+[enemigo]

    def ia(self,personaje,co):
        
        for p in self.poblacion:
              if  abs(p.x-personaje.x)<=2000:
                  p.ia(personaje,co)
               
    def trasladar(self,dx):
        for p in self.poblacion:
            p.x=p.x+dx
    def movimiento(self,personaje,co):
        for p in self.poblacion:
            mover=True  

           
            for c in co:
                ci=None
                          
#seccion para indicar si estan sobre una plataforma
                cayendo=True
                if p.dy>0:
                    if c.x<=p.x and c.x+50>=p.x:
                        for b in c.bloques:
                            if b.y<=p.y+50:
                               p.dy=0
                               p.cayendo=False 
                        
                    
#detectar colisiones
                delta=-1
                if p.dx>0:
                    if c.x<=p.x+50 :
                        if p.x-c.x<delta or delta<0:
                            ci=c
                            delta=sp.x-c.x
                            
                elif p.dx<0:
                    if c.x+50>=self.x :
                        if c.x-p.x<delta or delta<0:
                            ci=c
                            delta=c.x-p.x

            if ci is not None:
                for b in ci.bloques:
                    if b.y<=self.personaje.y and b.y+50>=self.personaje.y:
                            mover=False
                            break

            p.cayendo=cayendo                        
            if mover:
                p.x=p.x+p.dx
            if p.cayendo and p.nombre!="mothfire":
                p.y=p.y+p.dy
                p.dy=p.dy+p.dvy
#proyectiles
class Proyectil_e:
    __metaclass__=ABCMeta
    x=0
    y=0
    dx=0
    ruta=""
    tipo=""
    def getSprite(self):
        return image.load(self.ruta)
    def mover(self):
        self.x=self.x+self.dx

    def clonar(self):
        return copy.copy(self)
class Pro_chuchu(Proyectil_e):

    def __init__(self):
        self.dx=10
        self.ruta="Enemigos/imagenes/chuchu/pro.png"
        self.tipo="electrico"
class Pro_rana(Proyectil_e):

    def __init__(self):
        self.dx=9
        self.ruta="Enemigos/imagenes/rana/pro.png"
        self.tipo="agua"
class Pro_mothfire(Proyectil_e):
        def __init__(self):
            self.dx=11
            self.ruta="Enemigos/imagenes/mothfire/pro.png"
            self.tipo="fuego"
class ProParaE(Proyectil_e):
        def __init__(self,pro):
            self.pro=pro    
            self.dx=pro.dx
            self.ruta=pro.ruta
            self.tipo=pro.tipo
            self.dy=-20
            self.dvy=5
            self.x=pro.x
            self.y=pro.y
        def getSprite(self):
            return image.load(self.ruta)
        def mover(self):
            self.pro.mover()
            self.x=self.pro.x
            self.y=self.y+self.dy
            self.dy=self.dy+self.dvy

        
#estados de los enemigos
class Estado:
    
        __metaclass__=ABCMeta
        personaje=None
        def getSprite(self):
            pass
class Normal(Estado):
    def __init__(self,personaje):
        self.personaje=personaje
    def getSprite(self):
        return self.personaje.getSprite()

class Golpeado():    
    def __init__(self,personaje):
        self.personaje=personaje
    def getSprite(self):
        if self.personaje.nombre=="rana" and self.personaje.accion!="saltar":
            r="Enemigos\imagenes\rana\golpeados"+self.personaje.direccion[0]+".png"
        else:    
            r="Enemigos\imagenes\\"+self.personaje.nombre+"golpeado"+self.personaje.direccion[0]+".png"
        self.personaje.x=self.personaje.x-self.personaje.dx
        return image.load(r)
        
#fabrica enemigos
class Fabrica_enemigos:
    __metaclass__=ABCMeta
    instance=None
    def getEnemigo(self,x,y):
        pass
class Fabrica_chuchu(Fabrica_enemigos):

    @staticmethod
    def getInstance():
        if Fabrica_chuchu.instance is None:
            Fabrica_chuchu.instance=Fabrica_chuchu()
        elif not isinstance(Fabrica_chuchu.instance,Fabrica_chuchu):
            Fabrica_chuchu.instance=Fabrica_chuchu()
        return Fabrica_chuchu.instance
    
    def getEnemigo(self,x,y):
        e= Chuchu(Pro_chuchu(),x,y)
        e.estado=Normal(e)
        return e
class Fabrica_rana(Fabrica_enemigos):

    @staticmethod
    def getInstance():
        if Fabrica_rana.instance is None:
            Fabrica_rana.instance=Fabrica_rana()
        elif not isinstance(Fabrica_rana.instance,Fabrica_rana):
            Fabrica_rana.instance=Fabrica_rana()
        return Fabrica_rana.instance
    
    def getEnemigo(self,x,y):
        e= Rana(Pro_rana(),x,y)
        e.estado=Normal(e)
        return e
class Fabrica_mothfire(Fabrica_enemigos):

    @staticmethod
    def getInstance():
        if Fabrica_mothfire.instance is None:
            Fabrica_mothfire.instance=Fabrica_mothfire()
        elif not isinstance(Fabrica_mothfire.instance,Fabrica_mothfire):
            Fabrica_mothfire.instance=Fabrica_mothfire()
        return Fabrica_mothfire.instance
    
    def getEnemigo(self,x,y):
        e= Mothfire(Pro_mothfire(),x,y)    
        e.estado=Normal(e)
        return e


    
