
📜 Python Code to Read Temperature from MAX31855
python
Copy
Edit
import spidev
import time

# SPI channel 0, device 0 (use 1 if it's on CE1)
SPI_BUS = 0
SPI_DEVICE = 0

def read_max31855():
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEVICE)
    spi.max_speed_hz = 5000000
    spi.mode = 0b00

    # Read 4 bytes from MAX31855
    raw = spi.readbytes(4)
    spi.close()

    # Convert to integer
    value = int.from_bytes(raw, 'big')

    # Check for error bit (D16)
    if value & 0x00010000:
        return None  # Fault detected

    # Extract temperature (bits 31-18)
    temp_data = (value >> 18) & 0x3FFF
    if temp_data & 0x2000:  # Negative value
        temp_data -= 0x4000

    temperature = temp_data * 0.25
    return temperature

# Read loop
try:
    while True:
        temp = read_max31855()
        if temp is not None:
            print(f"Temperature: {temp:.2f} °C")
        else:
            print("Sensor error or disconnected")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped.")