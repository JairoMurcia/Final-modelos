import abc
from pygame import image
from abc import ABCMeta

class Bloque:
    __metaclass__=ABCMeta
    x=0
    y=0
    nombre=""
    
    
class Bloque_normal(Bloque):

    def __init__(self,n,y):
        self.nombre=n
        self.y=y
        
class Bloque_dañino(Bloque):

    def __init__(self,n,y):
        self.nombre=n
        self.tipo=self.__setTipo()
        self.y=y
    def __setTipo(self):
         if self.nombre=="lava":
             return "fuego"
         elif self.nombre=="pinchos":
             return "madera"

class Columna:

    def __init__(self,x,bloques):
        self.x=x
        self.bloques=bloques
class Constructor_columna:
    __bloques=[]
    __columnas=[]
    def __init__(self):
        pass
    
    def getColumna(self,nombre,x,y):
        for c in self.__columnas:
            if c.x==x:
                return c
        
        c=None
        aux=[]
        agregar=True
        for n in range(len(y)):
            for b in self.__bloques:
                if b.nombre==nombre[n] and y[n]==b.y:
                    aux=aux+[b]
                    agregar=False
                    break
            if agregar:
                 aux=aux+[self.__getBloque(nombre[n],y[n])]
        return Columna(x,aux)
        
    
    def reiniciar(self):
        self.__bloques=[]
        self.__columnas=[]
    def __getBloque(self,n,y):
         bloque_dañino=['lava','pinchos']
         for bd in bloque_dañino:
             if bd==n:
                 return Bloque_dañino(n,y)
         return Bloque_normal(n,y)       
        
        
        
