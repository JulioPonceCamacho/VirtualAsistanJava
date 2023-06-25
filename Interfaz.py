
import PyQt5
from functools import partial                             
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, QAbstractAnimation
from PyQt5.QtWidgets import (QApplication,QDialog, QVBoxLayout, QWidget, QPushButton,QMainWindow,
                             QLabel,QLineEdit,QTextEdit,QComboBox,QGridLayout)
import ctypes

from pyparsing import countedArray
from IngresarLocal import BorrarCodigo,ActualizarCodigo,buscarCodigo,ObtenerCodigo, ConsultaCodigos, formatoHTML, formatoTxt
from Reconocimiento import *
from WebScraping import REPOSITORIO, ObtenerRepositorios,ObtenerRepositoriosD
import config as cf
import threading as th 
VELOCIDAD_SPEECH,RESPUESTA_SPEECH,TEMA,COLOREL,ID_MIC,NOMBRE_MIC,ID_AS=cf.ObtenerConfiguracion()
REPOSITORIOS=ObtenerRepositorios()
REPOSITORIODEF=ObtenerRepositoriosD()
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


QG = PyQt5.QtGui
# ===================== CLASE barraTitulo ==========================

class barraTitulo(QWidget):
    def __init__(self, parent):
        super(barraTitulo, self).__init__()
        
        self.parent = parent

# ==================== Barra microfono= ====================
class barraTituloMIC(QWidget):
    def __init__(self, parent,nombre):
        super(barraTituloMIC, self).__init__()
        self.nombre=nombre        
        self.parent = parent


##############################################################################################
class hoverButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        
        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int
        self.posicionY = 50

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX, self.posicionY-20, 120, 120))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 120, 120))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)
 
##############################################################################################
class hoverButtonMin(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        
        self.setMouseTracking(True)

        self.fuente = self.font()

        self.posicionX = int
        self.posicionY = int

    def enterEvent(self, event):
        self.posicionX = self.pos().x()
        self.posicionY = 10
        
        self.animacionCursor = QPropertyAnimation(self, b"geometry")
        self.animacionCursor.setDuration(100)
        self.animacionCursor.setEndValue(QRect(self.posicionX, self.posicionY-10, 80, 80))
        self.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        self.fuente.setPointSize(11)
        self.setFont(self.fuente)

    def leaveEvent(self, event):
        self.fuente.setPointSize(10)
        self.setFont(self.fuente)
        
        self.animacionNoCursor = QPropertyAnimation(self, b"geometry")
        self.animacionNoCursor.setDuration(100)
        self.animacionNoCursor.setEndValue(QRect(self.posicionX, self.posicionY, 80, 80))
        self.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)
       
