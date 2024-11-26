import time
from datetime import datetime, timedelta
import trainline
import csv
import os

# Initialize the starting dates
from_date = datetime.strptime("01/03/2025 00:00", "%d/%m/%Y %H:%M")
to_date = datetime.strptime("01/03/2025 23:59", "%d/%m/%Y %H:%M")

# Stop date
stop_date = datetime.strptime("31/03/2025 00:00", "%d/%m/%Y %H:%M")

# Output CSV file path (saved in the project folder)
output_csv = os.path.join(os.getcwd(), "FI-RM_mar_train_coach.csv")

# Initialize the CSV file with headers
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Add a header row (adjust these to match the structure of `results.csv()`)
    writer.writerow(["departure_date","arrival_date","duration","number_of_segments", "price", "currency","transportation_mean", "bicycle_reservation"])

# Loop to run every minute
while True:
    try:
        # Check if we reached the stop date
        if from_date > stop_date:
            print("Reached the stop date. Exiting loop.")
            break

        # Format dates to strings for the search function
        from_date_str = from_date.strftime("%d/%m/%Y %H:%M")
        to_date_str = to_date.strftime("%d/%m/%Y %H:%M")
        
        # Print current dates
        print(f"Running search for dates: {from_date_str} to {to_date_str}")

        # Perform the search
        results = trainline.search(
            departure_station="firenze",
            arrival_station="roma",
            from_date=from_date_str,
            to_date=to_date_str
        )

        # Parse results into rows (assuming results.csv() provides CSV-like text)
        rows = results.csv().splitlines()  # Convert CSV text to a list of rows

        # Append rows to the CSV file
        with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in csv.reader(rows):
                writer.writerow(row)  # Append each row

        # Increment the dates by one day
        from_date += timedelta(days=1)
        to_date += timedelta(days=1)

        # Wait for one minute before the next iteration
        time.sleep(60)

    except Exception as e:
        # Handle any exceptions (like network issues or API errors) gracefully
        print(f"An error occurred: {e}")
        break





