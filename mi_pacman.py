# coding: utf-8
import pilasengine
pilas = pilasengine.iniciar()

def iniciar_juego():
    pilas.escenas.PantallaJuego()

def salir_del_juego():
    pilas.terminar()
#Creando el autor Pacman
class Pacman(pilasengine.actores.Actor):
    def iniciar(self):
     
        self.imagen= self.pilas.imagenes.cargar_grilla("pacman.png",4,4)
        self.escala=3
        self.x= 0
        self.y= -150
       #Pantalla de Inicio
class PantallaBienvenida(pilasengine.escenas.Escena):
    def iniciar(self):
        
        pilas.fondos.Volley()
        texto = pilas.actores.Texto("Bienvenido a mi juego")
        texto.x = 0
        texto.y = 80
        
        pilas.actores.Menu(
        [
            ('iniciar juego', iniciar_juego),
            ('salir', salir_del_juego),
        ])
        
        textoBy = pilas.actores.Texto("Creado por: Daniela Gallo C.")
        textoBy.x = 0
        textoBy.y = -150
        textoBy.color = pilas.colores.Color(255, 0, 0, 128)  
        textoBy.escala = 0.5
        
class PantallaJuego(pilasengine.escenas.Escena):
    def iniciar(self):
         juego=Juego()
         juego.iniciar()

class Juego():
    puntaje = pilas.actores.Puntaje(-280, 200, color=pilas.colores.violeta)    
    def iniciar(self):
        pilas.fondos.Volley()
        self.puntaje = pilas.actores.Puntaje(-280, 200, color=pilas.colores.violeta)
        pacman = Pacman(pilas)
        #Mensaje que dice mi Pacman
        pacman.decir("Estoy listo para comer")
        pacman.actualizar
        pacman.aprender("MoverseConElTeclado") 
        #Actor Monedas
        moneda= pilas.actores.Moneda() *11
        pilas.colisiones.agregar(pacman, moneda, self.cuando_colisiona)
        #Actor Aceitunas
        self.aceitunas=pilas.actores.Aceituna()*10
        pilas.colisiones.agregar(pacman,self.aceitunas,self.cuando_colisiona1)
        self.aceitunas_x=pilas.tareas.siempre(5, self.agregar_aceituna,self.aceitunas)
        self.aceitunas_y=pilas.tareas.siempre(10,self.agregar_aceituna_orbitales,self.aceitunas)
        
    def agregar_aceituna(self, aceitunas):
        aceituna=pilas.actores.Aceituna()
        aceituna.x=[-200,pilas.azar(0,200)]
        aceituna.y=pilas.azar(-200,200)
        aceitunas.agregar(aceituna)
        
    def agregar_aceituna_orbitales(self,aceitunas):
         aceituna=pilas.actores.Aceituna()
         aceituna.hacer(pilas.comportamientos.Orbitar,pilas.azar(-200,200),pilas.azar(-300,300),pilas.azar(10,20),pilas.azar(20,30))  
         aceitunas.agregar(aceituna)
    #Funciones cuando el Pacman come monedas
    def cuando_colisiona(self, pacman, moneda):
        moneda.eliminar()
        self.puntaje.aumentar (10)
        pilas.tareas.agregar(1,pacman.imagen.definir_cuadro,0)
        
        pacman.imagen.definir_cuadro(2)
        #Puntaje >90 se gana el juego
        if(int(self.puntaje.texto)>90):
            texto = pilas.actores.Texto ("Felicitaciones, has ganado")
            pilas.tareas.agregar(5,pilas.escenas.PantallaBienvenida)
        #Funciones cuando el Pacma se come aceitunas
    def cuando_colisiona1(self, pacman, aceituna):
        aceituna.eliminar()
        self.puntaje.reducir(10)
        if(int(self.puntaje.texto)<0):
            pilas.tareas.agregar(5,pilas.escenas.PantallaBienvenida)
            pacman.eliminar()
            texto = pilas.actores.Texto ("GAME OVER")
            pilas.fondos.Noche()  
            pilas.camara.vibrar(intensidad=7, tiempo=3)                                                                                

pilas.escenas.vincular(PantallaBienvenida)
pilas.escenas.PantallaBienvenida()
pilas.escenas.vincular(PantallaJuego)
pilas.definir_pantalla_completa(True)

pilas.ejecutar()