################################################################################################
class VentanaMIC(QMainWindow):
    MIC=None
    Entrada=None
    Mensaje=None
    mensaje=None
    signal = pyqtSignal(int)
    signalWeb = pyqtSignal(int)
    signalWebDef = pyqtSignal(int)
    def __init__(self,parent):
        self.parent=parent
        super(VentanaMIC, self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 180)
        self.pressing = False
        self.move(ancho-560,alto-440)

        self.WIDTH = 550
        self.HEIGHT = 180
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
            "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Entrada por Voz",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)

        self.MIC = QPushButton(self)
    
        self.initUI()
        

    def initUI(self):

        self.signal.connect(self.Buscar)
        self.signalWeb.connect(self.Web)
        self.signalWebDef.connect(self.WebDef)
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)
        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(15)
        self.Mensaje = QLabel("¿Como puedo ayudarte?",self)
        self.Mensaje.setAlignment(Qt.AlignCenter)
        self.Mensaje.setFont(fuenteTitulo)
        self.Mensaje.setGeometry(150,50,350,30)
        self.Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")
       
        self.MIC.setStyleSheet(estilo)
        self.MIC.setGeometry(20, 50, 120, 120)
        self.MIC.setToolTip("Microfono")
        self.MIC.setIcon(QG.QIcon('Media/MICROFONO.png'))
        self.MIC.setIconSize(QSize(100, 100))

        self.Entrada = QTextEdit("Por favor, Habla tu solicitud.",self)
        self.Entrada.setAlignment(Qt.AlignCenter)
        self.Entrada.setFont(fuenteTitulo)
        self.Entrada.setGeometry(150,90,350,75)
        self.Entrada.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:10px; text-align:center;")
        self.MIC.clicked.connect(self.hablar)
    comprobar=False   
    def hablar(self):
        import threading as th
        if self.comprobar==False:
            self.hilo = th.Thread(target=self.animacion)
            self.hilo.start()
            self.hilo2 = th.Thread(target=self.Mic, args=(self.hilo,))
            self.hilo2.start()
            self.comprobar=True
        else:
            print("Ya esta en proceso")
    def animacion(self):
        import threading
        t = threading.currentThread()
        self.MIC.setIcon(QG.QIcon('Media/MICROFONO_U.png'))
        while getattr(t, "do_run", True):
            posicionX=self.MIC.pos().x()
            posicionY=50
            self.MIC.animacion = QPropertyAnimation(self.MIC, b"geometry")
            self.MIC.animacion.setDuration(1000)
            self.MIC.animacion.setStartValue(QRect(posicionX,posicionY-10,120,120))
            self.MIC.animacion.setEndValue(QRect(posicionX,posicionY,120,120))
            self.MIC.animacion.start()
    def Mic(self,hilo):
        i=0
        self.mensaje=reconocer()
        self.comprobar=False
        self.signal.emit(1)
        hilo.do_run = False
        self.MIC.setIcon(QG.QIcon('Media/MICROFONO.png')) 
    def Buscar(self):
        i=0
        texto=self.mensaje
        if texto == "Lo siento, no tienes conexión a internet. Intenta mas tarde":
            self.Mensaje.setText(texto) 
            self.Mensaje.setAlignment(Qt.AlignCenter)   
        else :
            self.Entrada.setText(texto)
            self.Entrada.setAlignment(Qt.AlignCenter)   
            solicitud = texto
            exito,tipo,Val=identificar(solicitud)
            if exito == True:
                if tipo == 'WEB':
                    self.Mensaje.setText("Entendido, Espera un momento porfavor.")
                    Con=Val
                    Val=Val.replace(" ","+")
                    responder("Entendido, Espera un momento porfavor.")
                    self.hilo2 = th.Thread(target=self.buscaWeb, args=(Con,Val))
                    self.hilo2.start()
                if tipo == 'WEB_DEF':
                    import WebScraping as web
                    self.Mensaje.setText("Entendido, Espera un momento porfavor.")
                    Con=Val
                    Val=Val.replace(" ","+")
                    responder("Entendido, Espera un momento porfavor.")
                    self.hilo2 = th.Thread(target=self.buscaWebDef, args=(Con,Val))
                    self.hilo2.start()
                if tipo=='LOCAL':
                    aprox=ObtenerCodigo(Val)
                    if(len(aprox)>0):
                        self.Mensaje.setText("Encontre los siguientes resultados")
                        VR = VentanaResultado(aprox)
                        VR.Resultados=aprox
                        VR.show()
                    else:
                        self.Mensaje.setText('No se encontraron resultados.')
                        responder('No se encontraron resultados, prueba replanteando la petición')
                if tipo=='SALUDO':
                    self.Mensaje.setText(Val)
                    responder(Val)
                if tipo=='AYUDA':
                    self.Mensaje.setText(Val)
                    responder(Val)
            else:
                if tipo=='NONE':
                    self.Mensaje.setText(Val)
                    responder('Disculpa, no te escuche.')
        self.MIC.setIcon(QG.QIcon('Media/MICROFONO.png'))
        self.comprobar=False
    codeArray=None
    googleArray=None
    i=0
    Con=None
    def buscaWeb(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False
        while Com!=True:
            aux=[]
            busqueda=Val+":"+REPOSITORIOS[self.i]
            self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
            self.codeArray = web.getWebResults(self.googleArray, 'code',0)
            b="/*  Palabras reservadas comunmente Utilizadas  */\n"
            patron=re.compile(r'[\W_]') 
            for val in self.codeArray:
                if '\n' in val or ' ' in val:
                    aux.append(val) 
                else:
                    b=b+val+"\n"
            if b!="/*  Palabras reservadas comunmente Utilizadas  */\n":
                aux.append(b)
            self.i+=1
            if len(aux)>1 or self.i>=len(REPOSITORIOS):
                Com=True
        self.codeArray=aux
        if (len(self.codeArray)>0):
            self.signalWeb.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def buscaWebDef(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False
        while Com!=True:
            aux=[]
            busqueda=Val+":"+REPOSITORIODEF[self.i]
            self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
            self.codeArray = web.getWebResults(self.googleArray, 'p',0)
            self.i+=1
            if (len(self.codeArray)>1):
                aux=[]
                aux.append(self.codeArray[0])
                aux.append(self.codeArray[len(self.codeArray)-1])
                self.codeArray=aux
            if len(self.codeArray)>1 or self.i>=len(REPOSITORIODEF):
                Com=True
        if (len(self.codeArray)>0):
            self.signalWebDef.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def Web(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIOS[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.tipo="WEB"
        VRW.pos=self.i-1

        VRW.show()
    def WebDef(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIODEF[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.pos=self.i-1
        VRW.tipo="DEF"
        VRW.show()
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.parent.CMIC=False
        self.close()
    
    

##########################################################################################################
class VentanaAG(QWidget):
    Identificador=None
    Bloque=None
    Estado=None
    def __init__(self, parent):
        self.parent=parent
        super(VentanaAG, self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 300)
        self.pressing = False
        self.move(ancho-560,alto-560)
        self.WIDTH = 550
        self.HEIGHT = 300
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Agregar Código",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)

        self.Identificador= QLineEdit(self)
        self.Bloque= QTextEdit(self)
        self.Bloque.setTabStopWidth(20)
        self.Bloque.textChanged.connect(self.format)
        self.Estado = QLabel("",self)

        self.initUI()
    def initUI(self):
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)

        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(11)
        Mensaje = QLabel("Identificador",self)
        Mensaje.setFont(fuenteTitulo)
        Mensaje.setGeometry(20,40,350,30)
        Mensaje.setStyleSheet("color:"+COLOREL[2]+";")

        fuente = self.font()
        fuente.setPointSize(8)
        self.Estado.setFont(fuente)
        self.Estado.setGeometry(5,283,540,17)
        self.Estado.setStyleSheet(
            """
            color:white; background: rgba(0,122,204,255);
            border-bottom-left-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(17))
        self.Estado.setAlignment(Qt.AlignCenter)

        
        self.Identificador.setGeometry(20,70,380,30)
        self.Identificador.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white; text-align:center;")
        #self.Identificador.returnPressed.connect(self.Bloque.setFocus)
        AG = QPushButton(self)
        AG.setStyleSheet(estilo)
        AG.setGeometry(420, 70, 120, 120)
        AG.setToolTip("Agregar")
        
        AG.setIcon(QG.QIcon('Media/AGREGAR.png'))
        AG.setIconSize(QSize(100, 100))
        Texto = QLabel("Agregar",self)
        Texto.setFont(fuenteTitulo)
        Texto.setGeometry(420,190,120,30)
        Texto.setStyleSheet("color:"+COLOREL[2]+";")
        Texto.setAlignment(Qt.AlignCenter)


        Entrada = QLabel("Bloque de Codigo",self)
        Entrada.setFont(fuenteTitulo)
        Entrada.setGeometry(20,100,350,30)
        Entrada.setStyleSheet("color:"+COLOREL[2]+";")

        Consultar = QPushButton("Ver Todo",self)
        Consultar.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        Consultar.setGeometry(420,200,120,30)
        
        self.Bloque.setGeometry(20,130,380,150)
        self.Bloque.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;font-size:12px; ")

        AG.clicked.connect(self.ingresar)
        Consultar.clicked.connect(self.verTodo)

    def format(self):
        cursor = self.Bloque.textCursor()
        self.Bloque.blockSignals(True)
        an=self.Bloque.toPlainText()
        an=an.replace("\t","   ")
        an = formatoHTML(an)
        self.Bloque.setHtml(an)
        self.Bloque.setTextCursor(cursor)
        self.Bloque.blockSignals(False)

    def ingresar(self):
        bloq = self.Bloque.toPlainText()
        ID = self.Identificador.text()
        print("["+bloq+"]")
        if (str(ID) == '' or str(bloq) == '') or (str(ID) == ' ' or str(bloq) == ' '):
            self.Estado.setText("Llena los campos porfavor")
            self.Estado.setStyleSheet(
            """
            color:white; background: rgba(225,58,45,255);
            border-bottom-left-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(17))
            responder("Necesita llenar todos los campos.")
        else:
            import IngresarLocal as IL
            val=IL.Agregar(ID, bloq)
            if val == False:
                self.Estado.setText("El identificador ya existe")
                self.Estado.setStyleSheet(
                """
                color:white; background: rgba(225,58,45,255);
                border-bottom-left-radius:{0}px;
                border-bottom-right-radius:{0}px;
                """.format(17))
                responder("El identificador ya existe, porfavor cambialo.")
            else:
                self.Estado.setText("Agregado Correctamente")
                self.Estado.setStyleSheet(
                    """
                    color:white; background: rgba(0,122,204,255);
                    border-bottom-left-radius:{0}px;
                    border-bottom-right-radius:{0}px;
                    """.format(17))
                responder("Se ha agregado Correctamente")
    def verTodo(self):
        self.close()
        VT = VentanaTodo()
        VT.show()
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.parent.CAG=False
        self.close()
#####################################################################################################
class VentanaTEC(QWidget):
    Entrada = None
    signalWeb = pyqtSignal(int)
    signalWebDef = pyqtSignal(int)
    def __init__(self, parent):
        self.parent=parent
        super(VentanaTEC, self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 180)
        self.pressing = False
        self.move(ancho-560,alto-440)

        self.WIDTH = 550
        self.HEIGHT = 180
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Petición por Teclado",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)

        self.initUI()

    def initUI(self):
        self.signalWeb.connect(self.Web)
        self.signalWebDef.connect(self.WebDef)
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)

        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(11)
        self.Mensaje = QLineEdit("¿Como puedo ayudarte?",self)
        self.Mensaje.setEnabled(False)
        self.Mensaje.setAlignment(Qt.AlignCenter)
        self.Mensaje.setFont(fuenteTitulo)
        self.Mensaje.setGeometry(20,60,350,30)
        self.Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")
        MIC = QPushButton(self)
        MIC.setStyleSheet(estilo)
        MIC.setGeometry(400, 35, 120, 120)
        MIC.setToolTip("Enviar")
        MIC.setIcon(QG.QIcon('Media/TECLADO.png'))
        MIC.setIconSize(QSize(100, 100))


        Texto = QLabel("Enviar",self)
        Texto.setFont(fuenteTitulo)
        Texto.setGeometry(400,150,120,20)
        Texto.setStyleSheet("color:"+COLOREL[2]+";")
        Texto.setAlignment(Qt.AlignCenter)



        self.Entrada = QLineEdit(self)
        self.Entrada.setGeometry(20,100,350,50)
        self.Entrada.returnPressed.connect(self.ingresar)
        self.Entrada.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        
        MIC.clicked.connect(self.ingresar)
    
    def ingresar(self):
        solicitud = self.Entrada.text()
        exito,tipo,Val=identificar(solicitud)
        if exito == True:
            if tipo == 'WEB':
                self.Mensaje.setText("Entendido, Espera un momento porfavor.")
                Con=Val
                Val=Val.replace(" ","+")
                responder("Entendido, Espera un momento porfavor.")
                self.hilo2 = th.Thread(target=self.buscaWeb, args=(Con,Val))
                self.hilo2.start()
            if tipo == 'WEB_DEF':
                self.Mensaje.setText("Entendido, Espera un momento porfavor.")
                Con=Val
                Val=Val.replace(" ","+")
                responder("Entendido, Espera un momento porfavor.")
                self.hilo2 = th.Thread(target=self.buscaWebDef, args=(Con,Val))
                self.hilo2.start()
            if tipo=='LOCAL':
                aprox=ObtenerCodigo(Val)
                if(len(aprox)>0):
                    self.Mensaje.setText("Encontre los siguientes resultados")
                    VR = VentanaResultado(aprox)
                    VR.Resultados=aprox
                    VR.show()
                else:
                    self.Mensaje.setText('No se encontraron resultados.')
                    responder('No se encontraron resultados, prueba replanteando la petición')
            if tipo=='SALUDO':
                self.Mensaje.setText(Val)
                responder(Val)
            if tipo=='AYUDA':
                self.Mensaje.setText(Val)
                responder(Val)
        else:
            if tipo=='NONE':
                self.Mensaje.setText(Val)
                responder(Val+" Si requieres ayuda para saber como funciono solo dime: Necesito Ayuda")
    codeArray=None
    googleArray=None
    i=0
    Con=None
    def buscaWeb(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False
        while Com!=True:
            aux=[]
            busqueda=Val+":"+REPOSITORIOS[self.i]
            self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
            self.codeArray = web.getWebResults(self.googleArray, 'code',0)
            b="/*  Palabras reservadas comunmente Utilizadas  */\n"
            patron=re.compile(r'[\W_]') 
            for val in self.codeArray:
                if '\n' in val or ' ' in val:
                    aux.append(val) 
                else:
                    b=b+val+"\n"
            if b!="/*  Palabras reservadas comunmente Utilizadas  */\n":
                aux.append(b)
            self.i+=1
            if len(aux)>1 or self.i>=len(REPOSITORIOS):
                Com=True
        self.codeArray=aux
        if (len(self.codeArray)>0):
            self.signalWeb.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def buscaWebDef(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False
        while Com!=True:
            aux=[]
            busqueda=Val+":"+REPOSITORIODEF[self.i]
            self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
            self.codeArray = web.getWebResults(self.googleArray, 'p',0)
            self.i+=1
            if len(self.codeArray)>1 or self.i>=len(REPOSITORIODEF):
                Com=True
            if (len(self.codeArray)>1):
                aux=[]
                aux.append(self.codeArray[0])
                aux.append(self.codeArray[len(self.codeArray)-1])
                self.codeArray=aux
        if (len(self.codeArray)>0):
            self.signalWebDef.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def Web(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIOS[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.pos=self.i-1
        VRW.tipo="WEB"
        VRW.show()
    def WebDef(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIODEF[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.pos=self.i-1
        VRW.tipo="DEF"
        VRW.show()
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.parent.CTEC=False
        self.close()
######################################################################################################
class VentanaAJUS(QWidget):
    def __init__(self, parent):
        self.parent=parent
        super(VentanaAJUS, self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 480)
        self.pressing = False
        self.move(ancho-560,alto-740)

        self.WIDTH = 550
        self.HEIGHT = 480
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Configuración",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        

        # Aplicar Barra de Título personalizada
        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)

        self.initUI()


    def initUI(self):
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)

        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(11)
        Mensaje = QLabel("Velocidad de Habla",self)
        Mensaje.setAlignment(Qt.AlignCenter)
        Mensaje.setFont(fuenteTitulo)
        Mensaje.setGeometry(20,60,300,30)
        Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.EntradaV = QLineEdit(str(VELOCIDAD_SPEECH),self)
        #self.EntradaV.returnPressed.connect(self.Aplicar)
        self.EntradaV.setGeometry(330,60,190,20)
        self.EntradaV.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        self.EntradaV.setValidator(PyQt5.QtGui.QDoubleValidator())
    
        MensajeRA = QLabel("Respuesta del asistente por voz",self)
        MensajeRA.setAlignment(Qt.AlignCenter)
        MensajeRA.setFont(fuenteTitulo)
        MensajeRA.setGeometry(20,120,300,30)
        MensajeRA.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.RESA = QComboBox(self)
        if RESPUESTA_SPEECH == "Si":
            self.RESA.addItem("Si")
            self.RESA.addItem("No")
        else:
            self.RESA.addItem("No")
            self.RESA.addItem("Si")
        self.RESA.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        self.RESA.setGeometry(330,120,190,20)

        MensajeT = QLabel("Tema de Interfaz",self)
        MensajeT.setAlignment(Qt.AlignCenter)
        MensajeT.setFont(fuenteTitulo)
        MensajeT.setGeometry(20,180,300,30)
        MensajeT.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.TEMAQ = QComboBox(self)
        if TEMA == "Claro":
            self.TEMAQ.addItem("Claro")
            self.TEMAQ.addItem("Obscuro")
        else:
            self.TEMAQ.addItem("Obscuro")
            self.TEMAQ.addItem("Claro")
        self.TEMAQ.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        self.TEMAQ.setGeometry(330,180,190,20)


        MAS = QLabel("Asistente de la aplicación:",self)
        MAS.setAlignment(Qt.AlignCenter)
        MAS.setFont(fuenteTitulo)
        MAS.setGeometry(20,240,300,30)
        MAS.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.id_mic = QComboBox(self)
        self.id_mic.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        self.id_mic.setGeometry(330,240,190,20)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        aux=[]
        id=[]
        for voice in voices:
            if ID_AS == voice.id:
                self.id_mic.addItem(voice.name,voice.id)
            else:
                aux.append(voice.name)
                id.append(voice.id)
        i=0
        for val in aux:
            self.id_mic.addItem(val,id[i])        
            i+=1

        MDIS = QLabel("Dispositivo de entrada de audio",self)
        MDIS.setAlignment(Qt.AlignCenter)
        MDIS.setFont(fuenteTitulo)
        MDIS.setGeometry(20,300,300,30)
        MDIS.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.DIS = QComboBox(self)
        self.DIS.setStyleSheet("background-color:"+COLOREL[1]+"; border-radius:10px;color:white;")
        self.DIS.setGeometry(330,300,190,20)

        mic_list = sr.Microphone.list_microphone_names()
        self.DIS.addItem(NOMBRE_MIC,ID_MIC)
        for i, microphone_name in enumerate(mic_list):                     
            try: 
                with sr.Microphone(device_index = i, sample_rate = sample_rate, chunk_size = chunk_size) as source:      
                        if microphone_name != NOMBRE_MIC:
                            self.DIS.addItem(microphone_name,i)
            except:
                pass
        AJUS = QPushButton("Aplicar", self)
        AJUS.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        AJUS.setGeometry(400, 430,100, 30)
        AJUS.clicked.connect(self.Aplicar)        

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.parent.CRES=False
        self.close()
    def Aplicar(self):
        cf.CambiarConfiguracion(int(self.EntradaV.text()),self.RESA.currentText(),self.TEMAQ.currentText(),self.DIS.currentData(),self.DIS.currentText(),self.id_mic.currentData())
        VELOCIDAD_SPEECH,RESPUESTA_SPEECH,TEMA,COLOREL,ID_MIC,NOMBRE_MIC,ID_AS=cf.ObtenerConfiguracion()
        import os
        import sys
        os.execl(sys.executable, "main.py", *sys.argv) 
#########################################################################################################
class VentanaResultado(QWidget):
    Resultados = None
    indice=0
    def __init__(self, res,parent=None):
        super(VentanaResultado,self).__init__(parent)
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 600)
        self.pressing = False
        self.Resultados=res

        self.WIDTH = 550
        self.HEIGHT = 600
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Resultado de Consulta",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        # Aplicar Barra de Título personalizada
        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)
        self.texto = QLabel("Resultado",self)
        self.Entrada = QTextEdit(self)
        self.Entrada.textChanged.connect(self.format)
        self.Entrada.setTabStopWidth(20)
        self.initUI()
    def format(self):
        self.Entrada.blockSignals(True)
        cursor = self.Entrada.textCursor()
        an=self.Entrada.toPlainText()
        an=an.replace("\t","   ")
        an = formatoHTML(an)
        self.Entrada.setHtml(an)
        self.Entrada.setTextCursor(cursor)
        self.Entrada.blockSignals(False)
    def initUI(self):
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)
        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(12)
        Mensaje = QLabel("Valor Búscado",self)
        Mensaje.setAlignment(Qt.AlignCenter)
        Mensaje.setFont(fuenteTitulo)
        Mensaje.setGeometry(50,60,450,30)
        Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")
        
        self.texto.setFont(fuenteTitulo)
        self.texto.setGeometry(50,105,600,30)
        self.texto.setStyleSheet("color:"+COLOREL[2]+"")
        val=self.Resultados[0]
        nombre,bloque=buscarCodigo(int(val[0]),val[1],int(val[2]))
        self.texto.setText(nombre)

        SIG = QPushButton(">", self)
        SIG.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:15px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        SIG.setGeometry(480, 105,30, 30)
        SIG.clicked.connect(self.sigRes)

        RES = QPushButton("<", self)
        RES.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:15px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        RES.setGeometry(440, 105,30, 30)
        RES.clicked.connect(self.sigBack)

        responder('Encontre las siguientes coincidencias en tu repositorio local.')


        self.Entrada.setGeometry(50,150,450,400)
        self.Entrada.setStyleSheet("background-color:"+COLOREL[1]+"; color:white; border-radius:10px; font-size:12px;")
        BloqueHTML=formatoHTML(bloque)
        self.Entrada.setHtml(BloqueHTML)
        self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)



        BORRAR = QPushButton("Borrar", self)
        BORRAR.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        BORRAR.setGeometry(440, 550,60, 30)
        BORRAR.clicked.connect(self.Borrar)

        ACT = QPushButton("Actualizar", self)
        ACT.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        ACT.setGeometry(370, 550,60, 30)
        ACT.clicked.connect(self.Actualizar)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.close()
    def sigRes(self):
        if self.indice<len(self.Resultados)-1:
            self.indice+=1
        val=self.Resultados[self.indice]
        nombre,bloque=buscarCodigo(int(val[0]),val[1],int(val[2]))
        self.texto.setText(nombre)
        BloqueHTML=formatoHTML(bloque)
        self.Entrada.setHtml(BloqueHTML)
        self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)
    def sigBack(self):
        if self.indice>0:
            self.indice-=1
        val=self.Resultados[self.indice]
        nombre,bloque=buscarCodigo(int(val[0]),val[1],int(val[2]))
        self.texto.setText(nombre)
        BloqueHTML=formatoHTML(bloque)
        self.Entrada.setHtml(BloqueHTML)
        self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)

    def Borrar(self):
        val=self.texto.text()
        com=BorrarCodigo(val)
        if com==True:
            responder("Se ha borrado correctamente.")
        else:
            responder("No se pudo borrar el codigo")
        self.close()
    def Actualizar(self):
        id=self.texto.text()
        bloque=self.Entrada.toPlainText()
        bloque=formatoTxt(bloque)
        com=ActualizarCodigo(id,bloque)
        if com==True:
            responder("Se actualizó correctamente")
        else:
            responder("Existio un error al actualizar el archivo")        
##########################################################################################################
class VentanaResultadoWeb(QWidget):
    Resultados = None
    Web =None
    REPOSITORIOS=None
    Consulta ="Resultado de busqueda: "
    pos=0
    tipo=None
    busqueda=None
    indice=0
    signalWeb = pyqtSignal(int)
    signalWebDef = pyqtSignal(int)

    def __init__(self, parent,res):
        self.parent=parent
        super(VentanaResultadoWeb,self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 600)
        self.pressing = False
        self.Resultados=res

        self.WIDTH = 550
        self.HEIGHT = 600
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Resultado de Consulta",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        # Aplicar Barra de Título personalizada
        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"Ajustes"))
        self.setLayout(tituloBarra)
        self.texto = QLabel("Resultado",self)
        self.Entrada = QTextEdit(self)
        self.Entrada.textChanged.connect(self.format)
        self.Entrada.setTabStopWidth(20)
        self.initUI()
    def format(self):
        self.Entrada.blockSignals(True)
        cursor = self.Entrada.textCursor()
        an=self.Entrada.toPlainText()
        an=an.replace("\t","   ")
        an = formatoHTML(an)
        self.Entrada.setHtml(an)
        self.Entrada.setTextCursor(cursor)
        self.Entrada.blockSignals(False)
    def initUI(self):
        self.signalWeb.connect(self.Web)
        self.signalWebDef.connect(self.WebDef)
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)
        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(12)
        Mensaje = QLabel(self.Consulta,self)
        Mensaje.setAlignment(Qt.AlignCenter)
        Mensaje.setFont(fuenteTitulo)
        Mensaje.setGeometry(50,60,450,30)
        Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")
        
        self.texto.setFont(fuenteTitulo)
        self.texto.setGeometry(50,105,600,30)
        self.texto.setStyleSheet("color:"+COLOREL[2]+"")
        self.texto.setText("Resultado de busqueda: "+self.Consulta)

        SIG = QPushButton(">", self)
        SIG.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:15px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        SIG.setGeometry(480, 105,30, 30)
        SIG.clicked.connect(self.sigRes)

        RES = QPushButton("<", self)
        RES.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:15px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
        RES.setGeometry(440, 105,30, 30)
        RES.clicked.connect(self.sigBack)


        self.Entrada.setGeometry(50,150,450,400)
        self.Entrada.setStyleSheet("background-color:"+COLOREL[1]+"; color:white; border-radius:10px; font-size:12px;")
        try:
            BloqueHTML=formatoHTML(self.Resultados[self.indice])
            self.Entrada.setHtml(BloqueHTML)
            self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)
            Siguiente = QPushButton("Siguiente Página", self)
            Siguiente.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
            Siguiente.setGeometry(320, 560,100, 30)
            Siguiente.clicked.connect(self.Siguiente)

            Agregar = QPushButton("Guardar", self)
            Agregar.setStyleSheet("QPushButton{background-color:#0070c0; font-size:12px; font-weight:100; border-radius:10px;color:white;} QPushButton::hover{background-color: #5270ff;}QPushButton::pressed{background-color: #6835b6;}")
            Agregar.setGeometry(430, 560,100, 30)
            Agregar.clicked.connect(self.Guardar)
            responder('Encontre las siguientes coincidencias en la Web')

            self.rep = QLabel("",self)
            self.rep.setAlignment(Qt.AlignCenter)
            self.rep.setFont(fuenteTitulo)
            self.rep.setGeometry(20, 560,150, 30)
            self.rep.setStyleSheet("border: 0.5px solid black; color:"+COLOREL[2]+"; font-size:9px; border-radius:5px; text-align:center;")
        except:
            self.Entrada.setPlainText("Sin resultados")

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.close()
    def sigRes(self):
        if self.indice<len(self.Resultados)-1:
            self.indice+=1
        val=self.Resultados[self.indice]
        BloqueHTML=formatoHTML(val)
        self.Entrada.setHtml(BloqueHTML)
        self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)

    def sigBack(self):
        if self.indice>0:
            self.indice-=1
        val=self.Resultados[self.indice]
        BloqueHTML=formatoHTML(val)
        self.Entrada.setHtml(BloqueHTML)
        self.Entrada.moveCursor(PyQt5.QtGui.QTextCursor.Start)

    def Siguiente(self):
        if self.tipo == 'WEB':
            Con=self.texto.text()
            Val=Con.replace(" ","+")
            responder("Entendido, Espera un momento porfavor.")
            self.hilo2 = th.Thread(target=self.buscaWeb, args=(Con,Val))
            self.hilo2.start()
        if self.tipo == 'DEF':
            import WebScraping as web
            Con=self.texto.text()
            Val=Con.replace(" ","+")
            responder("Entendido, Espera un momento porfavor.")
            self.hilo2 = th.Thread(target=self.buscaWebDef, args=(Con,Val))
            self.hilo2.start()
    codeArray=None
    googleArray=None
    i=0
    Con=None
    def buscaWeb(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False  
        aux=[]
        busqueda=Val+":"+REPOSITORIOS[self.pos+1]
        self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
        self.codeArray = web.getWebResults(self.googleArray, 'code',0)
        b="/*  Palabras reservadas comunmente Utilizadas  */\n"
        patron=re.compile(r'[\W_]') 
        for val in self.codeArray:
            if '\n' in val or ' ' in val:
                aux.append(val) 
            else:
                b=b+val+"\n"
        if b!="/*  Palabras reservadas comunmente Utilizadas  */\n":
            aux.append(b)
        self.pos+=1
        if len(aux)>1 or self.i>=len(REPOSITORIOS):
            Com=True
        self.codeArray=aux
        if (len(self.codeArray)>0):
            self.signalWeb.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def buscaWebDef(self,Con,Val):
        import WebScraping as web
        self.codeArray=None
        self.googleArray=None
        self.i=0
        self.Con=Con
        Com=False
        aux=[]
        busqueda=Val+":"+REPOSITORIODEF[self.pos+1]
        self.googleArray = web.getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
        self.codeArray = web.getWebResults(self.googleArray, 'p',0)
        self.pos+=1
        if (len(self.codeArray)>1):
            aux=[]
            aux.append(self.codeArray[0])
            aux.append(self.codeArray[len(self.codeArray)-1])
            self.codeArray=aux
        if len(self.codeArray)>1 or self.i>=len(REPOSITORIODEF):
            Com=True
        if (len(self.codeArray)>0):
            self.signalWebDef.emit(1)
        else:
            self.Mensaje.setText('No se encontraron resultados.')
            responder('No se encontraron resultados, prueba replanteando la petición')
    def Web(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIOS[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.tipo="WEB"
        VRW.pos=self.pos-1

        VRW.show()
    def WebDef(self):
        VRW = VentanaResultadoWeb(self.parent,self.codeArray)
        VRW.Resultados=self.codeArray
        VRW.Web=self.googleArray
        VRW.rep.setText("Fuente: "+str(REPOSITORIODEF[self.i-1]).upper())
        VRW.texto.setText(self.Con)
        VRW.pos=self.pos-1
        VRW.tipo="DEF"
        VRW.show()
    def Guardar(self):
        VG = VentanaAG(self.parent)
        VG.Identificador.setText(self.texto.text())
        VG.Bloque.setHtml(formatoHTML(self.Entrada.toPlainText()))
        VG.show()


##########################################################################################################
class VentanaTodo(QWidget):
    def __init__(self, parent=None):
        super(VentanaTodo, self).__init__(parent)
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(550, 600)
        self.pressing = False

        self.WIDTH = 550
        self.HEIGHT = 600
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Asistente Virtual",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")


        self.initUI()

    def initUI(self):
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)


        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        fuenteTitulo = self.font()
        fuenteTitulo.setPointSize(12)
        Mensaje = QLabel("Selecciona el identificador para ver el codigo almacenado.",self)
        Mensaje.setAlignment(Qt.AlignCenter)
        Mensaje.setFont(fuenteTitulo)
        Mensaje.setGeometry(50,60,450,30)
        Mensaje.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")
        
        grid_layout = QGridLayout()
        Entrada = QWidget(self)
        Entrada.setGeometry(20,100,230,470)
        Entrada.setStyleSheet("background-color:"+COLOREL[1]+"; color:white; border-radius:10px;")
        Entrada.setLayout(grid_layout)

        self.IDEN = QLabel("",self)
        self.IDEN.setAlignment(Qt.AlignCenter)
        self.IDEN.setFont(fuenteTitulo)
        self.IDEN.setGeometry(270,100,250,30)
        self.IDEN.setStyleSheet("border: 1px solid black; color:"+COLOREL[2]+"; font-size:12px; border-radius:5px; text-align:center;")

        self.BLOC = QTextEdit(self)
        self.BLOC.textChanged.connect(self.format)
        self.BLOC.setTabStopWidth(20)
        self.BLOC.setGeometry(270,140,250,420)
        self.BLOC.setStyleSheet("background-color:"+COLOREL[1]+"; color:white; border-radius:10px; font-size:12px;")

        Lista = ConsultaCodigos()
        i=0
        for val in Lista:
            nombre=val.split("~")
            button = QPushButton(nombre[1])
            button.setStyleSheet("QPushButton{border: 0; padding: 10px;border-radius:10px; background-color:#0070c0; color:white;} QPushButton::hover{background-color:#444444;}")
            button.clicked.connect(partial(self.mostrar,val))
            grid_layout.addWidget(button,i,0)
            i+=1
    def format(self):
        self.BLOC.blockSignals(True)
        cursor = self.BLOC.textCursor()
        an=self.BLOC.toPlainText()
        an=an.replace("\t","   ")
        an = formatoHTML(an)
        self.BLOC.setHtml(an)
        self.BLOC.setTextCursor(cursor)
        self.BLOC.blockSignals(False)
    def mostrar(self,val):
        codigo = val.split("~")
        nombre,bloque=buscarCodigo(int(codigo[0]),codigo[1],int(codigo[2]))

        self.IDEN.setText(nombre)
        BloqueHTML=formatoHTML(bloque)
        self.BLOC.setHtml(BloqueHTML)
        
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def CERRAR(self):
        self.close()

#====================================================================
class VentanaPrincipalMin(QWidget):
    Entrada = None
    def __init__(self, parent):
        self.parent=parent
        super(VentanaPrincipalMin, self).__init__()
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint  )
        self.setMinimumSize(100, 100)
        self.pressing = False
        self.move(ancho-150,alto-150)

        self.WIDTH = 100
        self.HEIGHT = 100
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 50

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )

        tituloBarra = QVBoxLayout()
        tituloBarra.addWidget(barraTituloMIC(self,"min"))
        self.setLayout(tituloBarra)

        self.initUI()

    def initUI(self):
        self.BOT = QPushButton(self)
        self.BOT.setGeometry(10, 10, 80, 80)
        self.BOT.setStyleSheet("QPushButton{border-radius:40px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}")
        self.BOT.setToolTip("Microfono")
        self.BOT.setIcon(QG.QIcon('Media/MICROFONO.png'))
        self.BOT.setIconSize(QSize(80, 80))

        estilo="QPushButton{border-radius:40px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"

        self.MIC = hoverButtonMin(self)
        self.MIC.setStyleSheet(estilo)
        self.MIC.setGeometry(0,0,0,0)
        self.AGG = hoverButtonMin(self)
        self.AGG.setStyleSheet(estilo)
        self.AGG.setGeometry(0,0,0,0)
        self.TEC = hoverButtonMin(self)
        self.TEC.setStyleSheet(estilo)
        self.TEC.setGeometry(0,0,0,0)
        self.AJUS = hoverButtonMin(self)
        self.AJUS.setStyleSheet(estilo)
        self.AJUS.setGeometry(0,0,0,0)
        self.Extend = hoverButtonMin(self)

        self.Extend.setGeometry(0,0,0,0)
        self.Extend.setStyleSheet(estilo)

        self.BOT.clicked.connect(self.Mostrar)
        self.MIC.clicked.connect(self.MICROFONO)
        self.AGG.clicked.connect(self.AGREGAR)
        self.TEC.clicked.connect(self.TECLADO)
        self.AJUS.clicked.connect(self.AJUSTES)
        self.Extend.clicked.connect(self.Expandir)
    CMIC = False
    VMIC =None
    def MICROFONO(self):
        if self.CMIC == False:
            self.VMIC = VentanaMIC(self)
            mensajeSaludos= SALUDOS[random.randrange(len(SALUDOS))]
            responder(mensajeSaludos)
            self.VMIC.Mensaje.setText(mensajeSaludos)
            self.VMIC.show()
            self.CMIC=True
        else:
            self.CMIC=False
            self.VMIC.close()
    CAG=False
    VAG=None
    def AGREGAR(self):
        if self.CAG==False:
            self.CAG=True
            self.VAG = VentanaAG(self)
            self.VAG.show()
        else:
           self.VAG.close()
           self.CAG=False
    VTEC=None
    CTEC=False
    def TECLADO(self):
        if self.CTEC==False:
            self.CTEC=True
            self.VTEC=VentanaTEC(self)
            mensajeSaludos= SALUDOS[random.randrange(len(SALUDOS))]
            responder(mensajeSaludos)
            self.VTEC.Mensaje.setText(mensajeSaludos)
            self.VTEC.show()
        else:
            self.CTEC=False
            self.VTEC.close()

    VRES=None
    CRES=False
    def AJUSTES(self):
        if self.CRES==False:
            self.VRES=VentanaAJUS(self)
            self.VRES.show()
            self.CRES=True
        else:
            self.CRES=False
            self.VRES.close()
        print("AJUSTANDO")
    def CERRAR(self):
        self.close()
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def AGIL(self):
        ventana = VentanaPrincipalMin(None)
        ventana.show()
        self.close()

    MOSTRADO=False
    def Mostrar(self):
        if(self.MOSTRADO==False):        
            self.resize(500,self.HEIGHT)
            self.move(ancho-550,alto-150)
            self.centralwidget.setGeometry(400,0,100,100)
            self.BOT.setGeometry(410,10,80,80)
            
            #self.MIC.setGeometry(320, 10, 80, 80)
            self.MIC.setToolTip("Microfono")
            self.MIC.setIcon(QG.QIcon('Media/MICROFONO.png'))
            self.MIC.setIconSize(QSize(90, 90))
            self.MIC.setGeometry(410,0,0,0)
            self.anim(self.MIC,320,10,100)

            
            #self.AGG.setGeometry(240, 10, 80, 80)
            self.AGG.setToolTip("Agregar código Local")
            self.AGG.setIcon(QG.QIcon('Media/AGREGAR.png'))
            self.AGG.setIconSize(QSize(75, 75))
            self.AGG.setGeometry(410,0,0,0)
            self.anim(self.AGG,240,10,130)

            
            #self.TEC.setGeometry(160, 10, 80, 80)
            self.TEC.setToolTip("Búsqueda por teclado")
            self.TEC.setIcon(QG.QIcon('Media/TECLADO.png'))
            self.TEC.setIconSize(QSize(75, 75))
            self.TEC.setGeometry(410,0,0,0)
            self.anim(self.TEC,160,10,160)
            
            #self.AJUS.setGeometry(80, 10, 80, 80)
            self.AJUS.setToolTip("Ajustes")
            self.AJUS.setIcon(QG.QIcon('Media/AJUSTES.png'))
            self.AJUS.setIconSize(QSize(75, 75))
            self.AJUS.setGeometry(410,0,0,0)
            self.anim(self.AJUS,80,10,190)

            #self.Extend.setGeometry(0, 10, 80, 80)
            self.Extend.setToolTip("Expandir")
            self.Extend.setIcon(QG.QIcon('Media/EXPAND.png'))
            self.Extend.setIconSize(QSize(75, 75))
            self.Extend.setGeometry(410,0,0,0)
            self.anim(self.Extend,0,10,230)
            self.MOSTRADO=True
        else:
            self.MOSTRADO=False
            self.desAnim(self.MIC,410,10,100)
            self.desAnim(self.AGG,410,10,130)
            self.desAnim(self.TEC,410,10,160)
            self.desAnim(self.AJUS,410,10,190)
            self.desAnim(self.Extend,410,10,230)
            self.move(ancho-150,alto-150)
            self.resize(self.WIDTH, self.HEIGHT)
            self.centralwidget.setGeometry(0,0,100,100)
            self.BOT.setGeometry(10,10,80,80)
            self.MIC.setGeometry(0,0,0,0)
            self.AGG.setGeometry(0,0,0,0)
            self.TEC.setGeometry(0,0,0,0)
            self.AJUS.setGeometry(0,0,0,0)
            self.Extend.setGeometry(0,0,0,0)
                                
    def anim(self,boton,x,y,tiempo):
        boton.fuente = boton.font()
        boton.posicionX = boton.pos().x()
        boton.posicionY = 10
        
        boton.animacionCursor = QPropertyAnimation(boton, b"geometry")
        boton.animacionCursor.setDuration(tiempo)
        boton.animacionCursor.setEndValue(QRect(x, y, 80, 80))
        boton.animacionCursor.start(QAbstractAnimation.DeleteWhenStopped)
        
        boton.fuente.setPointSize(11)
        boton.setFont(boton.fuente)

    def desAnim(self,boton,x,y,tiempo):
        boton.fuente = boton.font()
        boton.fuente.setPointSize(10)
        boton.setFont(boton.fuente)
        
        boton.animacionNoCursor = QPropertyAnimation(boton, b"geometry")
        boton.animacionNoCursor.setDuration(tiempo)
        boton.animacionNoCursor.setEndValue(QRect(x-100, y, 0, 0))
        boton.animacionNoCursor.start(QAbstractAnimation.DeleteWhenStopped)
    def Expandir(self):
        ventana=ventanaPrincipal()
        ventana.show()
        import os
        import sys
        os.execl(sys.executable, "main.py", *sys.argv)   
        
        



