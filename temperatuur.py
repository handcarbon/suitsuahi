import board
import digitalio
import adafruit_max31855
import time

# SPI bus (shared)
spi = board.SPI()

# CS pins for each MAX31855
cs1 = digitalio.DigitalInOut(board.D8)  # GPIO8
cs2 = digitalio.DigitalInOut(board.D7)  # GPIO7

# Create sensor objects
sensor1 = adafruit_max31855.MAX31855(spi, cs1)
sensor2 = adafruit_max31855.MAX31855(spi, cs2)

# Read loop
while True:
    print("Sensor 1: {:.2f} °C".format(sensor1.temperature))
    print("Sensor 2: {:.2f} °C".format(sensor2.temperature))
    print("-" * 30)
    time.sleep(1)