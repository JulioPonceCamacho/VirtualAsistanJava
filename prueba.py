''''
from pocketsphinx import LiveSpeech

hmm= 'Modelos/es-mx'
lm = 'Modelos/es-mx.lm.bin'
dict = 'Modelos/cmudict-es-mx.dic'


recognizer = LiveSpeech (verbose=False, sampling_rate=16500, buffer_size=2048,no_search=False, full_utt=False, hmm=hmm, lm=lm,dict=dict)

for phrase in recognizer:
    print(phrase)

import re
def BuscarEnDict(mensaje):
    PALABRA=''
    SALUDO = ['HOLA','QUE TAL','BUEN DIA','BUENAS TARDES','BUENAS NOCHES','SALUDOS']
    f = open("Diccionario/CLAVE_LOCAL.txt", "r")
    for palabra in SALUDO:
        if palabra in mensaje:
            return 'SALUDO', mensaje
    AYUDA = ['NECESITO AYUDA','PUEDES AYUDARME','COMO FUNCIONAS','AYUDA','AYUDAME','CUAL ES TU FUNCIONAMIENTO']
    for palabra in AYUDA:
        if palabra in mensaje:
            return 'AYUDA',mensaje
    for linea in f:
        LINEAN = linea.replace('\n','')
        if  LINEAN in mensaje:
            val = mensaje.replace(LINEAN,'')
            f.close()
            return 'LOCAL', val
    f.close()
    f = open("Diccionario/CLAVE_WEB.txt", "r")
    for linea in f:
        LINEAN = linea.replace('\n','')
        if  LINEAN in mensaje:
            val = mensaje.replace(LINEAN,'')
            f.close()
            return 'WEB', val
    f.close()
    
    return 'NONE',''

def identificar(mensaje):
    mensaje = mensaje.upper()
    longitud = len(mensaje)
    if(longitud<4):
        print("Disculpa, no pude comprender tu petición se un poco mas claro.")
        return False, ''
    Tipo, mensaje2=BuscarEnDict(mensaje)
    if (Tipo == 'LOCAL'):
        print("Es una busqueda local")
        print("Se va a buscar = "+mensaje2)
        mensaje2=borrarBasura(mensaje2)
        print("Mensaje Optimizado="+mensaje2)
    elif(Tipo == 'WEB'):
        print("Es una busqueda Web")
        print("Se va a buscar = "+mensaje2)
        mensaje2=borrarBasura(mensaje2)
        print("Mensaje Optimizado="+mensaje2)
    elif(Tipo == 'SALUDO'):
        print('Que tal estoy para servirte')
        var=input()
    elif(Tipo == 'AYUDA'):
        print('Por su puesto, ¿Como te puedo ayudar?')
        var =input()
    #Ayuda de tipo Local
        if 'COMO PUEDO ALMACENAR CODIGOS' in var or 'COMO PUEDO GUARDAR CODIGOS' in var:
            print("Para ello tienes que dar en el icono de codigo local y seguido de ello tienes que establecer un nombre de identificador"+
            " y seguido colocar el bloque de codigo que utilizaras. Al final solo das en el boton de agregar y tu codigo estara en tu repositorio de"+
            " codigos locales para que los consultes en cualquier momento.")
        elif 'PARA QUE SIRVE AGREGAR CODIGO LOCAL' in var:
            print("Permite que almacenes tus codigos en un fichero local para que puedas acceder a ellos cuando lo desees.")
        elif 'QUE ES ALMACENAR CODIGO LOCAL' in var:
            print("Es la función que permite que almacenes tus codigos en un fichero local para que puedas acceder a ellos cuando lo desees a traves de un Identificador.")
            
    #Ayuda de tipo WEB
        elif 'PUEDO BUSCAR' in var or 'PUEDO HACER' in var or 'PUEDO BUSCAR' in var :
            print("Puedes realizar la busqueda de definiciones, sintaxis y algoritmos, estos se buscaran en repositorios de la Web.")
        elif 'COMO PUEDO BUSCAR DEFINICIONES' in var or 'COMO PUEDO BUSCAR CONCEPTOS' in var:
            print("Solo basta con mencionar que requieres una definicion y seguido de que, por ejemplo, Necesito la definicion de un ciclo")
        elif 'COMO PUEDO BUSCAR SINTAXIS' in var :
            print("Solo basta con mencionar que requieres una sintaxis y seguido cual, por ejemplo, Busca la sintaxís de for")
        elif 'COMO PUEDO BUSCAR ALGORITMOS' in var :
            print("Solo basta con mencionar que requieres una sintaxis y seguido cual, por ejemplo, Busca el algoritmo Burbuja")
    
    #Ayuda General
        AYUDA_GENERAL = ['COMO FUNCIONAS','COMO FUNCIONA','QUE PUEDO HACER','QUE ES LO QUE HACES','CUAL ES TU FUNCION','AYUDA GENERAL']
        for val in AYUDA_GENERAL:
            if val in var:
                print("Puedes realizar 2 funciones generales, consultar por internet algun aspecto como sintaxis, definciones o algoritmos por medio de la entrada de voz o por el teclado,"+
                " en la interfaz principal puedes encontrar esos iconos de acceso, o bien puedes consultar o agregar codigos en tu propio repositorio local. Un ejemplo de consulta es"+
                " Busca la sintaxis de for, o bien, busca localmente el algoritmo de conteo")
                break
        #Ayuda de configurarción
        AYUDA_CONFIGURACION = ['COMO PUEDO CAMBIAR EL TEMA','QUE PUEDO']
    elif(Tipo == 'NONE'):
        print("Disculpa, no pude entender tu solicitud, intenta de nuevo")
        print("Si requieres ayuda para saber como funciono solo dime: Necesito Ayuda")
        return  False
def repl_func(match):
  if match == True:
    return " "

def borrarBasura(mensaje):
    CLAV = [' EL ', ' EN ',' LA ','LA ',' ES ',' CUAL ',' PUEDES ',' PORFAVOR ','PORFAVOR ','PUEDES ',' PUEDES', 
            ' QUE ',' NECESITO','PODRIAS']
    i = 0
    val = re.sub(r"\s+", " ", mensaje)
    while i < len(CLAV): 
        val = val.replace(CLAV[i],"")
        i+=1
    return val

print("Ingresa palabras: ")
mensaje = input()
identificar(mensaje)


'''
'''
# coding: utf-8
import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window size
        self.WIDTH = 300
        self.HEIGHT = 300
        self.resize(self.WIDTH, self.HEIGHT)

        # Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.WIDTH, self.HEIGHT)

        # Initial
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.6)

        radius = 30
        self.centralwidget.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            """.format(radius)
        )


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

'''
'''
import time
import threading
 
class th1(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(th1, self).__init__(*args, **kwargs)
        self._stop = threading.Lock()
    def stop(self):
        self._stop.set()
    def stopped(self):
        return self._stop.isSet()
    def run(self):
        while True:
            if self.stopped():
                return
            print("Hello, world!")
            time.sleep(1)
 
x = th1()
x.start()
time.sleep(5)
x.stop()
x.join()




import speech_recognition as sr
  
mic_name = "Asignador de sonido Microsoft - Input"
sample_rate = 48000
chunk_size = 2048
r = sr.Recognizer()
r.dynamic_energy_threshold = False

mic_list = sr.Microphone.list_microphone_names()
  
for i, microphone_name in enumerate(mic_list):                     
    try: 
        with sr.Microphone(device_index = i, sample_rate = sample_rate, chunk_size = chunk_size) as source:      
                print( "ID: "+str(i)+" Todo bien-->"+microphone_name)
    except:
        pass

val=input("Microfono:")

with sr.Microphone(device_index = 0, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source2:
    
    
    r.adjust_for_ambient_noise(source2)
    print("Say Something")
    
    audio = r.listen(source2)
          
    try:
        text = r.recognize_google(audio,language="es-mx")
        print( "you said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
      
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

        

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
  print("ID: %s" % voice.id)
  print("Name: %s" % voice.name)
  print("Age: %s" % voice.age)
  print("Gender: %s" % voice.gender)
  print("Languages Known: %s" % voice.languages)
  
#----------------------------------------------------
#Retorna -1 con error en busqueda de google
#Retorna -2 con error en we scrapping
#----------------------------------------------------




#Importamos las libresias necesarias
import requests #Peticiones
from googlesearch import search #Google searcher
from bs4 import BeautifulSoup #BeautifulSoup version 4
#Funcion searcher en google:
def getGoogleSearch(query):
    #configuramos los parámetros de la busqueda:
    print(query)
    tld = 'com'
    lang = 'es'
    num = 2
    start = 0
    stop = num
    pause = 2.0
    #Obtenemos los resultados de la búsqueda:
    #try:
    results = search(query,tld=tld,lang=lang,num=num,start=start,stop=stop,pause=pause)
    genArray = []
    for res in results:
        genArray.append(res)
    return genArray
    #except:
     #   return -1;


#Funcion de webscrapping en web seleccionada
def getWebResults(url, keyword): #url: Objetivo de Scrapper, keyword: elemento en DOM a buscar
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        genArray = []
        SoupObject = soup.find_all(keyword)#Se le pasa el objetivo del DOM a buscar
        for res in SoupObject:
            genArray.append(res.get_text())
        return genArray
    except:
        return -2

busqueda = input('AppIn -> ')
busqueda = 'programacion+definicion+'+busqueda
googleArray = getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
print(googleArray[0])
codeArray = getWebResults(googleArray[0], 'p')
print(codeArray[0])

#polimorfismo[ok], java, programacion, calses, arreglos[detalle], matrices, objetos, recursividad[formato], metodo, atributos, palabras reservadas, paradigmas, funciones, ciclos, sentencias, socket, hilo, base de datos, parser, datos, tipos de datos, declaracion

'''''
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice: %s" % voice.name)
    print(" - ID: %s" % voice.id)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    print("\n")