from FilesManagement import *

def readDirectorys():
    '''Reads the content of directorys.txt file and returns a
    dictionary fordelName:forderRoute with the folders contained
    in the file
    '''
    directorys = {} #Dictionary that will contain the names and routes of the objective folders
    with open("directorys.txt") as file:
        for line in file.readlines(): #Iterates over the lines of the file
            line = line.strip() #Remove the \n character
            if line != "": #If the line is not empy, saves the content of the line in the dictionary
                line = line.split(",")
                directorys[line[0]]=line[1]
                if not isdir(line[1]):
                    create_dir(line[1]) #Creates the directory if it doesn´t exist
    return directorys #Returns the filled dictionary

def print_directorys():
    '''Imprime el contenido del diccionario directorys en forma de tabla
    '''
    toPrint = "Nombre\t|Ruta\n"
    for directory in directorys:
        toPrint += "{}\t|{}\n".format(directory,directorys[directory])
    print(toPrint)

def mover_archivo(ruta,ruta_destino= ""):
    '''Mueve el archivo ruta a la carpeta ruta_destino
       Si ruta destino no se especifica al momento de llamar la funcion se le pregunta
       al usuario a donde quiere mover la carpeta
       ruta: Posicion actual del archivo que se desea mover
       ruta_destino: Ruta a la cual se desea mover el archivo'''
    nombre_archivo = get_filename(ruta) #Nombre del archivo
    if ruta_destino != "":
        ruta_destino = unir_ruta(ruta_destino,nombre_archivo) #Crea la ruta de destino del archivo
    else:
        print_directorys()
        showMessage("Por favor seleccione una carpeta",type="hand") #Displays a message to let the user know that the code needs his interaction
        choise = input ("Por favor ingrese la carpeta a la cual desea mover la carpeta:")
        while choise not in directorys.keys(): #Verifica que la entrada del usuario sea valida
            choise = input ("Por favor ingrese un nombre valido")
        ruta_destino = unir_ruta(directorys[choise],nombre_archivo) #Crea la ruta de destino del archivo
    move_file(ruta,ruta_destino) #Mueve el archivo a la ruta de destino

def unzip_all(path):
    '''looks for all the zipfiles in a directory and ask the user if he wants to unzip them one by None
    path: The absolute path of the folder that contains the zip files'''
    files = lista_archivos(path) #List of all the files in the path folder
    called = False #Aux variable that indicates if the user have been notified already about the need of interaction
    for file in files:
        filePath = unir_ruta(path,file)
        if file_type(filePath).lower() == "zip":
            if not called:
                showMessage("Do you like to unzip this file?",type="question") #Notifies the user about the need of interaction if has not been notified before
                called=True #States that the user have already been notified
            choise = input("Would you like to uncompress the file {}? [y/n]".format(get_filename(filePath))) #Ask the usr if he want to unzip the file
            while choise not in ["y","n"]: #Validates the selecction of a valid option
                choise = "Please select a valid option [y/n]"
            if choise == "y":
                unzip(filePath,remove=True) #unzips the file

