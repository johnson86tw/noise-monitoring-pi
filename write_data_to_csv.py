import os
import csv
from datetime import datetime

log_dir = "./logs"

def write_data_to_csv(decibel: float):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    filename = os.path.join(log_dir, datetime.now().strftime('%Y-%m-%d') + '.csv')
    file_exists = os.path.isfile(filename)

    # Open the CSV file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header row if the file is new
        if not file_exists:
            writer.writerow(['Date', 'Decibel'])

        # Generate and write data row
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([timestamp, decibel])
        print(f'Written to {filename}: {timestamp, decibel}')