import abc
from pygame import image
from abc import ABCMeta
import copy
#seccion de personajes
class Personaje:
    __metaclass__=ABCMeta
    x=0
    y=0
    dx=1
    dy=1
    dy1=1
    dvy=10
    direccion="d"
    accion="pararse"
    nombre=""
    sprites=[]
    indice=1
    rango=1
    proyectil=None
    instance=None
    estado=None
    cayendo=False
    debil=[]
    vida=100
        #metodo abstracto para definir rango
    
    def get_sprite(self):
        self.avanza()
        if self.cayendo or self.accion=="saltar_atacar":
            accion="saltar"
            return image.load("Personaje/imagenes/"+self.nombre+"/saltar"+self.direccion[0]+"1.png")
        elif self.accion=="caminar_atacar":    
            accion="caminar"
        else:
            accion=self.accion
        ruta="Personaje/imagenes/"+self.nombre+"/"+accion+""+self.direccion[0]+""+str(self.indice)+".png"
        
        return image.load(ruta)
    
    def getSprite(self):
        return self.estado.get_sprite()
    def setEstado(self,e):
        self.estado=e
    def setAccion(self,accion):
        if self.accion!=accion:
            
            self.indice=1
            self.accion=accion
            self.asignarRango()
    def avanza(self):
        self.indice=((self.indice+1)%self.rango) +1
    def setProyectil(self,pr):
        self.proyectil=pr
    def get_proyectil(self):
        return self.proyectil.clonar()
    def setDireccion(self,direc):
        self.direccion=direc
        if direc[0] == 'i' and self.dx>0:
            self.dx=self.dx*-1
        elif direc[0]=='d' and self.dx<0:
             self.dx=self.dx*-1
    def asignarRango(self):
        if self.accion=='atacar':
            self.rango=2
        elif self.accion=='pararse' or self.accion=='escudarse' or self.accion=='saltar' or self.accion=='saltar_atacar':
            self.rango=1
        elif self.accion=='caminar_atacar' or self.accion=='caminar':
            self.rango=4
        elif self.accion=='morir':
            if self.nombre=='deku' or self.nombre=='goron':
                self.rango=4
            else:
                self.rango=3
    
#personaje deku       
class Deku(Personaje):
    def __init__(self):
        self.nombre="deku"
        self.indice=1
        self.dx=20
        self.dy=-50
        self.dy1=-50
        self.debil=["fuego"]
    @staticmethod
    def getInstance():
        if Deku.instance is None:
            Deku.instance=Deku()
        elif Deku.instance.nombre!="deku":
            Deku.instance=Deku()
        return Deku.instance    

    



#personaje goro    
class Goron(Personaje):
    def __init__(self):
        self.nombre="goron"
        self.indice=1
        self.dx=18
        self.dy=-48
        self.dy1=-48
        self.debil=["electrico"]
    @staticmethod
    def getInstance():
        if Goron.instance is None:
            Goron.instance=Goron()
        elif Goron.instance.nombre!="goron":
            Goron.instance=Goron()
    
        return Goron.instance


#personaje gerudo
class Gerudo(Personaje):
    def __init__(self):
        self.nombre="gerudo"
        self.indice=1
        self.dx=22
        self.dy=-48
        self.dy1=-48
        self.debil=["agua"]
    @staticmethod
    def getInstance():
        if Gerudo.instance is None:
            Gerudo.instance=Gerudo()
        elif Gerudo.instance.nombre!="gerudo":
            Gerudo.instance=Gerudo()
        return Gerudo.instance


    



#personaje zora    
class Zora(Personaje):
    def __init__(self):
        self.nombre="zora"
        self.indice=1
        self.dx=22
        self.dy=-49
        self.dy1=-49
        self.debil=["electrico"]
    @staticmethod
    def getInstance():
        if Zora.instance is None:
            Zora.instance=Zora()
        elif Zora.instance.nombre!="zora":
            Zora.instance=Zora()
        return Zora.instance

    