def ordenar_archivos(ruta,indice=0):
    '''Funcion que organiza los archivos de la carpeta especificada en ruta
    El parametro indice sirve para determinar la impresion del progreso del ordenador de archivos'''
    unzip_all(ruta) #Unzips all the zip files if there is any
    archivos = lista_archivos(ruta) #Crea una lista con los nombres de los archivos que se encuentran en la carpeta
    archivos = ordenar_por_fecha(ruta,archivos) #Ordena los archivos de la carpeta por fecha y retorna una lista con las rutas absolutas de los archivos
    categorias = list(map(clasificar_Archivo,archivos)) #Categorias de los archivos que hay en la carpeta
    if categorias.count("folder") >= 1: #Verifica si existen sub carpetas en la carpeta actual
        choise = input("La carpeta: {} tiene {} carpetas adentro, desea...\n(0) clasificar los archivos de las subcarpetas\n(1) mover la carpeta completa\n".format(ruta,categorias.count("folder"))) #Le pregunta al usuario si desea mover la carpeta con subcarpetas o calsificar los archivos que hay dentro
        while choise not in ["0","1"]: #Verifica que el usuario ingrese una opcion valdia
            choise = input("Por favor ingrese una opcion valida")
        if choise == "1":
            mover_archivo(ruta) #Mueve la carpeta, le pregunta al usuario la carpeta de destino
            return #Acaba la ejecucion de la funcion una vez de mueve la carpeta
    if categorias.count("folder") == 0: #Verifies again if there is any subfolder
        images = categorias.count("imagen") #Number of images in the folder
        videos = categorias.count("video") #Number of videos in the folder
        books = categorias.count("libro") #Number of books in the folder
        others = categorias.count("otro") #Number of "other" files in the folder
        if images >= minFiles and videos <= minFiles and books <= minFiles and others <= minFiles: #Moves the full folder if it contains mostly images and if the number of images is superior to minFiles
            mover_archivo(ruta,ruta_destino=directorys["images"]) #Moves the complete folder to the images folder
            return #Finish the function
        if videos >= minFiles and images <= minFiles and books <= minFiles and others <= minFiles: #Moves the full folder if it contains mostly videos and if the number of videos is superior to minFiles
            mover_archivo(ruta,ruta_destino=directorys["videos"]) #Moves the complete folder to the videos folder
            return #Finish the function
        if books >= minFiles and images <= minFiles and videos <= minFiles and others <= minFiles: #Moves the full folder if it contains mostly books and if the number of books is superior to minFiles
            mover_archivo(ruta,ruta_destino=directorys["books"]) #Moves the complete folder to the books folder
            return #Finish the function
        if others >= minFiles and images <= minFiles and videos <= minFiles and books <= minFiles: #Moves the full folder if it contains mostly other files and if the number of these files is superior to minFiles
            mover_archivo(ruta,ruta_destino=directorys["others"]) #Moves the complete folder to the others folder
            return #Finish the function
    for i in range(len(archivos)): #Iterates over all the indexis of the files list in the folder
        file = archivos[i] #Retrieves the file from the files list
        filePath = unir_ruta(ruta,file) #Absolute path of the current file
        if isdir(filePath):
            ordenar_archivos(filePath,indice=indice+1) #If the current file is a dir, recoursively calls this function over that directory, augmenting the index by one
        elif clasificar_Archivo(filePath) == "imagen":
            mover_archivo(filePath,ruta_destino=directorys["images"]) #Moves the file to the images folder if it is an image
        elif clasificar_Archivo(filePath) == "video":
            mover_archivo(filePath,ruta_destino=directorys["videos"]) #Moves the file to the videos folder if it is a video
        elif clasificar_Archivo(filePath) == "libro":
            mover_archivo(filePath,ruta_destino=directorys["books"]) #Moves the file to the books folder if it is a book
        elif clasificar_Archivo(filePath) == "ejecutable":
            mover_archivo(filePath,ruta_destino=directorys["exe"]) #Moves the file to the exe folder if it is a windows executable
        else:
            mover_archivo(filePath,ruta_destino=directorys["others"]) #Moves the file to the others folder if its type does not correspond to any file type mentioned above
        print("{}Procesando... {}% [{}/{}]".format(">"*indice,i*100/len(archivos),i,len(archivos))) #Prints the progress of the program


minFiles = 3 #Minimum number of files to move a complete folder
directorys = readDirectorys() #Diccionario que contiene los directorios a los que se moveran los archivos
ruta=input("Ingrese la ruta absoluta de la carpera que desea analizar:\n")
while not isdir(ruta):
    ruta=input("No ha ingresado una ruta valida, por favor intente de nuevo:\n")
ordenar_archivos(ruta)
