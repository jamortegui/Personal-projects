import urllib.request, urllib.parse, urllib.error
import time
import playsound as ps
import threading
import win32api
import subprocess

def connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host,timeout=2)
        return True
    except:
        return False

def playAllert():
    while not connected():
        ps.playsound("alarm.mp3")

def showMessage():
    if not connected():
        win32api.MessageBox(0, 'Not connected!', 'ERROR', 0x00001010)


horasTotales=float(input("Cuanto tiempo (en horas) desea correr el programa\n"))
rate = 1
suspend = input("¿Desea suspender el equipo al finalizar?[y/n]")
while suspend not in ["y","n"]:
    suspend = input("Por favor ingrese una opcion valida: ")
alert = threading.Thread(target=playAllert)
message = threading.Thread(target=showMessage)
count2= 10
start=time.time()
current=time.time()

while (current-start) <= horasTotales*60*60:
    if connected():
        if count2 >= 10:
            print("Connected! (remaining time: {:.2f} h)".format((horasTotales*60*60-(current-start))/(60*60)))
            count2 = 0
        else:
            count2 += 1
    else:
        alert.start()
        print("Not connected!")
        message.start()
        message = threading.Thread(target=showMessage)
        alert = threading.Thread(target=playAllert)
        count2=10
    time.sleep(rate)
    current=time.time()
if suspend == "y":
    subprocess.run("shutdown.exe /h")