#decorador escudo
class Escudo(Personaje):
    
    def __init__(self,personaje):
        self.personaje=personaje
        self.tipo="madera"
        self.delegado=E_goron(personaje)
        self.dx=self.personaje.dx
        self.x=self.personaje.x
        self.y=self.personaje.y
        self.dy=self.personaje.dy
        self.dy1=self.personaje.dy1
    def getSprite(self):
               
        return self.personaje.getSprite()

    
    def setProyectil(self,pr):
        self.personaje.setProyectil(pr)
    def get_proyectil(self):
        return self.personaje.get_proyectil()
    def get_sprite(self):
        ruta="Personaje\imagenes\\"+self.personaje.nombre+"\em.png"
        return image.load(ruta)
    def get_escudo(self):
        if isinstance(self.personaje,Deku):
            return self.get_sprite()
        else:
            return self.delegado.get_escudo()
#primer delegado        
class E_goron(Escudo):
    def __init__(self,personaje):
        self.personaje=personaje
        self.tipo="piedra"
        self.delegado=E_gerudo(personaje)
        
    def get_escudo(self):
        if isinstance(self.personaje,Goron):
            return self.get_sprite()
        else:
            return self.delegado.get_escudo()



#segundo delegado    
class E_gerudo(Escudo):
    def __init__(self,personaje):
        self.personaje=personaje
        self.tipo="electrico"
        self.delegado=E_zora(personaje)
        
    def get_escudo(self):
        if isinstance(self.personaje,Gerudo):
            return self.get_sprite()
        else:
            return self.delegado.get_escudo()
#tercer delagado
class E_zora(Escudo):
    def __init__(self,personaje):
        self.personaje=personaje
        self.tipo="electrico"
        self.delegado=None
        
    def get_escudo(self):
        if isinstance(self.personaje,Zora):
            return self.get_sprite()
        else:
            ruta="Personaje\imagenes\deku\pararsed1.png"
            return image.load(ruta)      




            
#seccion de fabrica abstracta       
class Fabrica_personaje:
    __metaclass__=ABCMeta
    
    instance=None
    @abc.abstractmethod
    def getPersonaje(self):
        pass
    def getProyectil(self):
        pass
    @abc.abstractmethod    
    def setProyectil(self,tipo):
        pass




    
#fabrica deku
class Fabrica_deku(Fabrica_personaje):

    @staticmethod
    def getInstance():
        if Fabrica_deku.instance is None:
            Fabrica_deku.instance=Fabrica_deku()
        elif not isinstance(Fabrica_deku.instance,Fabrica_deku):
            Fabrica_deku.instance=Fabrica_deku()
        return Fabrica_deku.instance
    
    def getPersonaje(self):
        p=Deku.getInstance()
        p.setProyectil(Pro_deku1(0,0))
        p.setEstado(Normal(p))
        return p
    
    def setProyectil(self,tipo):
        if tipo==1:
            Deku.getInstance().setProyectil(Pro_deku1(0,0))
            
        else:
            
            Deku.getInstance().setProyectil(Pro_deku2(0,0))
            



#fabrica goron           
class Fabrica_goron(Fabrica_personaje):

    @staticmethod
    def getInstance():
        if Fabrica_goron.instance is None:
            Fabrica_goron.instance=Fabrica_goron()
        elif not isinstance(Fabrica_goron.instance,Fabrica_goron):
            Fabrica_goron.instance=Fabrica_goron()
        return Fabrica_goron.instance
    
    def getPersonaje(self):
        
        p=Goron.getInstance()
        p.setProyectil(Pro_goron1(0,0))
        p.setEstado(Normal(p))
        return p

    def setProyectil(self,tipo):
        if tipo==1:
            p=Goron.getInstance()
            p.setProyectil(Pro_goron1(0,0))
        else:    
            p=Goron.getInstance()
            p.setProyectil(Pro_goron2(0,0))


