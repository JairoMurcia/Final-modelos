import pygame
from pygame.locals import *

from Controlador import controlador
from Logica import Logica
from Logica import *


#ventana inicial
class Ventana_inicial:
    pygame.init()
    __ancho=450
    __alto=500
    __clock=pygame.time.Clock()
    __bdp=pygame.image.load("img/boton_derecha.png")
    __bip=pygame.image.load("img/boton_izquierda.png")
    __bdb=pygame.image.load("img/boton_derecha.png")
    __bib=pygame.image.load("img/boton_izquierda.png")
    __bi=pygame.image.load("img/boton_iniciar.png")
    __bi=pygame.transform.scale(__bi,(200,50))
    __pantalla=pygame.display.set_mode((__ancho,__alto))
    __bdp=pygame.transform.scale(__bdb,(100,100))
    __bip=pygame.transform.scale(__bib,(100,100))
    __bdb=pygame.transform.scale(__bdb,(100,100))
    __bib=pygame.transform.scale(__bib,(100,100))
    __cv=controlador.Controlador_vp()
    __imagen_perso=__cv.getPersonaje()
    __imagen_perso=pygame.transform.scale(__imagen_perso,(100,100))
    __imagen_pro=__cv.getProyectil()
    __imagen_pro=pygame.transform.scale(__imagen_pro,(100,100))
    __imagen_esc=__cv.getEscudo()
    __imagen_esc=pygame.transform.scale(__imagen_esc,(100,100))
    _mn=None
    __logica=None
    __imagen_ene=None
    enInicio=True
    vivo=False
    __tam=0
    __logicaEnemigo=None
    
    def main(self):
        print(pygame.__version__)
        while self.enInicio:
    
    
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:

                    
                    exit()
                if eventos.type == pygame.MOUSEBUTTONUP:
                    if eventos.button==1 or eventos.button==2:
                        x=eventos.pos[0]
                        y=eventos.pos[1]
                        self.evento_mouse(x,y)
                        
            
            self.__pantalla.fill((255,255,255))        
            self.__pantalla.blit(self.__bip,[55,10])
            self.__pantalla.blit(self.__imagen_perso,[165,10])
            
            self.__pantalla.blit(self.__bdp,[265,10])

            self.__pantalla.blit(self.__bib,[10,120])
            self.__pantalla.blit(self.__imagen_pro,[120,120])
            self.__pantalla.blit(self.__imagen_esc,[230,120])
            self.__pantalla.blit(self.__bdb,[340,120])
           
            self.__pantalla.blit(self.__bi,[120,270])
            pygame.display.flip()
            self.__clock.tick(5)

            while self.vivo:
                fuente = pygame.font.Font(None, 30)
                texto1 = fuente.render(str(self.__logica.personaje.vida), 0, (255, 255, 255))
                pro_ene=[]
                pro_per=[]
                for eventos in pygame.event.get():
                    if eventos.type == pygame.QUIT:
                        exit()
                    if eventos.type == pygame.KEYUP:
                        if eventos.key==pygame.K_RIGHT or eventos.key==pygame.K_LEFT:
                            self.__logica.detener()
                pulsada = pygame.key.get_pressed()
                
                if pulsada[pygame.K_RIGHT]:
                    self.__logica.cambiarDireccion("derecha")
                    self.__logica.mover(self.__ancho)
                    
                if pulsada[pygame.K_LEFT]:
                    self.__logica.cambiarDireccion("izquierda")
                    self.__logica.mover(self.__ancho)    
                if pulsada[pygame.K_UP]:
                    self.__logica.saltar()
                      

                        
                self.__pantalla.fill((255,255,255))
                self.__imagen_ene=self.__logicaEnemigo.GetEnemigos()
                fondo=self.__mn.fondo
                pro_ene=self.__logicaEnemigo.pro
                for i in self.__imagen_ene:
                    i[0]=pygame.transform.scale(i[0],(50,50))
                    self.__pantalla.blit(i[0],[i[1],i[2]])
                for i in pro_ene:
                    im=pygame.transform.scale(i.getSprite(),(20,20))
                    self.__pantalla.blit(im,[i.x,i.y])  
                self.__imagen_perso=self.__logica.getPersonaje()
                self.__imagen_perso=pygame.transform.scale(self.__imagen_perso,(50,50))
                self.__pantalla.blit(self.__mn.fondo,[self.__mn.xAct,0])
                self.__pantalla.blit(self.__imagen_perso,[self.__logica.personaje.x,self.__logica.personaje.y])
                self.__pantalla.blit(texto1,(0,0))
                self.vivo=self.__logica.actualizar(pro_ene,self.__imagen_ene)
                pygame.display.flip()
                self.__clock.tick(5)
                



            
    def evento_mouse(self,x,y):
        if (x>=55 and x <=155) and (y>=10 and y <=110):
            self.__cv.correr_indice(-1)
            self.__releer()
        if (x>=265 and x <=365) and (y>=10 and y <=110):
            self.__cv.correr_indice(1)
            self.__releer()
        
        if (x>=340 and x<=440) and (y>=120 and y<=220) or (x>=10 and x<=110) and (y>=120 and y<=220):
            self.__cv.correr_pro()
            self.__leerPro()
        if (x>=120 and x<=320) and (y>=270 and y<=320):
            
            p=self.__cv.p.personaje
            f=self.__cv.fabrica
            p.x=100
            p.y=100
            self.__mn=Logica.Manejador_niveles()
            self.__logica=Logica.LogicaPersonaje(p,f,self.__mn)
            self.__logica.personaje.vida=100
            self.EnInicio=False
            self.vivo=True
            self.__tam=self.__mn.tam
            self.__logicaEnemigo=Logica.LogicaEnemigos(p,self.__mn.co,self.__mn.nivel)
            self.__logica.logEne=self.__logicaEnemigo
    def __releer(self):
        self.__imagen_perso=self.__cv.getPersonaje()
        self.__imagen_perso=pygame.transform.scale(self.__imagen_perso,(100,100))
        self.__imagen_pro=self.__cv.getProyectil()
        self.__imagen_pro=pygame.transform.scale(self.__imagen_pro,(100,100))
        self.__imagen_esc=self.__cv.getEscudo()
        self.__imagen_esc=pygame.transform.scale(self.__imagen_esc,(100,100))
    def __leerPro(self):
        
        self.__imagen_pro=self.__cv.getProyectil()
        self.__imagen_pro=pygame.transform.scale(self.__imagen_pro,(100,100))



        
  

v=Ventana_inicial()
v.main()


