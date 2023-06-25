import Reconocimiento

CARPETA = 'Local'
ARCHIVO = 'Local/Codigos.txt'
def comprobarArchivo(CARP,ARCH):
    import os
    if os.path.isdir(CARP):
        pass
    else:
        os.mkdir(CARP)
    if os.path.isfile(ARCH):
        pass
    else:
        file = open(ARCH, "w")
        file.write("/* \nEn este archivo se pueden encontrar los codigos locales almacenados para hacer uso de estos con el asistente. \n"
                +"La sintaxis utilizada para el almacenamiento local es la siguiente: \n"
                +"[Numero de lineas del bloque de codigo]\n"
                +"------------------------------------------------------------------\n"
                +"Identificador\n"
                +"Bloque de codigo\n"
                +"------------------------------------------------------------------\n */")
        file.close()

def Agregar(ID, Bloque ):
    comprobarArchivo(CARPETA, ARCHIVO)
    if(IdentificarExiste(ID)==False):
        f = open(ARCHIVO,'a')
        resultado=Bloque.split("\n")
        f.write('\n' + ID)
        f.write('\n' + '['+str(len(resultado)+2)+']')
        f.write('\n' + '------------------------------------------------------------------')
        f.write('\n' + Bloque)
        f.write('\n' + '------------------------------------------------------------------')
        f.close()
        return True
    else:
        return False
def IdentificarExiste(ID):
    linea = 9
    while linea < LineasTotales():
        with open(ARCHIVO) as f:
            data = f.readlines()[linea]
            data = data.replace("\n","")
        if ID == data:
            return True
        else:
            linea+=1
            with open(ARCHIVO) as f:
                data = f.readlines()[linea]
            data = data.replace("[","")
            data = data.replace("]","")
            linea = linea + int(data)+1
    return False

def LineasTotales():
    with open(ARCHIVO) as myfile:
        total_lines = sum(1 for line in myfile)
    return total_lines-1

def ConsultaCodigos():
    linea = 9
    Valores = []
    while linea < LineasTotales():
        with open(ARCHIVO) as f:
            Valor = ''
            Valor = Valor + str(linea)+'~'
            data = f.readlines()[linea]
            data = data.replace("\n","")
            Valor = Valor+data+'~'
            linea+=1
            with open(ARCHIVO) as f:
                data = f.readlines()[linea]
            data = data.replace("[","")
            data = data.replace("]","")
            Valor = Valor + data 
            Valor = Valor.replace("\n","")
            Valores.append(Valor)
            linea = linea + int(data)+1
    return Valores

def buscarCodigo(Linea,nombre,rango):
    inicio = Linea + 3
    Fin = inicio+rango -2
    with open(ARCHIVO) as f:
        data = f.readlines()[inicio:Fin]
    bloque = ''
    for i in data:
        bloque += i
    return nombre, bloque

    
def ObtenerCodigo(CLAVE):
    linea = 9
    CLAVE=CLAVE.upper()
    Valores = []
    Coincidencias =[]
    while linea < LineasTotales():
        Valores=[]
        with open(ARCHIVO) as f:
            data = f.readlines()[linea]
            data = data.replace("\n","")
            aux=data.upper()
            if CLAVE in aux:
                Valores.append(linea)
                Valores.append(data)
                linea+=1
                with open(ARCHIVO) as f:
                    data = f.readlines()[linea]
                data = data.replace("[","")
                data = data.replace("]","")
                Valores.append(data.replace("\n",""))
                linea = linea + int(data)+1
                Coincidencias.append(Valores)
            else:
                linea+=1
                with open(ARCHIVO) as f:
                    data = f.readlines()[linea]
                data = data.replace("[","")
                data = data.replace("]","")
                linea = linea + int(data)+1
    return Coincidencias

def BorrarCodigo(ID):
    linea = 9

    ArchivoAn=open(ARCHIVO,"r")
    lineas = ArchivoAn.readlines()
    ArchivoAn.close()
    an=""
    for l in lineas:
        an=an+l

    while linea < LineasTotales():
        with open(ARCHIVO) as f:
            data = f.readlines()[linea]
            data = data.replace("\n","")
        if ID == data:
            linea+=1
            with open(ARCHIVO) as f:
                data = f.readlines()[linea]
            data = data.replace("[","")
            data = data.replace("]","")
            fin = linea + int(data)
            with open(ARCHIVO) as f:
                bloque = f.readlines()[linea-1:fin+1]
            aux=""
            for l in bloque:
                aux=aux+l
            nuev=an.replace(aux,"")

            Archivo=open(ARCHIVO,"w")
            Archivo.write(nuev[:-1])
            Archivo.close()            
            return True
        else:
            linea+=1
            with open(ARCHIVO) as f:
                data = f.readlines()[linea]
            data = data.replace("[","")
            data = data.replace("]","")
            linea = linea + int(data)+1
    return False
