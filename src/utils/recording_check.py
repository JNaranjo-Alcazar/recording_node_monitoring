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

# Ejecutar el comando 'pidof' para obtener el PID del proceso 'record_snd_exe'
pidof_command = 'pidof record_snd_exe'
result = os.popen(pidof_command).read().strip()

# Obtener el PID del resultado y guardarlo en una variable
pid = result

file = open(os.path.join(LOGSPATH, f"folder_info.log"), "a") 
file.write("----------------------------------\n")
file.write("PID del proceso 'record_snd_exe':"+ pid + "\n")

if not pid:
    # Realizar acciones si el tamaño de la carpeta es menor al límite
    
    file.write("record_snd_exe is not recording\n")
    file.close()    
    next  # Retornar código de salida 0 (éxito)
if pid:
    
    file.write("record_snd_exe is recording\n")
    file.close()
    sys.exit(1)  # Retornar código de salida distinto de 0 (error)
    
    
