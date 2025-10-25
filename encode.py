import pyaudio
import numpy as np
import util


def text_to_bits(text):
    """Convert text into a string of ASCII bits."""
    return ''.join(format(ord(char), '08b') for char in text)


def frequency_to_sound(frequency, duration=0.9, volume=0.5, sample_rate=44100):
    """
    Play a sine wave of a given frequency.
    
    :param frequency: Frequency of the sound in Hz
    :param duration: Duration of the sound in seconds
    :param volume: Volume of the sound (0.0 to 1.0)
    :param sample_rate: Sampling rate in Hz
    """
    p = pyaudio.PyAudio()
    
    # Generate the samples for the sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    waveform = np.sin(2 * np.pi * frequency * t)
    
    # Normalize to 16-bit PCM and apply volume
    waveform = (waveform * volume * 32767).astype(np.int16)
    
    # Open a stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)
    
    # Play the sound
    util.wait_until_next_interval()
    stream.write(waveform.tobytes())
    
    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

def binary_to_frequency(binary_str):
    """
    Convert binary data to a frequency.
    
    :param binary_data: Binary data (bytes)
    :return: Frequency in Hz
    """
    
    # Check that binary_data is exactly one byte
    if len(binary_str) != 8:
        raise ValueError("binary_data must be exactly one byte")
    
    number_of_ones = binary_str.count('1')
    is_even = (number_of_ones % 2 == 0)

    data_to_send = binary_str + ('0' if is_even else '1')
    frequency = util.BASE + int(data_to_send, 2) * 25

    return frequency

if __name__ == "__main__":
    # Example usage: play a BASE Hz tone for 2 seconds
    freq = binary_to_frequency('10101010')
    frequency_to_sound(freq, duration=2)