#fabrica gerudo
class Fabrica_gerudo(Fabrica_personaje):

    @staticmethod
    def getInstance():
        if Fabrica_gerudo.instance is None:
            Fabrica_gerudo.instance=Fabrica_gerudo()
        elif not isinstance(Fabrica_gerudo.instance,Fabrica_gerudo):
            Fabrica_gerudo.instance=Fabrica_gerudo()
        return Fabrica_gerudo.instance
    
    def getPersonaje(self):
        return Gerudo.getInstance()
    def getPersonaje(self):
       
        p=Gerudo.getInstance()
        p.setProyectil(Pro_gerudo1(0,0))
        p.setEstado(Normal(p))
        return p

    def setProyectil(self,tipo):
        if tipo==1:
            p=Gerudo.getInstance()
            p.setProyectil(Pro_gerudo1(0,0))
        else:    
            p=Gerudo.getInstance()
            p.setProyectil(Pro_gerudo2(0,0))
    



#fabrica zora
class Fabrica_zora(Fabrica_personaje):

    @staticmethod
    def getInstance():
        if Fabrica_zora.instance is None:
            Fabrica_zora.instance=Fabrica_zora()
        elif not isinstance(Fabrica_zora.instance,Fabrica_zora):
            Fabrica_zora.instance=Fabrica_zora()
        return Fabrica_zora.instance
    
    def getPersonaje(self):
        
        p=Zora.getInstance()
        p.setProyectil(Pro_zora1(0,0))
        p.setEstado(Normal(p))
        return p

    def setProyectil(self,tipo):
        if tipo==1:
            p=Zora.getInstance()
            p.setProyectil(Pro_zora1(0,0))
        else:    
            p=Zora.getInstance()
            p.setProyectil(Pro_zora2(0,0))
    





#Seccion para proyectil
class Proyectil_p:
    __metaclass__=ABCMeta
    x=0
    y=0
    dx=0
    tipo=""
    ruta=""
    imagen=None
    def clonar(self):
        return copy.copy(self)
    def get_sprite(self):
        if self.imagen is None:
            self.imagen =image.load(self.ruta)
        return self.imagen    
    def mover(self):
        self.x=self.x+self.dx


#proyectiles deku
class Pro_deku1(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=2
    tipo="acido"
    ruta="Personaje\imagenes\deku\pro1.png"

class Pro_deku2(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=3
    tipo="madera"
    ruta="Personaje\imagenes/deku/pro2.png"

#proyectiles goron
class Pro_goron1(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=2
    tipo="piedra"
    ruta="Personaje\imagenes/goron/pro1.png"

class Pro_goron2(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=2
    tipo="fuego"
    ruta="Personaje\imagenes/goron/pro2.png"

#proyectiles gerudo   
class Pro_gerudo1(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=3
    tipo="metal"
    ruta="Personaje\imagenes/gerudo/pro1.png"

class Pro_gerudo2(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=2
    tipo="electrico"
    ruta="Personaje\imagenes/gerudo/pro2.png"


#proyectiles zora
class Pro_zora1(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=3
    tipo="hielo"
    ruta="Personaje\imagenes/zora/pro1.png"

class Pro_zora2(Proyectil_p):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    dx=2
    tipo="agua"
    ruta="Personaje\imagenes/zora/pro2.png"


    
#Seccion para los estados    
class Estado_personaje:
    __metaclass__=ABCMeta
    personaje=None
    @abc.abstractmethod
    def get_sprite(self):
        pass
class Normal(Estado_personaje):

    def __init__(self,personaje):
        self.personaje=personaje
    def get_sprite(self):
        
        return self.personaje.get_sprite()
class Herido(Estado_personaje):

    def __init__(self,personaje,t):
        self.personaje=personaje
        self.t=t
        self.mili=0
    def get_sprite(self):
        r="Personaje/imagenes/"+self.personaje.nombre+"/golpeado"+self.personaje.direccion[0]+".png"
        self.mili=self.mili+self.t
        if self.mili>=1200:
            self.personaje.setEstado(Invencible(self.personaje,self.t))
        return image.load(r)

   
class Invencible(Estado_personaje):

    def __init__(self,personaje,t):
        self.personaje=personaje
        self.t=t
        self.mili=0
        self.most=False
        
    def get_sprite(self):
        self.mili=self.mili+self.t
        if self.mili>=10000:
            self.personaje.setEstado(Normal(self.personaje))

        if self.most:
            return self.personaje.get_sprite()
            self.most=False
        else:
            self.most=True
            return image.load("Personaje\imagenes\invisible.png")
    
