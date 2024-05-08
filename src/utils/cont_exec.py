import os
import sys
import datetime

# This script checks if the record_snd_exe is working, if it is returns sys.exit(1) error and 
# if its not returns a next and ends
# So it will be loaded each hour from cronjob so if is not working it will be launched again

FOLDERPATH = os.environ.get("FOLDERPATH")
MAX_GB = int(os.environ.get("MAX_GB"))
LOGSPATH = os.environ.get("LOGSPATH")

now = datetime.datetime.now() 
output = now.strftime("%Y-%m-%d_%H:%M:%S")

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read().strip()
            return contenido
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe. Se creará con el valor 1.")
        escribir_archivo(nombre_archivo, '1')
        return '1'

def escribir_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(contenido)

def procesar_numero(archivo_nombre,numero):
    numero = int(numero)
    if numero < 3:
        escribir_archivo(archivo_nombre, str(numero + 1))
        sys.exit(1)
    elif numero >= 3:
        escribir_archivo(archivo_nombre, str(0))

if __name__ == "__main__":
    archivo_nombre = LOGSPATH + "/numeros.txt"
    numero = leer_archivo(archivo_nombre)

    if numero:
        procesar_numero(archivo_nombre,numero)
    
        
