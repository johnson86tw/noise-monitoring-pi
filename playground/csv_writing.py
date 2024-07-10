import csv
from datetime import datetime
import random
import time
import os


def write_data_to_csv():
    try:
        while True:
            filename = datetime.now().strftime('%Y-%m-%d') + '.csv'
            file_exists = os.path.isfile(filename)

            # Open the CSV file in append mode
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)

                # Write the header row if the file is new
                if not file_exists:
                    writer.writerow(['Date', 'Decibel'])

                # Generate and write data row
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                decibel = generate_decibel()
                writer.writerow([timestamp, decibel])
                print(f'Written to {filename}: {timestamp}, {decibel}')

            # Wait for 1 second before generating the next reading
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScript interrupted.")


write_data_to_csv()


def generate_decibel():
    return round(random.uniform(30.0, 100.0), 2)
