import os
import shutil
import re
import win32api
import threading
import zipfile

def move_file(origen,destino):
    '''Mueve el archivo de la ruta de orgen a la ruta de destino, verifica que la extension del archivo sea la misma'''
    if file_type(origen) != "dir" and file_type(origen) != file_type(destino):
        raise ValueError("The extension of the origin and destination file does not match") #Raises an exception if the file type doesn´t match
    count = 0 #Aux variable to know the "number" of the file in case the file name is repeated in the destination folder
    while (isfile(origen) and isfile(destino)) or (isdir(origen) and isdir(destino)): #Verifies that the destination file or folder does not exist.
        count += 1
        if isdir(origen):
            result=re.search(r".*\([0-9]+\)$",destino) #Verifies if the destination path already has a number at the end
            if result == None:
                destino += "({})".format(count) #If it does not have a number, it adds the count variable
            else:
                destino = "(".join(destino.split("(")[:-1])+"({})".format(count) #If it has a number at the end, it replaces it with the count value
        elif isfile(origen):
            extension = file_type(origen)
            result=re.search(r".*\([0-9]+\)\."+extension,destino) #Verifies if the destination path already has a number at the end
            if result == None:
                destino = destino.split(".")[0]+"({}).{}".format(count,extension) #If it has not a number, adds the count Variable
            else:
                destino = "(".join(destino.split("(")[:-1])+"({}).{}".format(count,extension) #If it has a number, replaces the number with the count value
    shutil.move(origen,destino) #Mueve el archivo de la ruta "origen" a la ruta "destino"

def file_type(file):
    '''Devuelve la extension del archivo que entra como parametro'''
    if isdir(file): return "dir" #Retorna "dir" si el archivo es una carpeta
    return file.split(".")[-1] #Separa el string por puntos y devuelve el ultimo elemento de la lista, correspondiente a la extension del archivo

def isdir(ruta):
    '''Verifica si la ruta ingresada es o no una carpeta'''
    return os.path.isdir(ruta)

def isfile(ruta):
    '''Verifica si la ruta ingresada es o no un archivo'''
    return os.path.isfile(ruta)

def unir_ruta(ruta,archivo):
    '''Retorna un string con la ruta absoluta del archivo'''
    return os.path.join(ruta,archivo)

def lista_archivos(carpeta):
    '''Devuelve una lista con el nombre de todos los archivos y las sub carpetas de la carpeta que entra como parametro'''
    return os.listdir(carpeta)

def fecha_creacion(archivo):
    '''Retorna la fecha de creación de un archivo, recive como entrada la ruta absoluta del archivo'''
    return os.path.getctime(archivo)

def ordenar_por_fecha(carpeta,archivos):
    '''Retorna la lista de archivos y carpetas ordenada por su fecha de creación de menor a mayor (archivos mas viejos primero)
    Recive como parametros carpeta (La ruta absoluta de la carpeta) y archivos (la lista de los nombres de los arhivos de la carpeta)'''
    aux = [unir_ruta(carpeta,x) for x in archivos] #Crea una lista con las rutas absolutas de todos los archivos en la carpeta
    aux.sort(reverse=True,key=fecha_creacion) #Organiza la lista aux por su fecha de creacion y la Retorna
    return aux

def clasificar_Archivo(archivo):
    '''Retorna un string con el nombre de la categoria del archivo
    Como entrada recive archivo, la ruta del archivo a clasificar'''
    imagenes=["JPG","JPEG","PNG","GIF"] #Lista con los formatos de imagenes mas comunes
    videos=["AVI","MP4","MPEG-4","MKV","FLV","MOV","WMV"] #Lista con los formatos de video mas comunes
    libros=["PDF","EPUB"] #Lista con los formatos de libros mas comunes
    ejecutables=["EXE"] #Lista con los formatos de archivos ejecutables
    compressedFolder=["ZIP","RAR","7Z"] #List of common compressed files' formats
    if isdir(archivo): return "folder" #retorna folder si el archivo es una carpeta
    if file_type(archivo).upper() in compressedFolder: return "compressed" #Returns compressed if the file is a compressed file
    if file_type(archivo).upper() in imagenes: return "imagen" #retorna imagen si el archivo es una imagen
    if file_type(archivo).upper() in videos: return "video"  #retorna video si el archivo es un video
    if file_type(archivo).upper() in libros: return "libro"  #retorna libro si el archivo es un libro
    if file_type(archivo).upper() in ejecutables: return "ejecutable" #retorna ejecutable si el archivo es un .exe
    return "otro" #Retorna otro si la extension del archivo no corresponde a ninguna categoria

def delete_file(file):
    '''Elimina el archivo que entra como parametro'''
    os.remove(file)

def create_dir(dir):
    '''Creates a new directory in the specidief path (dir)'''
    os.mkdir(dir)

def get_filename(path):
    '''Return the name of the file for a given path
    '''
    return os.path.basename(path)

def showMessage(message,title="",type="info",urgent=True,stop=True):
    '''Displays a windows MessageBox
    message: The message to be displayed
    type: the type of message to be displayed ["info","exclamation","question","warming","asterisk","stop","error","hand"]
    urgent = boolean, indicates if the message will be shown on top of all other open apps or not
    Stop = booleam, indicates if the message will stop the program, or if it will run on a separate thread
    '''
    if not stop:
        thread = threading.Thread(target=showMessage,args=(message,title,type,urgent)) #Creates a separate thread with the function
        thread.start() #Stars the thread
    else:
        types ={"info":0x00000040,"exclamation":0x00000030,"question":0x00000020,"warming":0x00000030,
                "asterisk":0x00000040,"stop":0x00000010,"error":0x00000010,"hand":0x00000010} #Dictionary that contains the values needed to display the selected icon
        if type not in types.keys(): #Verifies that the type is an available type
            type = "info"
        value = types[type] #int value with the configuration for the MessageBox command
        if urgent:
            value += 0x00001000 #Ads the top must configuration to show the message over all apps
        win32api.MessageBox(0, message, title, value) #Displays the message

def unzip(path,outdir="",remove=False):
    '''Unzips the file in the path to the outdir folder
    path: Absolute path of the zip files
    outdir: Destination dir of the uncompressed folder
    remove: Boolean, indicates if the file needs to be removed after beeing descompressed'''
    if file_type(path).lower() != "zip": #Raises an error if the path file is not a zip file
        raise Exception ("{} is not a zip file!".format(path))
    if outdir=="": #Sets the out dir to the same name as the file if this is not specified
        outdir = path.replace(".{}".format(file_type(path)),"")
    if not isdir(outdir): #Creates the out directory if this is not already created
        create_dir(outdir)
    with zipfile.ZipFile(path,"r") as zip_ref:
        zip_ref.extractall(outdir) #Extracts the zip file
    if remove:
        delete_file(path) #Removes the zip file if indicated so
