import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import csv
import time
from datetime import datetime

# In update(), after reading timestamp:
timestamp = datetime.now()

# Append datetime object (not string)
times.append(timestamp)

LOG_FILENAME = 'temperature_log.csv'

# Simulated temperature read function (replace with your sensor code)
def get_temperature():
    # Replace this with actual sensor reading
    import random
    return 20 + random.uniform(-2, 2)

# Initialize CSV log file with header
with open(LOG_FILENAME, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Temperature_C'])

times = []
temps = []

def update(frame):
    temp = get_temperature()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append data to lists
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
