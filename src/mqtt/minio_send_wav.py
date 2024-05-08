import os
import glob
import argparse

wavs_path = os.environ.get("FOLDERPATH")  # wavs
logs_path = os.environ.get("LOGSPATH")  # logs
bucket = os.environ.get("NODO")  # nodo
home = "/home/sorollia/"


def last_file_recorded(path):
    list_of_files = glob.glob(path + '*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy and upload WAV files to Minio')
    parser.add_argument('wav_file', nargs='?', help='Path to the WAV file to upload (optional)')
    args = parser.parse_args()

    if args.wav_file:
        # Si se proporciona un archivo WAV como argumento, lo copiamos
        os.system(f"sudo cp {args.wav_file} /home/")
        last_audio = last_file_recorded("/home/")
    else:
        # Si no se proporciona un archivo WAV, usamos el último archivo creado en la carpeta wavs
        last_audio_wavs = last_file_recorded(wavs_path)
        os.system(f"sudo cp {last_audio_wavs} /home/")
        last_audio = last_file_recorded("/home/")

    print(f"Archivo WAV a cargar: {last_audio}")

    # Copiamos el archivo a Minio
    os.system(f"/snap/bin/minio-mc-nsg cp {last_audio} sorollia/{bucket}")

    # Eliminamos el archivo localmente
    os.system(f"sudo rm {last_audio}")
