import numpy as np
import pyaudio
import datetime
import time
import pytz
import os
from dotenv import load_dotenv
load_dotenv()

log_dir = "./logs"

# Constants from the TES-1350A manual
V_fs = 0.65  # Full scale voltage in Vrms
db_fs = 100  # Corresponding dB level at full scale in low range

# Calculate the reference voltage for 94 dB SPL
V_94 = V_fs * 10 ** ((94 - db_fs) / 20)

# Set the timezone to Taipei
tz = pytz.timezone('Asia/Taipei')

# Function to convert voltage to dB SPL
def voltage_to_db_spl(v_rms, v_ref):
    return 20 * np.log10(v_rms / v_ref) + 94 - 3

# Function to process audio data
def process_audio_data(indata, frames, time, status):
    indata = np.frombuffer(indata, dtype=np.int16)  # Convert to 16-bit integer
    max_int_value = 2**15  # 32768 for 16-bit PCM

    # Scale the integer data to voltage
    voltage_data = indata / max_int_value * V_fs

    squared_data = np.square(voltage_data)
    mean_squared_data = np.mean(squared_data)
    rms_voltage = np.sqrt(mean_squared_data)
   
    # Convert the RMS voltage to decibels (A-weighted)
    db_spl = voltage_to_db_spl(rms_voltage, V_94)
    log_entry = f"{datetime.datetime.now(tz)} - {db_spl:.2f} dB(A)\n"
    print(log_entry, end='')

    current_date_str = datetime.datetime.now(tz).strftime("%Y-%m-%d")
    log_filename = os.path.join(log_dir, f"decibel_log_{current_date_str}.txt")

    with open(log_filename, "a") as log_file:
        log_file.write(log_entry)


device_index = int(os.getenv("DEVICE_INDEX", 1))
duration = int(os.getenv("DURATION", 5))

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Increase CHUNK size

audio = pyaudio.PyAudio()

try:
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)
    print("Recording...")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            indata = stream.read(CHUNK, exception_on_overflow=False)
            process_audio_data(indata, CHUNK, None, None)
        except OSError as e:
            print(f"Error: {e}", flush=True)
except Exception as e:
    print(f"Failed to open stream: {e}", flush=True)
finally:
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()