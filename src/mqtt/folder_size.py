import os
import sys
import datetime

 

FOLDERPATH = os.environ.get("FOLDERPATH")
MAX_GB = int(os.environ.get("MAX_GB"))
LOGSPATH = os.environ.get("LOGSPATH")

now = datetime.datetime.now()
output = now.strftime("%Y-%m-%d_%H:%M:%S")
 

folder_size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(FOLDERPATH) for filename in filenames)
size_gb = folder_size / (1024 * 1024 * 1024)  # Convertir a gigabytes
 
file = open(os.path.join(LOGSPATH, f"folder_info.log"), "a") 

file.write("----------------------------------\n")
file.write(f"Time: {output}\n")
file.write(f"Folder: {FOLDERPATH}\n")
file.write(f"MAX_GB: {MAX_GB}\n")
file.write(f"Actual Gb: {size_gb}\n")
file.write(f"Logic operation: {size_gb<MAX_GB}\n")

if size_gb < MAX_GB:
    # Realizar acciones si el tamaño de la carpeta es menor al límite
    
    file.write(f"next\n")
    file.close()    
    next  # Retornar código de salida 0 (éxito)
else:
    
    file.write(f"sys exit 1\n")
    file.close()
    sys.exit(1)  # Retornar código de salida distinto de 0 (error)
    
    
