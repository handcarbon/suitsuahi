import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import csv
import spidev
import time

from datetime import datetime


LOG_FILENAME = 'temperature_log.csv'

# Simulated temperature read function (replace with your sensor code)
def get_temperature(spi):
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

spi1 = spidev.SpiDev()
spi1.open(0, 0)  #
spi1.max_speed_hz = 5000000
spi1.mode = 0b00


# Initialize CSV log file with header
with open(LOG_FILENAME, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Temperature_C'])

times = []
temps = []

def update(frame):
    temp = get_temperature(spi1)

    timestamp = datetime.now()
    times.append(timestamp)
    temps.append(temp)

    # Log data to CSV every 15 seconds
    if len(times) == 1 or (time.time() - update.last_log_time) >= 15:
        with open(LOG_FILENAME, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, f"{temp:.2f}"])
        update.last_log_time = time.time()

    # Keep only last 40 data points for display
    if len(times) > 40:
        times.pop(0)
        temps.pop(0)

    # Clear and plot
    plt.cla()
    plt.plot(times, temps, marker='o')
    plt.title('Temperature Over Time')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Time (HH:MM)')
    plt.grid(True)

    # Format x-axis to show HH:MM
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # Optional: auto-format date labels to avoid overlap
    plt.gcf().autofmt_xdate()

    plt.tight_layout()

# Initialize last_log_time attribute
update.last_log_time = 0

# Set up matplotlib animation
fig = plt.figure()
ani = animation.FuncAnimation(fig, update, interval=15000)  # update every 15 sec

plt.show()
