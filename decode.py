import pyaudio
import numpy as np

import util

def sound_to_frequency(duration=1, sample_rate=44100, chunk_size=1024):
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

    print("Listening...")

    try:
        while True:
            util.wait_until_next_interval()

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

            # Find indices of the two largest peaks
            peak_indices = positive_magnitude.argsort()[-2:][::-1]  # top 2 peaks
            dominant_freqs = positive_freqs[peak_indices]

            # Optional: ignore very low frequencies (noise)
            dominant_freqs = [f for f in dominant_freqs if f > 20]

            yield tuple(dominant_freqs)
            
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

    w_out_parity = int(val) >> 1
    ret = ""
    for i in range(8):
        ret = str((w_out_parity >> i) & 1) + ret

    return ret

# Example usage
for freqs in sound_to_frequency(duration=1):
    freq_one = freqs[0]
    freq_two = freqs[1]

    rounded_freq_one = round(freq_one / util.INTERVAL) * util.INTERVAL
    rounded_freq_two = round(freq_two / util.INTERVAL) * util.INTERVAL

    binary_one = frq_to_bin(rounded_freq_one)
    binary_two = frq_to_bin(rounded_freq_two)

    ascii_char_one = binary_to_ascii(binary_one)
    ascii_char_two = binary_to_ascii(binary_two)
    print(ascii_char_one, end='', flush=True)
    print(ascii_char_two, end='', flush=True)
