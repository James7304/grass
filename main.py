from encode import text_to_bits, binary_to_frequency, frequency_to_sound

def main():
    print("Welcome to the text-to-bits CLI tool!")
    while True:
        text = input("Enter text (or 'quit' to exit): ").strip()
        if text.lower() == "quit":
            print("Goodbye!")
            break
        else:
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
