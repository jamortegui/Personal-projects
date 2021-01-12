from FilesManagement import *
import moviepy.editor as ed
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def isVideo(file):
    #verifies if the file is a video file
    return isfile(file) and clasificar_Archivo(file) == "video"

def extractImages(file,dir):
    ''' Extracts the images from the video and stores them in the cache directory
    file: Route of the video from wich we want to extract the images
    dir: route of the cache directory
    '''
    images = 8 #Number of images to extract
    fileName=get_filename(file)
    count = 0 #Auxiliar varible to count the images existing in the cache folder
    for i in range(images): # For cicle that checks if the images already exist
        imgpath = unir_ruta(dir,"{}({}).jpg".format(fileName,i))
        if isfile(imgpath):
            count+=1
    if count == images:
        return #If the images already exist, the function ends
    video = ed.VideoFileClip(file) #Open the video as a videoFileClip object
    l = video.duration #lenght of the video in seconds
    times=np.arange(1,images+1)*l/(images+1) #list of time stamps from wich we want to extract the imagenes
    for i in range(len(times)):
        imgpath = unir_ruta(dir,"{}({}).jpg".format(fileName,i)) #Crea la ruta donde se va a guardar la imagen
        video.save_frame(imgpath,t=times[i]) #Saves the video screenshot
    video.close()

def clearCache(dir):
    '''Removes all the files from the cache directory
    dir: route of the cache directory'''
    files = lista_archivos(dir)
    for file in files: #for cicle that deletes all files in teh cache folder
        delete_file(unir_ruta(dir,file))

def displayImages(file,dir):
    '''Displays a plot showing the screenshots of the video
    file: Route of the video from wich we want to display the screenshots
    dir: route of the cache directory
    '''
    if plt.gcf() is None:
        plt.figure() #Creates a new figure if there is not an active figure
        #plt.ion()
        #plt.show()
    names=[]
    fileName=get_filename(file)
    for name in lista_archivos(dir):
        if name.startswith(fileName):
            names.append(name)
    x = 2 #number of columns of the subplot
    if len(names)%2 == 0:
        y=len(names)/2 #number of rows the subplot
    else:
        y=len(names)/2+1
    plt.clf() #Clears the figure before plot again
    for i in range(len(names)): #For cicle that displays each image in each subplot
        plt.subplot(y,x,i+1)
        plt.box(False) #Removes the frame
        plt.axis("off") #Removes the ticks and the axis
        img = mpimg.imread(unir_ruta(dir,names[i])) #open the image to be displayed
        plt.imshow(img) #displays the image
    plt.subplots_adjust(wspace=0,hspace=0) #Removes spaces between subplots (images)
    plt.draw() #updates the figure
    plt.pause(0.5) #Gives enough time for the GUI to update

def getCategoryList(file):
    '''Returns a list with the current categories
    file: route of the categories file
    '''
    categories = []
    with open(file) as categories_f:
        for category in categories_f.readlines():
            categories.append(category.replace("\n",""))
    return categories

def addCategory(category,categories,file):
    '''Adds a new category to the categories file
    category: str, the name of the new category to be added
    categories: list of categories
    file: route of the categories file
    '''
    if category == "cache":
        return #Stops the function if the category name is cache, this name is reserved
    categories.append(category)
    with open(file,"a") as categories_f:
        categories_f.write("{}\n".format(category))

def removeCategory(category,categories,file):
    '''Removes a category from the categories file
    category: str, the name of the new category to be removed
    categories: list of categories
    file: route of the categories file
    '''
    categories.remove(category) #removes the category from the list
    with open(file,"w") as categories_f:
        for category in categories:
            categories_f.write("{}\n".format(category)) #Rewrites the file

def printCategories(categories):
    '''Prints the current categories to the screen
    categories: list of categories
    '''
    toPrint = "-1\t|Remove category\n0\t|Add new category\n"
    i = 1
    for category in categories:
        toPrint += "{}\t|{}\n".format(i,category)
        i += 1
    print(toPrint)

path = input("Please insert the folder that contains the videos:") #The main path of the videos
while not isdir(path): #Verifies that the inserted path is a valid dir
    path = input("Please insert a valid directory:")
cache = unir_ruta(path,"cache")
if not isdir(cache):
    create_dir(cache) #creates the cache dir if this does not exist
categoriesFile = unir_ruta(path,"categories.txt")
with open(categoriesFile,"a") as file: #Creates the categories file if is not yet created
    pass
categories = getCategoryList(categoriesFile)
for category in categories: #Creates a dir for each category if it does not exist yet
    if not isdir(unir_ruta(path,category)):
        create_dir(unir_ruta(path,category))
files = lista_archivos(path) #list of all the files in te folder
for i in range(len(files)): #For cicle that extracts all the required images from the videos
    file = files[i]
    filePath = unir_ruta(path,file) #Gets the absolute path of the file
    if isVideo(filePath):
        print("Procesing images... please wait [{}/{}]({:.1f}%)".format(i+1,len(files),((i+1)*100)/(len(files))))
        extractImages(filePath,cache)
for file in files:
    filePath = unir_ruta(path,file) #Gets the absolute path of the file
    #print(cache)
    #print(filePath)
    #input("...")
    if isVideo(filePath):
        clasified = False #Boolean that indicates if the video have been properly clasified
        displayImages(filePath,cache)
        while not clasified:
            printCategories(categories)
            print("File: "+file)
            action = int(input("Please select the category for this video:"))
            while action < -1 or action > len(categories): #Verifies that action is in the correct range
                action = int(input("Please select a valid category"))
            if action == -1: #Removes a category
                category = input("Please insert the category that youn want to remove: ")
                if category in categories: #Verifies that the input is an existing category
                    removeCategory(category,categories,categoriesFile)
                    if len(lista_archivos(unir_ruta(path,category))) == 0:
                        delete_file(unir_ruta(path,category)) #Deletes the category folder if it is empty
                    print("{} has been removed".format(category))
            elif action == 0: #Adds a new category
                category = input("Please insert the new category that youn want to add: ")
                if not(category in categories): #Verifies that the input is not an existing category
                    addCategory(category,categories,categoriesFile)
                    create_dir(unir_ruta(path,category)) #Creates the dir for the new category
                    print("{} has been added".format(category))
            else:
                fileDestination = unir_ruta(path,categories[action-1])
                fileDestination = unir_ruta(fileDestination,file) #Creates the absolute path for the destination of the file
                move_file(filePath,fileDestination) #Moves the file
                print("{} has been moved to {}".format(file,categories[action-1]))
                clasified = True
clearCache(cache)