def existe(val, lista):
    for com in lista:
        if val==com:
            return True
    return False

def ActualizarCodigo(ID,Bloque):
    BorrarCodigo(ID)
    return Agregar(ID,Bloque)

def formatoHTML(texto):
    texto = texto.replace("<","12121212121")
    texto = texto.replace(">","31313131313")
    texto = texto.replace("=","<font color='cyan'>=</font>")
    texto = texto.replace(";","<font color='green'>;</font>")
    texto = texto.replace("-","<font color='chocolate'>-</font>")
    texto = texto.replace("\n","<br>")
    texto = texto.replace("}","<font color='tomato'>}</font>")
    texto = texto.replace("{","<font color='tomato'>{</font>")
    texto = texto.replace("(","<font color='cyan'>(</font>")
    texto = texto.replace(")","<font color='cyan'>)</font>")
    texto = texto.replace("[","<font color='chartreuse'>[</font>")
    texto = texto.replace("]","<font color='chartreuse'>]</font>")
    texto = texto.replace(";","<font color='aquamarine'>;</font>")
    texto = texto.replace(" : ","<font color='cyan'> : </font>")
    texto = texto.replace(".","<font color='cyan'>.</font>")
    texto = texto.replace("+","<font color='chocolate'>+</font>")
    texto = texto.replace("*","<font color='chocolate'>*</font>")
    texto = texto.replace("!=","<font color='cyan'>!=</font>")
    texto = texto.replace("!","<font color='cyan'>!</font>")
    texto = texto.replace("%","<font color='chocolate'>%</font>")
    texto = texto.replace("/*     Codigos de la Web     */","<font color='green'>/*     Codigos de la Web     */</font>")
    texto = texto.replace("*/","<font color='green'>*/</font>")
    texto = texto.replace("/*","<font color='green'>/*</font>")
    texto = texto.replace(" / ","<font color='chocolate'> / </font>")
    texto = texto.replace("//","<font color='chartreuse'>//</font>")
    texto = texto.replace("~","<font color='chartreuse'>~</font>")
    texto=texto.replace("for","<font color='cornflowerblue'>for</font>")
    texto=texto.replace("while","<font color='cornflowerblue'>while</font>")
    texto=texto.replace("Scanner","<font color='cornflowerblue'>Scanner</font>")
    texto=texto.replace("public ","<font color='fuchsia'>public </font>")
    texto=texto.replace("private ","<font color='fuchsia'>private </font>")
    texto=texto.replace("final ","<font color='fuchsia'>final </font>")
    texto=texto.replace("static ","<font color='aquamarine'>static </font>")
    texto=texto.replace("class ","<font color='aquamarine'>class </font>")
    texto=texto.replace("System","<font color='aqua'>System</font>")
    texto=texto.replace("out","<font color='lightpink'>out</font>")
    texto=texto.replace("\"","<font color='yellow'>\"</font>")
    texto=texto.replace(" do ","<font color='cornflowerblue'> do </font>")
    texto=texto.replace("package","<font color='cornflowerblue'>package</font>")
    texto=texto.replace("import ","<font color='cornflowerblue'>import </font>")
    texto=texto.replace("if ","<font color='cornflowerblue'>if </font>")
    texto=texto.replace("else","<font color='cornflowerblue'>else</font>")
    texto=texto.replace("break","<font color='cornflowerblue'>break</font>")
    texto=texto.replace("pass","<font color='cornflowerblue'>pass</font>")
    texto=texto.replace("int ","<font color='cornflowerblue'>int </font>")
    texto=texto.replace("short ","<font color='cornflowerblue'>short </font>")
    texto=texto.replace("long ","<font color='cornflowerblue'>long </font>")
    texto=texto.replace("float ","<font color='cornflowerblue'>float </font>")
    texto=texto.replace("double ","<font color='cornflowerblue'>double </font>")
    texto=texto.replace("boolean ","<font color='cornflowerblue'>boolean </font>")
    texto=texto.replace("true","<font color='cornflowerblue'>true</font>")
    texto=texto.replace("false","<font color='cornflowerblue'>false</font>")
    texto=texto.replace("&","<font color='lightpink'>&</font>")
    texto=texto.replace("|","<font color='lightpink'>|</font>")
    texto=texto.replace("void","<font color='yellow'>void</font>")
    texto=texto.replace("null","<font color='coral'>null</font>")
    texto=texto.replace("char ","<font color='cornflowerblue'>char </font>")
    texto=texto.replace("String","<font color='cornflowerblue'>String</font>")
    texto=texto.replace("   ","&nbsp;&nbsp;&nbsp;")
    texto=texto.replace("\s","&nbsp;")
    texto=texto.replace("12121212121","<font color='chartreuse'>&lt;</font>")
    texto=texto.replace("31313131313","<font color='chartreuse'>&gt;</font>")
    return texto
