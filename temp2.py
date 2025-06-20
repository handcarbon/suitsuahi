import spidev
import time

def read_max31855(spi):
    raw = spi.readbytes(4)
    if len(raw) != 4:
        return float('nan')

    value = (raw[0] << 24) | (raw[1] << 16) | (raw[2] << 8) | raw[3]

    # Check for error bit (D16)
    if value & 0x00010000:
        return float('nan')  # Error reading sensor

    # Extract temperature (14-bit signed)
    temp_raw = (value >> 18) & 0x3FFF
    if temp_raw & 0x2000:  # Negative value
        temp_raw -= 0x4000

    temp_c = temp_raw * 0.25
    return temp_c

# Create two SPI objects for CE0 and CE1
spi1 = spidev.SpiDev()
spi2 = spidev.SpiDev()

# Open SPI bus 0, devices 0 and 1
spi1.open(0, 0)  # CE0
spi2.open(0, 1)  # CE1

# Set SPI speed and mode
for spi in (spi1, spi2):
    spi.max_speed_hz = 5000000
    spi.mode = 0b00

# Read loop
try:
    while True:
        temp1 = read_max31855(spi1)
        temp2 = read_max31855(spi2)

        print(f"Sensor 1: {temp1:.2f} °C" if temp1 == temp1 else "Sensor 1: Error")
        print(f"Sensor 2: {temp2:.2f} °C" if temp2 == temp2 else "Sensor 2: Error")
        print("-" * 30)

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    spi1.close()
    spi2.close()
