from bs4 import BeautifulSoup
import re

def cleanLink(link):
    '''Clears the links from the great suspender extension'''
    result = re.search(r"\&uri=(.*)$",link) #Looks if the link has the format from the extension
    if result == None: #If it has not the format, returns the same link
        return link
    return result[1] #Returns the filter link

def get_folder(soup,name="",get_all=""):
    '''Extract all the links from a particular folder
    soup: html soup
    name: Name of the subfolder
    get_all: Indicates if the user wants to save all the sub folders'''
    tags = soup("h3") #Lista de todos los tags h3 del archivo html
    if len(tags) > 0: #If there are subfolders, looks for the subfolders
        if get_all=="" or get_all=="n":
            looking=input("insert the folder from wich you want to extract the links:") #Solicita al usuario el nombre de la carpeta de marcadores que desea abrir
            if looking == "-1":
                pass #If the user selects inputs "-1" , the function does not looks for subfolders
            else:
                if get_all=="":
                    get_all=input("Whould you like to get all the sub folders from this folder?[y/n]") #Ask the user if he wants to sabe al the subfolders
                    while get_all not in ["y","n"]:
                        get_all=input("Please insert a valid value")
                count = 0 #Indicador de la posicion de la carpeta
                for tag in tags: #Ciclo for que busca la carpeta de la cual se quieren extraer los links
                    count += 1
                    if len(tag.contents) >= 1 and tag.contents[0] == looking:
                        break #Detiene el ciclo for si encuentra la carpeta que se esta buscando
                soup_2 = soup("dl")[count] #Estrae la "sopa" correspondiente a la lista que contiene los links de la carpeta
                get_folder(soup_2,name=looking,get_all=get_all) #Recursively looks for the subfolder inside the current folder
        else: #If the user sets get_all as y(yes), itereta and saves al the subfolders
            for i in range(len(tags)):
                if len(tags[i].contents) >= 1: #If the tag has a valid folder name
                    looking = name+"-"+tags[i].contents[0] #Name of the folder
                    soup_2 = soup("dl")[i] #Extrats the "soup" corresponding to the folder
                    get_folder(soup_2,name=looking,get_all=get_all) #Recursively looks for the subfolder inside the current folder
    if name != "":
        tags = soup("a")
        with open("links({}).txt".format(name),"a") as file: #Abre el archivo links.txt para escribir los links de la carpeta en el
            for tag in tags: #Ciclo for que escribe los links de la carpeta al archivo txt
                result = cleanLink(tag.get("href",None))#re.search(link,tag.get("href",None)) #Extrae el link de youtube sin variables adicionales del valor que este en href
                file.write("{}\n".format(result)) #le agrega el salto de linea al final



#link = r"https\://www\.youtube\.com/watch\?v\=.{11}" #Regular expression que representa un link generico de youtube
fileName = input("insert the file name: ") #Solicita al usuario el archivo html que desea abrir
#fileName = "bookmarks_9_9_20.html" #Archivo html de los marcadores
#fileName = "toDownload.txt"
file = open(fileName,encoding="utf8") #Abre el archivo html en la variable file
#print(file.read())
soup = BeautifulSoup(file.read(), "html.parser") #Convierte el archivo html en una sopa de beatiful soup
file.close() #Se cierra el archivo para optimizar memoria ya que este no se volvera a utilziar
#looking="youtube" #Carpeta de marcadores que se quiere extraer
get_folder(soup)
