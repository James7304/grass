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
            sequent_bit = '0'  # Starting sequent bit
            for i in range(0, len(bits), 16):
                byte = bits[i:i+16]
                print(f"ASCII bits: {byte}")
                freq = binary_to_frequency(sequent_bit, byte)
                frequencies.append(freq)
                sequent_bit = '1' if sequent_bit == '0' else '0'  # Toggle sequent bit

            # Play all tones as a single continuous stream
            frequency_to_sound(frequencies)

if __name__ == "__main__":
    main()
