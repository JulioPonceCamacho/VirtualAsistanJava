
#----------------------------------------------------
#Retorna -1 con error en busqueda de google
#Retorna -2 con error en we scrapping
#----------------------------------------------------




#Importamos las libresias necesarias
from lib2to3.pgen2.pgen import generate_grammar
import requests #Peticiones
from googlesearch import search#Google searcher
from bs4 import BeautifulSoup #BeautifulSoup version 4

REPOSITORIO='programarya'
#Funcion searcher en google:
def getGoogleSearch(query):
    #configuramos los parámetros de la busqueda:
    print(query)
    tld = 'com'
    lang = 'es'
    num = 2
    start = 0
    stop = num
    pause = 3.0
    #Obtenemos los resultados de la búsqueda:
    try:
        results = search(query,tld=tld,lang=lang,num=num,start=start,stop=stop,pause=pause)
        genArray = ['Google Results ->']
        for res in results:
            genArray.append(res)
        return genArray
    except:
        array = []
        array.append("Error en el servidor")
        return array

#Funcion de webscrapping en web seleccionada
def getWebResults(urls, keyword,n): #url: Objetivo de Scrapper, keyword: elemento en DOM a buscar
    try:
        url=urls[n]
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        genArray = []
        SoupObject = soup.find_all(keyword)#Se le pasa el objetivo del DOM a buscar
        for res in SoupObject:
            genArray.append(res.get_text())
        if len(genArray)==0:
            SoupObject = soup.find_all('pre')#Se le pasa el objetivo del DOM a buscar
            for res in SoupObject:
                genArray.append(res.get_text())
        if(len(genArray)>0):
            aux="/*       Resumen General        */\n"
            i=0
            posibles=""
            auxArray=[]
            while i<len(genArray):
                res=genArray[i]
                if '\n' in res:
                   aux=aux+res+"\n"
                   auxArray.append(res)
                   aux=aux+"/*        ...          */\n"
                else:
                    j=i
                    while '\n' in res or j<len(genArray):
                        res=genArray[j]
                        posibles=posibles+res+"\n"
                        j+=1
                    if j!=i:
                        i=j-1
                i+=1
            genArray=[]
            if posibles!="":
                aux=aux+"/*       Posibles resultados correctos       */\n"+posibles
            for res in auxArray:
                genArray.append(res)
            genArray.append(aux)
            if posibles!="":
                genArray.append("/*        Posibles datos utiles        */\n"+posibles)
    except:
        if n<len(urls):
            genArray=getWebResults(urls,keyword,n+1)
        else:
            genArray=[]
            genArray.append('Sin resultados')
    return genArray

def ObtenerRepositorios():
    with open('Local/RepositoriosCodigo.txt') as archivo:
        i=0
        rep=[]
        for linea in archivo:
            rep.append(linea.replace("\n",""))
    return rep
def ObtenerRepositoriosD():
    with open('Local/RepositoriosDefinicion.txt') as archivo:
        i=0
        rep=[]
        for linea in archivo:
            rep.append(linea.replace("\n",""))
    return rep
'''
busqueda = input('AppIn -> ')
googleArray = getGoogleSearch(str(busqueda))  #sintaxis+while+java:programarya
print(googleArray[1])
codeArray = getWebResults(googleArray[1], 'code')
print(codeArray[1])
'''
