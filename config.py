import pyttsx3
VELOCIDAD_SPEECH=150
RESPUESTA_SPEECH='Si'
TEMA='Obscuro'
COLORESOBS=['#3d3d3d','#262626','white']
COLORESCLA=['#bac6d1','#26477c','black']
COLOREL=[]
ID_MIC=0
ID_AS=0
NOMBRE_MIC='Desconocido'

ARCH = '.conf.cfg'
def comprobarArchivo():
    import os
    if os.path.isfile(ARCH):
        pass
    else:
        file = open(ARCH, "w")
        file.write("")
        file.close()
        GenerarConfiguracionPorDefecto()

def GenerarConfiguracionPorDefecto():
    file = open(ARCH, "w")
    file.write("S_SPEECH:"+str(VELOCIDAD_SPEECH))
    file.write("\nR_SPEECH:"+RESPUESTA_SPEECH)
    file.write('\nTEMA:'+TEMA)
    MIC_NAM,ID_M=ObtenerMIC()
    file.write('\nID_MIC:'+str(ID_M))
    file.write('\nMIC:'+MIC_NAM)
    file.write('\nID_VOZ:'+ObtenerAsistenteDefecto())
    file.close()
def ObtenerAsistenteDefecto():  
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    return voices[0].id
def ObtenerConfiguracion():
    comprobarArchivo()
    with open(ARCH) as archivo:
        i=0
        for linea in archivo:
            if i == 0:
                VELOCIDAD_SPEECH=int(linea.replace("S_SPEECH:","").replace("\n",""))
            elif i == 1:
                RESPUESTA_SPEECH=linea.replace("R_SPEECH:","").replace("\n","")
            elif i == 2:
                TEMA=linea.replace("TEMA:","").replace("\n","")
            elif i == 3:
                ID_MIC=int(linea.replace('ID_MIC:','').replace("\n",""))
            elif i==4:
                NOMBRE_MIC=linea.replace('MIC:',"").replace("\n","")
            elif i==5:
                ID_AS=linea.replace('ID_VOZ:',"").replace("\n","")
            i+=1
    if TEMA=='Obscuro':
        return VELOCIDAD_SPEECH,RESPUESTA_SPEECH,TEMA,COLORESOBS,ID_MIC,NOMBRE_MIC,ID_AS
    elif TEMA=='Claro':
        return VELOCIDAD_SPEECH,RESPUESTA_SPEECH,TEMA,COLORESCLA,ID_MIC,NOMBRE_MIC,ID_AS
def CambiarConfiguracion(VEL,RES,TEM,ID_MIC,MIC,id_as):
    file = open(ARCH, "w")
    file.write("S_SPEECH:"+str(VEL))
    file.write("\nR_SPEECH:"+str(RES))
    file.write('\nTEMA:'+str(TEM))
    file.write('\nID_MIC:'+str(ID_MIC))
    file.write('\nMIC:'+str(MIC))
    file.write('\nID_VOZ:'+str(id_as))
    file.close()

def ObtenerMIC():
    import speech_recognition as sr
    sample_rate = 48000
    chunk_size = 2048
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    mic_list = sr.Microphone.list_microphone_names()
    for i, microphone_name in enumerate(mic_list):                     
        try: 
            with sr.Microphone(device_index = i, sample_rate = sample_rate, chunk_size = chunk_size) as source:      
                    return microphone_name, i
        except:
            pass


