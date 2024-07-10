
from record import start_recording, fetch_decibel
from write_data_to_csv import write_data_to_csv
import pyaudio
import time
import os
from dotenv import load_dotenv
load_dotenv()

duration = int(os.getenv("DURATION", 1))

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


if __name__ == "__main__":
    audio = pyaudio.PyAudio()
    device_index = get_device_index()

    stream = start_recording(audio, device_index)
    print("Recording...")

    try:
        start_time = time.time()
        if duration == 0:
            while True:
                fetch_decibel(stream, write_data_to_csv)
        else:
            while time.time() - start_time < duration:
                fetch_decibel(stream, write_data_to_csv)
    except KeyboardInterrupt:
        print("\nRecording interrupted.")
    except Exception as e:
        print(f"Error: {e}", flush=True)
    finally:
        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        audio.terminate()