# =================== CLASE ventanaPrincipal =======================

class ventanaPrincipal(QWidget):
    def __init__(self, parent=None):
        super(ventanaPrincipal, self).__init__(parent)
        self.setStyleSheet("background-color:"+COLOREL[0]+"; border-radius:60 px")
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowSystemMenuHint | Qt.FramelessWindowHint)
        self.setMinimumSize(550, 180)
        self.pressing = False
        self.move(ancho-560,alto-240)
        
        self.WIDTH = 550
        self.HEIGHT = 180
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        radius = 30

        self.centralwidget.setStyleSheet(
           "border: 1px solid "+COLOREL[1]+";background:"+COLOREL[0]+";""""
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


        titulo=QLabel("Asistente Virtual",self)
        titulo.setGeometry(120,5,300,30)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px; color:white; font-size:14px;")

        self.initUI()

    def initUI(self):
        Grid= QGridLayout(self)
        Grid.setContentsMargins(0,0,0,0)
        Reducir = QPushButton(self)
        Reducir.setToolTip("Modo Agíl")
        Reducir.setIconSize(QSize(10, 10))
        Reducir.setGeometry(10,10,10,10)
        Reducir.setIcon(QG.QIcon('Media/RESI.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        Reducir.setStyleSheet(estiloCab)
        Reducir.clicked.connect(self.AGIL)

        botones=QWidget(self)
        botones.setGeometry(455,5,80,30)
        botones.setStyleSheet("Background:"+COLOREL[1]+"; border-radius:15px; padding:0px; border:0px;")
        botones.setContentsMargins(0,0,0,0)
        botones.setLayout(Grid)
        buttonCerrar = QPushButton(self)
        buttonCerrar.setToolTip("Cerrar")
        buttonCerrar.setIconSize(QSize(25, 25))
        buttonCerrar.setIcon(QG.QIcon('Media/CLOS.png'))
        estiloCab="QPushButton{border-radius:10px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed  {background-color :#425473;} QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
        buttonCerrar.setStyleSheet(estiloCab)
        buttonCerrar.clicked.connect(self.CERRAR)
        buttonMinimizar = QPushButton()
        buttonMinimizar.setToolTip("Minimizar")
        buttonMinimizar.setIconSize(QSize(25, 25))
        buttonMinimizar.setStyleSheet(estiloCab)
        buttonMinimizar.setIcon(QG.QIcon('Media/MIN.png'))
        Grid.addWidget(buttonMinimizar,0,0)
        Grid.addWidget(buttonCerrar,0,1)
        buttonMinimizar.clicked.connect(self.Minimizar)



        estilo="QPushButton{border-radius:60px;border:0px;}QPushButton::hover{background-color :#6d7f94;} QPushButton::pressed{background-color :#425473;}QToolTip { background-color: "+COLOREL[1]+"; color: white;border: black solid 1px}"
      # ======================= WIDGETS ==========================
        MIC = hoverButton(self)
        MIC.setStyleSheet(estilo)
        MIC.setGeometry(410, 50, 120, 120)
        MIC.setToolTip("Microfono")
        MIC.setIcon(QG.QIcon('Media/MICROFONO.png'))
        MIC.setIconSize(QSize(150, 150))

        AGG = hoverButton(self)
        AGG.setStyleSheet(estilo)
        AGG.setGeometry(280, 50, 120, 120)
        AGG.setToolTip("Agregar código Local")
        AGG.setIcon(QG.QIcon('Media/AGREGAR.png'))
        AGG.setIconSize(QSize(150, 150))


        TEC = hoverButton(self)
        TEC.setStyleSheet(estilo)
        TEC.setGeometry(150, 50, 120, 120)
        TEC.setToolTip("Búsqueda por teclado")
        TEC.setIcon(QG.QIcon('Media/TECLADO.png'))
        TEC.setIconSize(QSize(150, 150))

        AJUS = hoverButton(self)
        AJUS.setStyleSheet(estilo)
        AJUS.setGeometry(20, 50, 120, 120)
        AJUS.setToolTip("Ajustes")
        AJUS.setIcon(QG.QIcon('Media/AJUSTES.png'))
        AJUS.setIconSize(QSize(150, 150))
        
        MIC.clicked.connect(self.MICROFONO)
        AGG.clicked.connect(self.AGREGAR)
        TEC.clicked.connect(self.TECLADO)
        AJUS.clicked.connect(self.AJUSTES)

    CMIC = False
    VMIC =None
    def MICROFONO(self):
        if self.CMIC == False:
            self.VMIC = VentanaMIC(self)
            mensajeSaludos= SALUDOS[random.randrange(len(SALUDOS))]
            responder(mensajeSaludos)
            self.VMIC.Mensaje.setText(mensajeSaludos)
            self.VMIC.show()
            self.CMIC=True
        else:
            self.CMIC=False
            self.VMIC.close()
    CAG=False
    VAG=None
    def AGREGAR(self):
        if self.CAG==False:
            self.CAG=True
            self.VAG = VentanaAG(self)
            self.VAG.show()
        else:
           self.VAG.close()
           self.CAG=False
    VTEC=None
    CTEC=False
    def TECLADO(self):
        if self.CTEC==False:
            self.CTEC=True
            self.VTEC=VentanaTEC(self)
            mensajeSaludos= SALUDOS[random.randrange(len(SALUDOS))]
            responder(mensajeSaludos)
            self.VTEC.Mensaje.setText(mensajeSaludos)
            self.VTEC.show()
        else:
            self.CTEC=False
            self.VTEC.close()

    VRES=None
    CRES=False
    def AJUSTES(self):
        if self.CRES==False:
            self.VRES=VentanaAJUS(self)
            self.VRES.show()
            self.CRES=True
        else:
            self.CRES=False
            self.VRES.close()
        print("AJUSTANDO")
    def CERRAR(self):
        self.close()
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.width(), self.height())
            self.start = self.end
    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
    def Minimizar(self):
        self.showMinimized()
    def AGIL(self):
        ventana = VentanaPrincipalMin(None)
        ventana.show()
        self.close()

   
# ================================================================