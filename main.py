from encode import text_to_bits, binary_to_frequency, frequency_to_sound
import util
import threading

# This function handles sending text input
def send_loop():
    print("Welcome to the Vibe Code!")
    while True:
        text = input("Enter text to transmit (or 'quit' to exit): ").strip()
        if text.lower() == "quit":
            print("Goodbye!")
            break
        else:
            bits = text_to_bits(text)

            # Split into bytes and convert each to frequency
            frequencies = [util.START_FREQ]
            next_sequent = 0
            for i in range(0, len(bits), 8):
                byte = str(next_sequent) + bits[i:i+8]
                next_sequent = 0 if next_sequent == 1 else 1
                freq = binary_to_frequency(byte)
                frequencies.append(freq)

            # Play all tones as a single continuous stream
            frequencies.append(util.END_FREQ)
            frequency_to_sound(frequencies)

# This function handles listening and decoding frequencies
def receive_loop():
    from decode import sound_to_frequency, frq_to_bin, binary_to_ascii  # assuming these exist
    next_sequent = -1

    for freq in sound_to_frequency():  # This should be a generator
        rounded_freq = round(freq / util.INTERVAL) * util.INTERVAL

        if rounded_freq == util.START_FREQ and next_sequent == -1:
            print("\n----- New Message -----")
            next_sequent = 0
        elif rounded_freq == util.END_FREQ and next_sequent != -1:
            print("\n----- End Message -----")
            next_sequent = -1
            continue  # keep listening for next messages

        if next_sequent != -1 and rounded_freq >= util.BASE * 0.99:
            expected_seq = (int((rounded_freq - util.BASE) / util.INTERVAL) >> 8) & 1
            if next_sequent == expected_seq:
                binary = frq_to_bin(rounded_freq)
                ascii_char = binary_to_ascii(binary)
                print(ascii_char, end='', flush=True)
                next_sequent = 0 if next_sequent == 1 else 1

# Run both loops in parallel
if __name__ == "__main__":
    listener_thread = threading.Thread(target=receive_loop, daemon=True)
    listener_thread.start()

    send_loop()  # main thread handles input
