import pyaudio
import numpy as np

import util

def sound_to_frequency(duration=0.1, sample_rate=44100, chunk_size=1024):
    """
    Listen through the microphone and estimate the dominant frequency.

    :param duration: Duration to record in seconds
    :param sample_rate: Sampling rate in Hz
    :param chunk_size: Number of samples per read
    :return: Estimated frequency in Hz
    """
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    try:
        while True:
            # Wait until the time has reached a 1 second interval
            # util.wait_until_next_interval()

            frames = []
            num_chunks = int(sample_rate / chunk_size * duration)
            for _ in range(num_chunks):
                data = stream.read(chunk_size, exception_on_overflow=False)
                frames.append(np.frombuffer(data, dtype=np.int16))

            # Combine frames into a single array
            audio_data = np.hstack(frames)

            # Perform FFT
            fft_result = np.fft.fft(audio_data)
            fft_magnitude = np.abs(fft_result)
            frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)

            # Only consider positive frequencies
            positive_freqs = frequencies[:len(frequencies)//2]
            positive_magnitude = fft_magnitude[:len(frequencies)//2]

            # Find the peak frequency
            peak_index = np.argmax(positive_magnitude)
            dominant_freq = positive_freqs[peak_index]

            if (dominant_freq < util.START_FREQ * 0.99):
                continue

            yield dominant_freq
            
    except KeyboardInterrupt:
        print("\nStopped listening.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def binary_to_ascii(binary_str):
    """
    Convert a binary string to its ASCII representation.

    :param binary_str: String of binary digits (e.g., '01000001')
    :return: Corresponding ASCII character
    """
    if len(binary_str) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")

    ascii_chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        ascii_char = chr(int(byte, 2))
        ascii_chars.append(ascii_char)

    return ''.join(ascii_chars)

def parityOf(int_type):
    parity = 0
    while(int_type):
        parity = -parity
        int_type = int_type & (int_type - 1)
    return parity

def frq_to_bin(frq):

    frq -= util.BASE
    val = frq/util.INTERVAL

    w_out_parity = int(val) & 255
    ret = ""
    for i in range(8):
        ret = str((w_out_parity >> i) & 1) + ret

    return ret

next_sequent = -1
