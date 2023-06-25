from tkinter.messagebox import NO
import webbrowser
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import pyttsx3
import os
import random
import socket 
import threading
import re
import multiprocessing as pr
from difflib import SequenceMatcher as SM

import config as cf

VELOCIDAD_SPEECH,RESPUESTA_SPEECH,TEMA,COLOREL,ID_MIC,NOMBRE_MIC,ID_AS=cf.ObtenerConfiguracion()

NOMBRE_ARCHIVO="SALIDA.mp3"
mic_name = "Asignador de sonido Microsoft - Input"
sample_rate = 48000
chunk_size = 2048

r = sr.Recognizer() 
r.dynamic_energy_threshold = False

SALUDOS = ["Hola, ¿Como estás? ¿Como te ayudo?","¿Que tal?, ¿Como puedo Ayudarte?","Hola, ¿En que te ayudo?","Saludos ¿Como puedo servirte?"]
ADIOS = ["Hasta luego, buen dia","Excelente Día","Adios, nos vemos luego",]
CORRECTO= ["Este es el resultado encontrado.","Buena noticia, hay resultados","Hay resultados.","El resultado se muestra en la ventana."]
ERRONEO = ["Lo siento, no logre encontrar nada relacionado.","No se encontraron coincidencias, prueba de otra forma.","Sin resultados, trata de "]
SINENTENDER= ["Lo siento, no comprendo tu solicitud.","Intenta de nuevo.","Se un poco más claro porfavor.","Disculpa, no puedo entenderte.","Trata de nuevo."]


def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def comprobarConexion():
    testConn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        testConn.connect(('http://www.youtube.com', 100))
        testConn.close()
        return True
    except:
        testConn.close()
        return False
def Coincidencia(text1,text2):
    return (SM(None, text1, text2).ratio())

def asistenteRespuesta(n,texto):
    ''''
    if checkFileExistance(NOMBRE_ARCHIVO)==True:
        os.remove(NOMBRE_ARCHIVO)
    if comprobarConexion()==True:
        tts = gTTS(texto, lang='es-us',)
        with open(NOMBRE_ARCHIVO, "wb") as archivo:
            tts.write_to_fp(archivo)
        try:
            playsound(NOMBRE_ARCHIVO)
        except:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150) # Control de velocidad
            text = " "+texto
            engine.say(text)
            engine.runAndWait()
    else:
    '''''
    if RESPUESTA_SPEECH == 'Si':
        engine = pyttsx3.init()

        engine.setProperty("rate", VELOCIDAD_SPEECH) # Control de velocidad
        engine.setProperty("voice",ID_AS)
        text = " "+texto
        engine.say(text)
        engine.runAndWait()
        engine.stop()

def responder(texto):
   hilo = pr.Process(name="Respuesta",target=asistenteRespuesta,args=(0,texto))
   hilo.start()


