import pyaudio

def list_audio_devices_by_host():
    p = pyaudio.PyAudio()

    device_info = p.get_host_api_info_by_index(0)
    num_devices = device_info.get('deviceCount')

    print("Input devices availables:")
    for i in range(num_devices):
        device_name = p.get_device_info_by_host_api_device_index(0, i).get('name')
        print(f"Index: {i}, Name: {device_name}")

    p.terminate()


def list_audio_devices():

    p = pyaudio.PyAudio()

    num_devices = p.get_device_count()

    print("Input devices availables:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            print(f"Index: {i}, Name: {device_info['name']}")

    p.terminate()

if __name__ == "__main__":
    list_audio_devices()