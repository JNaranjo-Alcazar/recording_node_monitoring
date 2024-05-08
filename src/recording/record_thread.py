import pyaudio
import wave
import threading
import time
from queue import Queue

# Configuración de grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 10  # Duración de cada segmento de grabación
DEVICE_INDEX = 1 # check this

# Bandera para indicar si se está grabando
recording = False

def record_segment(q):
    global recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=DEVICE_INDEX)

    frames = []
    print("Iniciando grabación...")

    while recording:
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

        if len(frames) >= int(RATE / CHUNK * DURATION):
            timestamp = time.time()
            formatted_datetime = time.strftime("/wavs/snd_%Y%m%d_%H%M%S", time.localtime(timestamp))
            q.put((formatted_datetime, frames))
            frames = []

    stream.stop_stream()
    stream.close()
    audio.terminate()

def save_segment(q):
    # segment_number = 1

    while True:
        filename, frames = q.get()
        # print(f"Guardando segmento {segment_number}...")
        # timestamp = int(time.time())
        # filename = f"/wavs/snd_{formatted_datetime}.wav"
        wf = wave.open(f'{filename}.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # print(f"Segmento {segment_number} guardado.")
        # segment_number += 1

def start_recording():
    global recording
    recording = True

    q = Queue()
    record_thread = threading.Thread(target=record_segment, args=(q,))
    save_thread = threading.Thread(target=save_segment, args=(q,))

    record_thread.start()
    save_thread.start()

def stop_recording():
    global recording
    recording = False

if __name__ == "__main__":
    
    start_time = time.time()
    
    start_recording()
    input("Presiona Enter para detener la grabación...")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    
    print("Tiempo transcurrido: {} h, {} m, {} s".format(hours, minutes, seconds))
    
    stop_recording()