def reconocer():
    with sr.Microphone(device_index = ID_MIC, sample_rate = sample_rate, 
                        chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text=r.recognize_google(audio,language="es-mx")
            mensaje='{}'.format(text)
            identificar(mensaje)
            return mensaje
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            responder("Lo siento, puede que no tengas conexión a internet.")
        except:
            if checkFileExistance(NOMBRE_ARCHIVO)==True:
                os.remove(NOMBRE_ARCHIVO)
            if comprobarConexion()==True:
                return "No entendi tu petición"
            else:
                return "Lo siento, no tienes conexión a internet. Intenta mas tarde"

def BuscarEnDict(mensaje):
    PALABRA=''
    AYUDA = ['NECESITO AYUDA','PUEDES AYUDARME','COMO FUNCIONAS','AYUDA','AYUDAME']
    for palabra in AYUDA:
        aux1=palabra.split(" ")
        aux2=mensaje.split(" ")
        if len(aux2)>=len(aux1):
            concidencia=0
            val=0
            for pal in aux1:
                concidencia+=Coincidencia(pal, aux2[val]) / len(aux1)
                val+=1
            if(concidencia>0.90):
                print("coincidencia: "+str(concidencia))
                while val < len(aux2):
                    mensaje+=aux2[val]+" "
                    val+=1
                print(mensaje)
                return 'AYUDA',mensaje
    f = open("Diccionario/CLAVE_LOCAL.txt", "r")
    for linea in f:
        LINEAN = linea.replace('\n','')
        aux1=LINEAN.split(" ")
        aux2=mensaje.split(" ")
        if len(aux2)>len(aux1):
            concidencia=0
            val=0
            for pal in aux1:
                concidencia+=Coincidencia(pal, aux2[val]) / len(aux1)
                val+=1
            if(concidencia>0.90):
                print("coincidencia: "+str(concidencia))
                mensaje=""
                while val < len(aux2):
                    mensaje+=aux2[val]+" "
                    val+=1
                print(mensaje)
                f.close()
                return 'LOCAL', mensaje
    f.close()
    f = open("Diccionario/CLAVE_WEB.txt", "r")
    for linea in f:
        LINEAN = linea.replace('\n','')
        aux1=LINEAN.split(" ")
        aux2=mensaje.split(" ")
        if len(aux2)>len(aux1):
            concidencia=0
            val=0
            for pal in aux1:
                concidencia+=Coincidencia(pal, aux2[val]) / len(aux1)
                val+=1
            if(concidencia>0.90):
                print("coincidencia: "+str(concidencia))
                RES=['SINTAXIS', 'ALGORITMO', 'CODIGO', 'PROGRAMA', 'FUENTE' , 'CODIFICACION']
                mensaje=""
                for v in RES:
                    if v in aux1:
                        mensaje=v+" "
                        break
                while val < len(aux2):
                    mensaje+=aux2[val]+" "
                    val+=1
                print(mensaje)
                f.close()
                return 'WEB', mensaje
    f.close()

    SALUDO = ['HOLA','QUE TAL','BUEN DIA','BUENAS TARDES','BUENAS NOCHES','SALUDOS']
    for palabra in SALUDO:
        aux1=palabra.split(" ")
        aux2=mensaje.split(" ")
        if len(aux2)>=len(aux1):
            concidencia=0
            val=0
            for pal in aux1:
                concidencia+=Coincidencia(pal, aux2[val]) / len(aux1)
                val+=1
            print("coincidencia: "+str(concidencia))
            if(concidencia>0.90):
                return 'SALUDO', mensaje

    return 'WEB_DEF',mensaje

def identificar(mensaje):
    try:
        mensaje = mensaje.upper()
    except:
        return False,'NONE','Disculpa, no te escuche.'
    longitud = len(mensaje)
    if(longitud<4):
        return False,'NO', ''
    Tipo, mensaje2=BuscarEnDict(mensaje)
    print(Tipo)
    if (Tipo == 'LOCAL'):
        mensaje2=borrarBasura(mensaje2)
        return True,Tipo,mensaje2
    elif(Tipo == 'WEB'):
        print("Es una busqueda Web")
        print("Se va a buscar = "+mensaje2)
        if 'JAVA' in mensaje2:
            pass
        else:
            mensaje2=mensaje2+" JAVA"
        if 'CONCEPTO' in mensaje2 or 'DEFINICI' in mensaje2  or 'DEFINICIÓN' in mensaje2 or 'SIGNIFIC' in mensaje2 or 'SIGNIFICA' in mensaje2 or 'QUE ES' in mensaje2 or 'QUÉ ES' in mensaje2: 
            if 'JAVA' in mensaje2:
                mensaje2=mensaje2.replace("JAVA","PROGRAMACION")
            mensaje2=borrarBasura(mensaje2)
            print("Mensaje Optimizado="+mensaje2)
            return True, Tipo+"_DEF",mensaje2
        else:
            mensaje2=borrarBasura(mensaje2)
            print("Mensaje Optimizado="+mensaje2)
            return True, Tipo,mensaje2
    elif(Tipo == 'SALUDO'):
        mensajeSaludos= SALUDOS[random.randrange(len(SALUDOS))]
        return True,Tipo,mensajeSaludos
    elif 'NECESITO AYUDA' in mensaje2 or'PUEDES AYUDARME' in mensaje2 or 'AYUDAME' in mensaje2 or 'AYUDA' == mensaje2:
        res='Por su puesto, ¿Como te puedo ayudar? Puedes decirme tu peticion escrita o vocalmente, pero tienes que iniciar con la palabra AYUDA'
        return True,'AYUDA',res
    elif 'AYUDA' in mensaje2 or 'UNA PREGUNTA' in mensaje2 or 'PREGUNTA' in mensaje2:  
        #Ayuda de tipo Local
        if 'COMO PUEDO ALMACENAR CODIGOS' in mensaje2 or 'COMO PUEDO GUARDAR CODIGOS' in mensaje2 or 'GUARDAR CODIGOS' in mensaje2 or 'ALMACENAR CODIGOS' in mensaje2:
                res="Para ello tienes que dar en el icono de codigo local y seguido de ello tienes que establecer un nombre de identificador y seguido colocar el bloque de codigo que utilizaras. Al final solo das en el boton de agregar y tu codigo estara en tu repositorio de codigos locales para que los consultes en cualquier momento."
                return True,'AYUDA',res
        elif 'PARA QUE SIRVE AGREGAR CODIGO LOCAL' in mensaje2 or 'CODIGO LOCAL' in mensaje2 in 'LOCAL' in mensaje2:
                res="Permite que almacenes tus codigos en un fichero local para que puedas acceder a ellos cuando lo desees."
                return True,"AYUDA",res
        elif 'QUE ES ALMACENAR CODIGO LOCAL' in mensaje2:
                res="Es la función que permite que almacenes tus codigos en un fichero local para que puedas acceder a ellos cuando lo desees a traves de un Identificador."
                return True,'AYUDA',res
        #Ayuda de tipo WEB
        elif 'QUE PUEDO BUSCAR' in mensaje2 or 'PUEDO HACER' in mensaje2 :
                res="Puedes realizar la busqueda de definiciones, sintaxis y algoritmos, estos se buscaran en repositorios de la Web."
                return True,'AYUDA',res
        elif 'COMO PUEDO BUSCAR DEFINICIONES' in mensaje2 or 'COMO PUEDO BUSCAR CONCEPTOS' in mensaje2:
                res="Solo basta con mencionar que requieres una definicion y seguido de que, por ejemplo, Necesito la definicion de un ciclo"
                return True,'AYUDA',res

        elif 'BUSCAR SINTAXIS' in mensaje2 :
                res="Solo basta con mencionar que requieres una sintaxis y seguido cual, por ejemplo, Busca la sintaxís de for"
                return True,'AYUDA',res
        elif 'BUSCAR ALGORITMOS' in mensaje2 :
                res="Solo basta con mencionar que requieres una sintaxis y seguido cual, por ejemplo, Busca la sintaxis del ciclo for"
                return True,'AYUDA',res
        elif 'BUSCAR DEFINCION' in mensaje2 :
                res="Solo basta con mencionar que requieres un concepto o definción y seguido cual, por ejemplo, Busca el concepto de clase"
                return True,'AYUDA',res
        #Ayuda General
        elif 'COMO FUNCIONAS' in mensaje2 or 'COMO FUNCIONA' in mensaje2 or 'QUE PUEDO HACER' in mensaje2 or 'QUE ES LO QUE HACES' in mensaje2 or 'CUAL ES TU FUNCION' in mensaje2 or 'AYUDA GENERAL' in mensaje2:
                res="Puedes realizar 2 funciones generales, consultar por internet algun aspecto como sintaxis, definciones o algoritmos por medio de la entrada de voz o por el teclado, en la interfaz principal puedes encontrar esos iconos de acceso, o bien puedes consultar o agregar codigos en tu propio repositorio local. Un ejemplo de consulta es Busca la sintaxis de for, o bien, busca localmente el algoritmo de conteo"
                return True,'AYUDA',res
        #Ayuda de configurarción
        elif 'CAMBIAR EL TEMA' in mensaje2 or 'TEMA' in mensaje2:
            res="En la sección de configuración puedes encontrar el apartado de Tema" 
            return True,'AYUDA',res
        elif 'DESACTIVAR VOZ' in mensaje2 or 'VOZ' in mensaje2:
            res="En la sección de configuración puedes encontrar el apartado de Voz" 
            return True,'AYUDA',res
        elif 'DISPOSITIVO' in mensaje2 or 'MICROFONO' in mensaje2:
            res="En la sección de configuración puedes encontrar el apartado de Dispositivos" 
            return True,'AYUDA',res
        else:
            res="Disculpa, no logro entender tu petición." 
            return True,'AYUDA',res
    elif Tipo=='WEB_DEF':
        if 'JAVA' in mensaje2:
            pass
        else:
            mensaje2=mensaje2+" JAVA"
        return True,Tipo,mensaje+' PROGRAMACION'
    elif(Tipo == 'NONE'):
        NO=SINENTENDER[random.randrange(len(SINENTENDER))]
        return  False,'NONE',NO
def repl_func(match):
  if match == True:
    return " "

def borrarBasura(mensaje):
    CLAV = ['DE ',' EL ', ' EN ',' LA ','LA ',' CUAL ',' PUEDES ',' PORFAVOR ','PORFAVOR ','PUEDES ',' PUEDES', 
            ' QUE ',' NECESITO','PODRIAS']
    i = 0
    print(mensaje)
    val = re.sub(r"\s+", " ", mensaje)
    while i < len(CLAV): 
        val = val.replace(CLAV[i]," ")
        i+=1
    val = re.sub(r"\s+", " ", val)
    val=val.strip()
    return val