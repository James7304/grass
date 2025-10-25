import pyaudio
import numpy as np
from scipy.signal import find_peaks
import time
from collections import defaultdict

def sound_to_frequency(chunk_size=1024, sample_rate=44100, magnitude_threshold=1000, min_duration=1.0):
    """
    Continuously listen and yield the strongest dominant frequency (highest amplitude) 
    that lasts at least min_duration seconds and is of the form 440 + n*25 Hz.

    :param chunk_size: Samples per read
    :param sample_rate: Sampling rate
    :param magnitude_threshold: Minimum FFT magnitude to consider a frequency
    :param min_duration: Minimum duration in seconds a frequency must persist to be reported
    :yield: Strongest stable frequency in Hz
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Listening for strongest stable peak... (Press Ctrl+C to stop)")

    freq_start_time = None
    last_freq = None

    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # FFT
            fft_result = np.fft.fft(audio_data)
            fft_magnitude = np.abs(fft_result)
            frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)

            # Positive frequencies only
            pos_freqs = frequencies[:len(frequencies)//2]
            pos_magnitude = fft_magnitude[:len(frequencies)//2]

            # Find index of highest amplitude above threshold
            idx = np.argmax(pos_magnitude)
            if pos_magnitude[idx] < magnitude_threshold:
                last_freq = None
                freq_start_time = None
                continue

            freq = pos_freqs[idx]
            # Snap to 440 + n*25
            n = round((freq - 440) / 25)
            valid_freq = 440 + n * 25
            print(valid_freq)
            if abs(freq - valid_freq) > 12.5:  # tolerance
                last_freq = None
                freq_start_time = None
                continue

            current_time = time.time()
            if last_freq == valid_freq:
                # Check duration
                if current_time - freq_start_time >= min_duration:
                    yield valid_freq
            else:
                last_freq = valid_freq
                freq_start_time = current_time

    except KeyboardInterrupt:
        print("\nStopped listening.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

for freq in sound_to_frequency():
    print("Detected frequency:", round(freq, 1))
