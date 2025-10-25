import pyaudio
import numpy as np
import util


def text_to_bits(text):
    """Convert text into a string of ASCII bits."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_frequency(binary_str):
    """
    Convert binary data to a frequency.
    
    :param binary_data: Binary data (bytes)
    :return: Frequency in Hz
    """
    
    # Check that binary_data is exactly one byte
    if len(binary_str) != 9:
        raise ValueError("binary_data must be exactly one byte" + str(len(binary_str)))
    
    number_of_ones = binary_str.count('1')
    is_even = (number_of_ones % 2 == 0)

    # data_to_send = binary_str + ('0' if is_even else '1')
    data_to_send = binary_str
    frequency = util.BASE + int(data_to_send, 2) * util.INTERVAL

    return frequency

def frequency_to_sound(frequencies, duration=1.9, volume=0.5, sample_rate=44100):
    """
    Play a list of frequencies as a continuous stream with no gaps.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    waveforms = []

    for freq in frequencies:
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        waveform = np.sin(2 * np.pi * freq * t)
        waveform = (waveform * volume * 32767).astype(np.int16)
        waveforms.append(waveform)
        
        silence = np.zeros(int(sample_rate * 0.1), dtype=np.int16)
        waveforms.append(silence)

    # Concatenate all waveforms into one continuous stream
    full_waveform = np.concatenate(waveforms)
    # util.wait_until_next_interval()
    stream.write(full_waveform.tobytes())

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    # Example usage: play a BASE Hz tone for 2 seconds
    freq = binary_to_frequency('10101010')
    frequency_to_sound(freq, duration=2)
