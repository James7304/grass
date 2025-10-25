from encode import text_to_bits, binary_to_frequency, frequency_to_sound
from decode import sound_to_frequency, frq_to_bin, binary_to_ascii
import util
import packet
import threading
import sys

# Shared event used to pause/resume listening
listening_enabled = threading.Event()
listening_enabled.set()  # listening starts ON

def restore_prompt():
    """Reprints the input prompt after receiver prints output."""
    sys.stdout.write("\nEnter text to transmit (or 'quit' to exit): ")
    sys.stdout.flush()


# -----------------------------------------
# Sending (Transmitting)
# -----------------------------------------
def send_loop():
    global listening_enabled
    print("Welcome to the Vibe Code!")

    while True:
        text = input("Enter text to transmit (or 'quit' to exit): ").strip()
        if text.lower() == "quit":
            print("Goodbye!")
            break

        # STOP listening while sending to avoid self-decoding
        listening_enabled.clear()

        bits = text_to_bits(text)
        send_packet = packet.create_packet(bits)

        # Build transmission frequency sequence
        frequencies = [util.START_FREQ]
        next_sequent = 0
        for i in range(0, len(send_packet), 8):
            byte = str(next_sequent) + send_packet[i:i+8]
            next_sequent = 0 if next_sequent == 1 else 1
            freq = binary_to_frequency(byte)
            frequencies.append(freq)

        frequencies.append(util.END_FREQ)

        # Play the entire signal
        frequency_to_sound(frequencies)

        # TURN LISTENING BACK ON
        listening_enabled.set()


# -----------------------------------------
# Receiving (Listening / Decoding)
# -----------------------------------------
def receive_loop():
    global listening_enabled
    next_sequent = -1
    streamed_data = ""

    for freq in sound_to_frequency():  # Should be a microphone generator

        # Skip all decoding while transmitting
        if not listening_enabled.is_set():
            continue

        rounded_freq = round(freq / util.INTERVAL) * util.INTERVAL

        # Detect message start
        if rounded_freq == util.START_FREQ and next_sequent == -1:
            print("\n\n----- New Message -----")
            print("Receiving: ", end='', flush=True)
            next_sequent = 0
            continue

        # Detect message end
        elif rounded_freq == util.END_FREQ and next_sequent != -1:
            # Check packet
            try:
                extracted_bits = packet.extract_packet(streamed_data)
                message = binary_to_ascii(extracted_bits)
                print("\nReceived Message: {}".format(message))
                frequency_to_sound([util.ACK_FREQ], duration=util.DURATION * 8)

                print("----- End Message -----")
                restore_prompt()

            except ValueError as e:
                print("\nError: {}".format(e) + ". Waiting for retransmission...")

            next_sequent = -1
            streamed_data = ""

            continue

        # Decode characters
        if next_sequent != -1 and rounded_freq >= util.BASE * 0.99:
            expected_seq = (int((rounded_freq - util.BASE) / util.INTERVAL) >> 8) & 1
            if next_sequent == expected_seq:
                binary = frq_to_bin(rounded_freq)
                streamed_data += binary

                ascii_char = binary_to_ascii(binary)
                if len(streamed_data) > 16:
                    print(ascii_char, end='', flush=True)
                next_sequent = 0 if next_sequent == 1 else 1


# -----------------------------------------
# Start System
# -----------------------------------------
if __name__ == "__main__":
    listener_thread = threading.Thread(target=receive_loop, daemon=True)
    listener_thread.start()

    send_loop()
