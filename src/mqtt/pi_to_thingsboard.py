import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import subprocess
import soundfile as sf
import numpy as np
import glob
#import emoji

from pijuice import PiJuice
from pijuice import __version__ as library_version
from json import dumps 
from datetime import datetime


 #environment variables to configure at raspberrypi

THINGSBOARD_HOST = os.environ.get("THINGSBOARD_HOST")
PORT = os.environ.get("PORT")
ACCESS_TOKEN = os.environ.get("TOKEN")
FOLDERPATH = os.environ.get("FOLDERPATH")

LOGSPATH = os.environ.get("LOGSPATH") #logs
PWD = os.environ.get("PWD") #path
BUCKET = os.environ.get("NODO") # nodo

INTERVAL=300

pijuice = PiJuice(1, 0x14)  # Instantiate PiJuice interface object

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.

next_reading = time.time() 

def last_file_recorded(path, ext_file):
    
    message = ""
    
    if path == None:
        message = "Folder is None"
        return None, False, message
    
    else:  
        can_access_folder = os.access(path, os.R_OK)
        
    
    if not can_access_folder:
        message = "Folder is not accessible"
        return None, False, message
    
    else:
        list_of_files = glob.glob(f"{path}{ext_file}") # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        message = "Folder is accessible"
        return latest_file, True, message


def get_pijuice_data(path):
    
    status = pijuice.status.GetStatus()["data"]
    
    FolderSize = get_folderSize(path)
        
    fecha = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    latest_file, folder_access, message = last_file_recorded(FOLDERPATH,"*.wav")
    
    if folder_access == True:
        last_file = os.path.basename(latest_file)
    else:
        last_file = None
    
             
    pijuice_status = {
    "date":fecha,
    "batteryCharge": pijuice.status.GetChargeLevel()["data"],
    "batteryVoltage": pijuice.status.GetBatteryVoltage()["data"] / 1000,
    "batteryCurrent": pijuice.status.GetBatteryCurrent()["data"] / 1000,
    "batteryTemperature": pijuice.status.GetBatteryTemperature()["data"],
    "batteryStatus": status["battery"],
    "powerInput": status["powerInput"],
    "powerInput5vIo": status["powerInput5vIo"],
    "ioVoltage": pijuice.status.GetIoVoltage()["data"] / 1000,
    "ioCurrent": pijuice.status.GetIoCurrent()["data"] / 1000,
    "FolderSize": FolderSize / (1024 * 1024 * 1024),
    "LastFile": last_file,
    "Message": message,
    }
    
    return pijuice_status

def print_string_with_newlines(s):
            prev_char = ""
            cadena = ""
            for char in s:
                if prev_char == '"' and char == 'C':
                    if cadena[:16]=="CompletedProcess":
                        cadena = ""
                if prev_char == "'" and char == 'E':
                    if cadena[-8:]=="stderr='":
                        cadena = ""
                if prev_char == "\\" and char == "n":
                    if cadena[-6:]=="Client":
                        cadena = "Client"
                    else:
                        print(cadena)
                        cadena = ""
                else:
                    cadena = cadena + char
                prev_char = char        
      

def get_folderSize(path):
    
    size = 0
    
    for ele in os.scandir(path): 
        size+=os.path.getsize(ele)
    
    return size

def publish_data(host, port, token, data):
    
    try:
        data_str = "'" +json.dumps(data)+ "'"
        
        # process = subprocess.run(['mosquitto_pub', '-d', '-q', '1', '-h', host, '-p', port, '-t', 'v1/devices/me/telemetry', '-u', token, '-m', data_str], capture_output=True, text=True) 
        # print_string_with_newlines(str(process))
        
        last_log, access, message = last_file_recorded(LOGSPATH, "*.txt")
        command = f'mosquitto_pub -d -q 1 -h {host} -p {port} -t v1/devices/me/telemetry -u {token} -m {data_str}'
        
        os.system(f"{command} > {last_log} 2>&1")
        # os.system(f'mosquitto_pub -d -q 1 -h {host} -p {port} -t v1/devices/me/telemetry -u {token} -m {data_str}')

        
        print(f"-------DATA REGISTERED--------\n")
        print(f"date = {data['date']}\n")
        print(f"batteryCharge = {data['batteryCharge']}\n")
        print(f"batteryVoltage = {data['batteryVoltage']}\n")
        print(f"batteryCurrent = {data['batteryCurrent']}\n")
        print(f"batteryTemperature = {data['batteryTemperature']}\n")
        print(f"batteryStatus = {data['batteryStatus']}\n")
        print(f"powerInput = {data['powerInput']}\n")
        print(f"powerInput5vIo = {data['powerInput5vIo']}\n")
        print(f"ioVoltage = {data['ioVoltage']}\n")
        print(f"ioCurrent = {data['ioCurrent']}\n")
        print(f"FolderSize = {data['FolderSize']}\n")
        print(f"LastFile = {data['LastFile']}\n")
        print(f"-----------------------------\n")

        
    
    except KeyError:
        #print("Cannot connect due to:", KeyError)    
        print(f"Cannot connect due to:", KeyError, "\n")   
    except LookupError:
        print(f"Cannot connect due to:", LookupError, "\n")   
        
    
if __name__ == '__main__':
   
    
    print(f"Interval time set to {INTERVAL} seconds\n")
    
    print(f"Starting VPN \n")
    
    try:
        # vpn file to configure vpn if wanted
        os.system('sudo wg-quick up /vpn-rpi.conf')
        print(f"VPN connection was successful\n")
    
    except KeyError:
        print(f"Cannot connect via VPN\n")
        
    
    try:
        while True:
            sensor_data = get_pijuice_data(FOLDERPATH)
            # Sending data to TB via mosquitto_pub on subprocess.run
            publish_data(THINGSBOARD_HOST, PORT, ACCESS_TOKEN, sensor_data)
            next_reading += INTERVAL
            sleep_time = next_reading-time.time()
        
            if sleep_time > 0:
                time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        #print('Exiting due to KeyboardInterrupt')
        print('Exiting due to KeyboardInterrupt\n')
        
    
