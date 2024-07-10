from datetime import datetime
import csv
import os


def write_data_to_csv(decibel: float):
    try:
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
            writer.writerow([timestamp, decibel])
            print(f'Written to {filename}: {timestamp}, {decibel}')

    except KeyboardInterrupt:
        print("\nScript interrupted.")
