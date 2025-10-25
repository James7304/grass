from encode import text_to_bits, frequency_to_sound, binary_to_frequency

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
            for i in range(0, len(bits), 8):
                print(f"ASCII bits: {bits[i:i+8]}")
                freq = binary_to_frequency(bits[i:i+8])
                frequency_to_sound(freq)


if __name__ == "__main__":
    main()
