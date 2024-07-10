
from record import start_recording, fetch_decibel
from write_data_to_csv import write_data_to_csv
import pyaudio
import time
import os
from dotenv import load_dotenv
load_dotenv()


log_dir = "./logs"
duration = int(os.getenv("DURATION", 5))


def get_device_index():
    p = pyaudio.PyAudio()
    usb_device_index = None

    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)

        # Check if the device name contains 'USB'
        if 'USB' in device_info['name']:
            usb_device_index = i

    p.terminate()

    if usb_device_index is None:
        raise ValueError("No USB device found")
    return usb_device_index


try:
    audio = pyaudio.PyAudio()
    device_index = get_device_index()
    stream = start_recording(audio, device_index)
    print("Recording...")

    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            fetch_decibel(stream, write_data_to_csv)
        except Exception as e:
            print(f"Error: {e}", flush=True)
except Exception as e:
    print(f"Failed to open stream: {e}", flush=True)
finally:
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
