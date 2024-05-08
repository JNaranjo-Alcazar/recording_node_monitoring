# This program uses two main functions: record_audio() and save_audio().
# The record_audio() function opens the pipeline with the microphone using pyaudio 
# and records audio for 10 seconds.
# The save_audio() function saves the audio data to a WAV file with a unique name based on the timestamp.

# In the main() function, an infinite loop is executed that records audio and saves files every 10 seconds.
# A thread is created to save the audio file in the background, 
# which allows the program to continue recording without interruption.


import pyaudio
import wave
import threading
import time
import datetime
import sys

# Redirigir stdout a la nada (devnull)
sys.stdout = open('/dev/null', 'w')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
DEVICE_INDEX = 1 # check this

def record_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)

    frames = []
    start_time = time.time()

    # More exact
    # while time.time() - start_time <= RECORD_SECONDS:
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    
    # print('Grabando')

    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
    # print('Finalizado')

    stream.stop_stream()
    # print('stop stream')
    stream.close()
    # print('stream close')
    p.terminate()
    # print('saliendo funcion')

    return frames

def save_audio(frames):
    # p = pyaudio.PyAudio() # Error

    timestamp = time.time()
    formatted_datetime = time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp))

    filename = f"/wavs/snd_{formatted_datetime}.wav"

    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    # wave_file.setsampwidth(p.get_sample_size(FORMAT))
    wave_file.setsampwidth(2) # Hardcoded
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

    # print(f"Audio saved as {filename}")

# Can lead to data loss
# def main():
#     while True:
#         frames = record_audio()
#         save_thread = threading.Thread(target=save_audio, args=(frames,))
#         save_thread.start()
#         # time.sleep(RECORD_SECONDS)

# Cannot lead to data loss but audios can be longer than 10 seconds
def main():
    frames = []
    save_thread = None
    
    start_time = time.time()

    while True:
        new_frames = record_audio()
        frames.extend(new_frames)

        if save_thread is None or not save_thread.is_alive():
            save_thread = threading.Thread(target=save_audio, args=(frames,))
            save_thread.start()
            frames = []

    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    
    print("Tiempo transcurrido: {} h, {} m, {} s".format(hours, minutes, seconds))


if __name__ == "__main__":
    main()
