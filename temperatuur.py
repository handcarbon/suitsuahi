import time
import board
import digitalio
import adafruit_max31855

# Set up SPI
spi = board.SPI()

# Set up chip select pins for each sensor
cs1 = digitalio.DigitalInOut(board.D8)  # GPIO8 (CE0)
cs1.direction = digitalio.Direction.OUTPUT

cs2 = digitalio.DigitalInOut(board.D7)  # GPIO7 (CE1)
cs2.direction = digitalio.Direction.OUTPUT

# Initialize MAX31855 sensors
sensor1 = adafruit_max31855.MAX31855(spi, cs1)
sensor2 = adafruit_max31855.MAX31855(spi, cs2)

# Read loop
try:
    while True:
        temp1 = sensor1.temperature
        temp2 = sensor2.temperature

        print(f"Sensor 1 Temperature: {temp1:.2f} °C")
        print(f"Sensor 2 Temperature: {temp2:.2f} °C")
        print("-" * 30)

        time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped.")