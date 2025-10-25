import pyaudio
import numpy as np

def play_sound(frequency, duration=1.0, volume=0.5, sample_rate=44100):
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
    stream.write(waveform.tobytes())
    
    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

# Example usage: play a 440 Hz tone for 2 seconds
play_sound(440, duration=2)
