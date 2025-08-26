import cc1101
import time
from cc1101.options import ModulationFormat, PacketLengthMode
import datetime

# Define the sequence and pauses (in samples)

SEQUENCE = [
    ("ffffffffff", 4712),
    ("fffffffffc", 4712),
    ("AAAAAAAAAA", 23162),
    ("BBBBBBBBBB", 23162),
    ("CCCCCCCCCC", 23140)
]

# Symbol rate 
SYMBOL_RATE = 3300  # baud (samples per second)
SAMPLE_RATE = 1_000_000.0


with cc1101.CC1101() as radio:
    # Set frequency to 433.92 MHz 
    radio.set_base_frequency_hertz(433.92e6)

    # Set symbol rate to 3300 baud 
    radio.set_symbol_rate_baud(SYMBOL_RATE)

    # Set modulation format to ASK/OOK 
    radio._set_modulation_format(ModulationFormat.ASK_OOK)

    # Configure output power for OOK (0 for '0', non-zero for '1') 
    radio.set_output_power((0, 0xC6))

    # Set packet length mode to FIXED 
    radio.set_packet_length_mode(PacketLengthMode.FIXED)
    radio.enable_raw_mode()
    
    last_time = datetime.datetime.now()
 

    # Transmit the sequence with specified pauses
    for hex_string, pause_samples in SEQUENCE:
        data_bytes = bytes.fromhex(hex_string)
        # Ensure packet length matches the data
        radio.set_packet_length_bytes(len(data_bytes))
        
        try:
            # Transmit the data
            pause = datetime.datetime.now() - last_time
            print(f"Pause for {pause.total_seconds() * 1000:.2f} ms")
            last_time = datetime.datetime.now()
            radio.transmit(data_bytes)
            print(f"Transmission completed: {hex_string}")
            
            # Convert pause from samples to seconds 
            pause_seconds = pause_samples / SAMPLE_RATE
            time.sleep(pause_seconds)
        except:
            # Force IDLE state before transmission
            radio.set_idle()
            