def formatoTxt(texto):
    texto = texto.replace("<font color='chartreuse'>&lt;</font>","<")
    texto=texto.replace("<font color='chartreuse'>&gt;</font>",">",)
    texto=texto.replace("&nbsp;&nbsp;&nbsp;","\t",)
    texto = texto.replace("<font color='cyan'>=</font>","=")
    texto = texto.replace("<font color='green'>;</font>",";")
    texto = texto.replace("<font color='chocolate'>-</font>","-")
    texto = texto.replace("<br>","\n")
    texto = texto.replace("<font color='tomato'>}</font>","}")
    texto = texto.replace("<font color='tomato'>{</font>","{")
    texto = texto.replace("<font color='cyan'>(</font>","(")
    texto = texto.replace("<font color='cyan'>)</font>",")")
    texto = texto.replace("<font color='chartreuse'>[</font>","[")
    texto = texto.replace("<font color='chartreuse'>]</font>","]")
    texto = texto.replace("<font color='aquamarine'>;</font>",";")
    texto = texto.replace("<font color='cyan'> : </font>"," : ")
    texto = texto.replace("<font color='cyan'>.</font>",".")
    texto = texto.replace("<font color='chocolate'>+</font>","+")
    texto = texto.replace("<font color='chocolate'>*</font>","*")
    texto = texto.replace("<font color='cyan'>!=</font>","!=")
    texto = texto.replace("<font color='cyan'>!</font>","!")
    texto = texto.replace("<font color='chocolate'>%</font>","%")
    texto = texto.replace("<font color='green'>/*     Codigos de la Web     */</font>","/*     Codigos de la Web     */")
    texto = texto.replace("<font color='green'>*/</font>","*/",)
    texto = texto.replace("<font color='green'>/*</font>","/*")
    texto = texto.replace("<font color='chocolate'> / </font>"," / ")
    texto = texto.replace("<font color='chartreuse'>//</font>","//")
    texto = texto.replace("<font color='chartreuse'>~</font>","~")
    texto=texto.replace("<font color='cornflowerblue'>for</font>","for")
    texto=texto.replace("<font color='cornflowerblue'>while</font>","while")
    texto=texto.replace("<font color='cornflowerblue'>Scanner</font>","Scanner")
    texto=texto.replace("<font color='fuchsia'>public </font>","public ")
    texto=texto.replace("<font color='fuchsia'>private </font>","private ")
    texto=texto.replace("<font color='fuchsia'>final </font>","final ")
    texto=texto.replace("<font color='aquamarine'>static </font>","static ")
    texto=texto.replace("<font color='aquamarine'>class </font>","class ")
    texto=texto.replace("<font color='aqua'>System</font>","System")
    texto=texto.replace("<font color='lightpink'>out</font>","out")
    texto=texto.replace("<font color='yellow'>\"</font>","\"")
    texto=texto.replace("<font color='cornflowerblue'> do </font>"," do ")
    texto=texto.replace("<font color='cornflowerblue'>package</font>","package")
    texto=texto.replace("<font color='cornflowerblue'>import </font>","import ")
    texto=texto.replace("<font color='cornflowerblue'>if </font>","if ")
    texto=texto.replace("<font color='cornflowerblue'>else</font>","else")
    texto=texto.replace("<font color='cornflowerblue'>break</font>","break")
    texto=texto.replace("<font color='cornflowerblue'>pass</font>","pass")
    texto=texto.replace("<font color='cornflowerblue'>int </font>","int ")
    texto=texto.replace("<font color='cornflowerblue'>short </font>","short ")
    texto=texto.replace("<font color='cornflowerblue'>long </font>","long ")
    texto=texto.replace("<font color='cornflowerblue'>float </font>","float ")
    texto=texto.replace("<font color='cornflowerblue'>double </font>","double ")
    texto=texto.replace("<font color='cornflowerblue'>boolean </font>","boolean ")
    texto=texto.replace("<font color='cornflowerblue'>true</font>","true")
    texto=texto.replace("<font color='cornflowerblue'>false</font>","false")
    texto=texto.replace("<font color='lightpink'>&</font>","&")
    texto=texto.replace("<font color='lightpink'>|</font>","|")
    texto=texto.replace("<font color='yellow'>void</font>","void")
    texto=texto.replace("<font color='coral'>null</font>","null")
    texto=texto.replace("<font color='cornflowerblue'>char </font>","char ")
    texto=texto.replace("<font color='cornflowerblue'>String</font>","String")
    texto=texto.replace(" &nbsp; ","   ")
    return texto
