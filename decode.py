import pyaudio
import numpy as np

def sound_to_frequency(duration=1.0, sample_rate=44100, chunk_size=1024):
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

    frames = []
    num_chunks = int(sample_rate / chunk_size * duration)
    for _ in range(num_chunks):
        data = stream.read(chunk_size, exception_on_overflow=False)
        frames.append(np.frombuffer(data, dtype=np.int16))

    # Stop stream
    stream.stop_stream()
    stream.close()
    p.terminate()

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

    return dominant_freq

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

# Example usage
# freq = sound_to_frequency(duration=2)
# print(f"Detected frequency: {freq:.2f} Hz")

ascii_char = binary_to_ascii('01001001')
print(f"ASCII character: {ascii_char}")
