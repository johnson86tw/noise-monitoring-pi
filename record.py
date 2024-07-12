import numpy as np
import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048  # Increase CHUNK size


def start_recording(audio: pyaudio.PyAudio, device_index):
    return audio.open(format=FORMAT, channels=CHANNELS,
                      rate=RATE, input=True,
                      input_device_index=device_index,
                      frames_per_buffer=CHUNK)


# Constants from the TES-1350A manual
V_fs = 0.65  # Full scale voltage in Vrms
db_fs = 100  # Corresponding dB level at full scale in low range

# Calculate the reference voltage for 94 dB SPL
V_94 = V_fs * 10 ** ((94 - db_fs) / 20)


def fetch_decibel(stream: pyaudio.Stream, callback):
    indata = stream.read(CHUNK, exception_on_overflow=False)
    indata = np.frombuffer(indata, dtype=np.int16)  # Convert to 16-bit integer
    max_int_value = 2**15  # 32768 for 16-bit PCM

    # Scale the integer data to voltage
    voltage_data = indata / max_int_value * V_fs

    squared_data = np.square(voltage_data)
    mean_squared_data = np.mean(squared_data)
    rms_voltage = np.sqrt(mean_squared_data)

    # Convert the RMS voltage to decibels (A-weighted)
    db_spl = voltage_to_db_spl(rms_voltage, V_94)

    callback(f"{db_spl:.1f}")


def voltage_to_db_spl(v_rms, v_ref):
    return 20 * np.log10(v_rms / v_ref) + 94 - 3
