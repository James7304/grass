import speech_recognition as sr
from encode import text_to_bits, binary_to_frequency, frequency_to_sound

def recognize_speech():
    """Capture audio from the microphone and return recognized text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Speak now...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn’t understand you.")
    except sr.RequestError:
        print("Speech recognition service unavailable.")
    return None


def main():
    print("Welcome to the CLI tool!")
    print("Type 'voice' to use speech input or 'quit' to exit.")

    while True:
        text = input("Enter text (or 'voice'/'quit'): ").strip()

        if text.lower() == "quit":
            print("Goodbye!")
            break

        elif text.lower() == "voice":
            spoken_text = recognize_speech()
            if not spoken_text:
                continue
            text = spoken_text
            print(text)
        # Normal text handling
        bits = text_to_bits(text)
        print(bits)

        # Split into bytes and convert each to frequency
        frequencies = []
        next_sequent = 0
        for i in range(0, len(bits), 8):
            byte = str(next_sequent) + bits[i:i+8]
            next_sequent = 0 if next_sequent == 1 else 1
            print(f"ASCII bits: {byte}")
            freq = binary_to_frequency(byte)
            frequencies.append(freq)

        # Play all tones as a single continuous stream
        frequency_to_sound(frequencies)


if __name__ == "__main__":
    main()
