import sys
sys.path.append('./Personaje')
sys.path.append('./Escenario')
sys.path.append('./Enemigos')
from Personaje import Personaje
from Personaje import *
from Escenario import Escenario
from Escenario import *
from Enemigos import Enemigos
from Enemigos import *
import pygame
#manejar niveles
class Manejador_niveles:
    nivel=1
    tam=50
    cc=Escenario.Constructor_columna()
    bloques=["","tierra","pasto","piedra","lava","pinchos"]
    co=[]
    fondo=pygame.image.load('Escenario/Imagenes/fondo1.png')
    #fondo=pygame.transform.scale(fondo,(500,1700))
    xAct=0
    def __init__(self):
        self.crear_escenario()
        self.xi=self.co[0].x
        self.xf=self.co[-1].x
    def crear_escenario(self):
        x=0
        y=0
        matriz=self.__crearMatriz()
        nombres=[]
        alturas=[]
        for i in range(len(matriz[1])-1):

            for m in matriz:
                if m[i]!=0:
                    nombres=nombres+[self.bloques[m[i]]]
                    alturas=alturas+[y]
                y=y+self.tam
            if  nombres!=[]:   
                self.co=self.co+[self.cc.getColumna(nombres,x,alturas)]
            nombres=[]
            alturas=[]
            x=x+self.tam
            
            y=0
        col=[]
        for c in self.co:
            if c.bloques is not None:
                col=col+[c]
        
        self.co=col        
                
    def __crearMatriz(self):
        m=open("Escenario/imagenes/nivel"+str(self.nivel)+".txt","r")
        lines=m.readlines()
        
        m.close()
        aux=[]
        for l in lines[:len(lines)-1]:
            aux=aux+ [list(l)[:len(list(l))-1]]
        aux=aux+[list(lines[len(lines)-1])]
        
        a=[]
        b=[]
        for c in aux:
            for d in c:
                if d!='\n':
                    a=a+[int(d)]
                    
            b=b+[a]
            a=[]
        
        return b


