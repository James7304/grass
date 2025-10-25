import pyaudio
import numpy as np
import util


def text_to_bits(text):
    """Convert text into a string of ASCII bits."""
    return ''.join(format(ord(char), '08b') for char in text)



def frequencies_to_sound(frequencies, duration=1, volume=0.5, sample_rate=44100):
    """
    Play two sine waves simultaneously.
    
    :param frequencies: Tuple of two frequencies in Hz, e.g., (440, 660)
    :param duration: Duration of the sound in seconds
    :param volume: Volume of the sound (0.0 to 1.0)
    :param sample_rate: Sampling rate in Hz
    """
    if not isinstance(frequencies, (list, tuple)) or len(frequencies) != 2:
        raise ValueError("frequencies must be a tuple or list of two values")
    
    p = pyaudio.PyAudio()
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate two sine waves and sum them
    waveform = np.sin(2 * np.pi * frequencies[0] * t) + np.sin(2 * np.pi * frequencies[1] * t)
    
    # Normalize to avoid clipping
    waveform = waveform / np.max(np.abs(waveform))
    
    # Apply volume and convert to 16-bit PCM
    waveform = (waveform * volume * 32767).astype(np.int16)
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)
    
    stream.write(waveform.tobytes())
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def binary_to_frequency(sequent_bit, binary_str):
    """
    Convert binary data to a frequency.
    
    :param binary_data: Binary data (bytes)
    :return: Frequency in Hz
    """
    
    # Check that binary_data is exactly one byte
    if len(binary_str) != 16:
        raise ValueError("binary_data must be exactly two bytes")
    
    number_of_ones = binary_str.count('1')
    is_even = (number_of_ones % 2 == 0)

    data_to_send = sequent_bit + binary_str + ('0' if is_even else '1')

    first_nine = data_to_send[:9]
    first_frequency = util.BASE + int(first_nine, 2) * 25
    second_nine = data_to_send[9:]
    second_frequency = util.BASE + int(second_nine, 2) * 25

    return (first_frequency, second_frequency)

def frequency_to_sound(frequencies, duration=0.9, volume=0.5, sample_rate=44100):
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
        waveform = np.sin(2 * np.pi * freq[0] * t)
        waveform += np.sin(2 * np.pi * freq[1] * t)
        waveform = waveform / np.max(np.abs(waveform))
        waveform = (waveform * volume * 32767).astype(np.int16)
        waveforms.append(waveform)
        
        silence = np.zeros(int(sample_rate * 0.1), dtype=np.int16)
        waveforms.append(silence)

    # Concatenate all waveforms into one continuous stream
    full_waveform = np.concatenate(waveforms)
    util.wait_until_next_interval()
    stream.write(full_waveform.tobytes())

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    # Example usage: play a BASE Hz tone for 2 seconds
    freq = binary_to_frequency('10101010')
    frequency_to_sound(freq, duration=2)
