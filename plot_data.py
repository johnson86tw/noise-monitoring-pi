import os
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import pytz

# Set the timezone to Taipei
tz = pytz.timezone('Asia/Taipei')

# Directory containing log files
log_dir = "./logs"

# List to store all data
all_data = []

# Loop through all log files in the directory
for log_filename in os.listdir(log_dir):
    if log_filename.startswith("decibel_log_") and log_filename.endswith(".txt"):
        log_filepath = os.path.join(log_dir, log_filename)
        with open(log_filepath, "r") as file:
            for line in file:
                timestamp, db_spl = line.split(" - ")
                timestamp = pd.to_datetime(timestamp)
                db_spl = float(db_spl.replace(" dB(A)\n", ""))
                all_data.append([timestamp, db_spl])

# Create a DataFrame
df = pd.DataFrame(all_data, columns=["Timestamp", "dB(A)"])

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df["Timestamp"], df["dB(A)"], label="dB(A)", color="blue")
plt.xlabel("Time")
plt.ylabel("dB(A)")
plt.title("Decibel Levels Over Time")
plt.legend()
plt.grid(True)

# Generate the plot filename with the current date
current_date_str = datetime.datetime.now(tz).strftime("%Y-%m-%d")
plot_filename = f"decibel_plot_{current_date_str}.png"

# Save the plot as an image file with the date in the filename
plt.savefig(plot_filename)

# Optionally, you can also print a message to indicate that the plot has been saved
print(f"Plot saved as '{plot_filename}'")