#manejo de logica del personaje   
class LogicaPersonaje:
    __proPer=[]
    logEne=None
    __manNiv=None
    def __init__(self,personaje,fabrica,__manNiv):
        self.personaje=personaje
        self.fabrica=fabrica
        self.__manNiv=__manNiv
        self.co=self.__manNiv.co
        self.__ubicar()
        self.xAct=self.personaje.x
    def getPersonaje(self):
        return self.personaje.getSprite()
    def mover(self,ancho):
        if not isinstance(self.personaje.estado,Personaje.Herido):
            if self.personaje.x+self.personaje.dx<=0:
                    self.personaje.x=0
            elif  self.personaje.x+50>=ancho:
                    self.personaje.x=ancho-50
            if not self.__detectarColision():
                    if self.__manNiv.xi==self.co[0].x and self.personaje.dx<0 or (self.personaje.dx>0 and self.personaje.x-50<=ancho//2):
                        self.personaje.x=self.personaje.x+self.personaje.dx
                        self.xAct=self.personaje.x    
                    elif ancho>=self.co[-1].x and self.personaje.dx>0 or (self.personaje.dx<0 and self.personaje.x-50>=ancho//2):
                        self.personaje.x=self.personaje.x+self.personaje.dx
                        self.xAct=self.personaje.x
                    else:
                    
                        self.xAct=self.xAct+self.personaje.dx
                        for c in self.co:
                            c.x=c.x-self.personaje.dx
                        self.logEne.mover_enemigos(-self.personaje.dx)
                        self.__manNiv.xAct=self.__manNiv.xAct-self.personaje.dx
                    
            self.personaje.setAccion("caminar")
    def __detectarColision(self):
        delta=-1
        ci=None
        if  self.personaje.dx<0:
            for c in self.co:
                if c.x<self.personaje.x:
                    if self.personaje.x-c.x<delta or delta<0:
                        delta=self.personaje.x-c.x
                        ci=c
        else:
            for c in self.co:
                if c.x>=self.personaje.x+50:
                    if c.x-self.personaje.x+50<delta or delta<0:
                        delta=c.x-self.personaje.x
                        ci=c
        if ci is not None:
                if ci.x+50>=self.personaje.x:
                    for b in ci.bloques:
                        if b.y<=self.personaje.y and b.y+50>=self.personaje.y:
                            return True
        return False
    def actualizar(self,pro,ene):
        if self.personaje.accion !='saltar' and self.personaje.dy<0:
            self.personaje.dy=0
        if self.personaje.cayendo:
            self.personaje.y=self.personaje.y+self.personaje.dy
            
            self.personaje.dy=self.personaje.dy+self.personaje.dvy
        
        cayendo=True
        for c in self.co:
            
            if c.x<=self.personaje.x and c.x+50>=self.personaje.x:
                
                for b in c.bloques:
                    
                    if b.y<=self.personaje.y+50 and b.y+50>self.personaje.y+50:
                        self.personaje.y=b.y-50
                        cayendo=False
                        self.personaje.dy=0
                        break
        self.personaje.cayendo=cayendo
        golpeado=False
        for pr in pro:
            
            if (pr.x<=self.personaje.x+50 and pr.x+50>=self.personaje.x) or (pr.x+50>=self.personaje.x and pr.x<=self.personaje.x+50):
               if (pr.y<=self.personaje.y+50 and pr.y+50>=self.personaje.y) or (pr.y+50>=self.personaje.y and pr.y<=self.personaje.y+50):
                golpeado=True
                
                if pr.tipo in self.personaje.debil:
                    self.personaje.vida=self.personaje.vida-20
                else:
                    self.personaje.vida=self.personaje.vida-10
                break
            
        if golpeado and isinstance(self.personaje.estado,Personaje.Normal) and self.personaje!='morir':
            if self.personaje.vida <=0:
                self.personaje.setAccion("morir")
            else:    
                self.personaje.setEstado(Personaje.Herido(self.personaje,200))


        for e in ene:
            
            golpeado=False
            if (e[1]<=self.personaje.x+50 and e[1]+50>=self.personaje.x) or (e[1]+50>=self.personaje.x and e[1]<=self.personaje.x+50):
               if (e[2]<=self.personaje.y+50 and e[2]+50>=self.personaje.y) or (e[2]+50>=self.personaje.y and e[2]<=self.personaje.y+50):
 
                    golpeado=True
                
                    break
        if golpeado and isinstance(self.personaje.estado,Personaje.Normal) and self.personaje!='morir':
            self.personaje.setEstado(Personaje.Herido(self.personaje,500))
           
            self.personaje.vida=self.personaje.vida-10
        self.logEne.actualizar()
        return not(self.personaje.accion=='morir' and self.personaje.indice==self.personaje.rango)
            
        
        


            
    def detener(self):
        self.personaje.setAccion("pararse")
        
    def saltar(self):
        if not self.personaje.cayendo:
            self.personaje.cayendo=True
            self.personaje.dy=self.personaje.dy1
            self.personaje.setAccion("saltar")
        
    def cambiarDireccion(self,direc):
        if self.personaje.direccion[0]!=direc[0]:
            self.personaje.setDireccion(direc)
    
    def __ubicar(self):
        y=self.co[0].bloques[0].y
        
        
        self.personaje.x=self.co[0].x
        self.personaje.y=y-50




#manejar la logica de los enemigos
        
class LogicaEnemigos:
    enemigo=Enemigos.Poblacion()
    def __init__(self,p,co,nivel):
        self.p=p
        self.co=co
        self.nivel=nivel
        self.leerEnemigos()
        self.pro=[]
    def leerEnemigos(self):
        r=open('Enemigos\enemigos_nivel1.txt','r')
        f=r.readlines()
        r.close
        lista=[]
        for l in f:
            lista=lista+[l.split()]
        fabrica=None    
        for l in lista:
            if l[0]=='chuchu':
                fabrica=Enemigos.Fabrica_chuchu.getInstance()
            elif l[0]=='rana':
                fabrica=Enemigos.Fabrica_rana.getInstance()
            elif l[0]=='mothfire':
                fabrica=Enemigos.Fabrica_mothfire.getInstance()    
            x=int(l[1])
            y=int(l[2])
            
                            
            p=fabrica.getEnemigo(x,y)
            self.enemigo.agregar(p)
        
    def GetEnemigos(self):
        aux=[]
        
        for c in self.enemigo.poblacion:
            i=c.get_sprite()
            x=c.x
            y=c.y
            aux=aux+[[i,x,y]]
            
        return aux    
    def mover_enemigos(self,dx):
        self.enemigo.trasladar(dx)
    def actualizar(self):
        self.enemigo.ia(self.p,self.co)
        self.enemigo.movimiento(self.p,self.co)
        for pr in self.pro:
            pr.mover()
        for p in self.enemigo.poblacion:
            if p.lanza():
                self.pro=self.pro+[p.get_proyectil()]
        
        
    
