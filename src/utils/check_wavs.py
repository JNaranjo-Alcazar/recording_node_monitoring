import os
import wave

def is_wav_file(filepath):
    _, ext = os.path.splitext(filepath)
    return ext.lower() == '.wav'

def can_load_wav(filepath):
    try:
        with wave.open(filepath, 'rb') as wav_file:
            # Intenta cargar los encabezados del archivo WAV
            wav_file.readframes(1)
        return True
    except wave.Error:
        return False

def delete_unloadable_wavs(folder_path):
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if is_wav_file(filepath) and not can_load_wav(filepath):
            print(f"Deleting {filepath}")
            os.remove(filepath)

# Ruta de la carpeta que contiene los archivos WAV
folder_path = '/home/jgrau/orellia2/avis'

delete_unloadable_wavs(folder_path)
