import csv
from collections import defaultdict, Counter
from heapq import nlargest

def year_in_review(csv_file, year):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        
        # Skip the header
        # next(reader)

        # Initializing variables to hold summary data
        train_counts = defaultdict(int)
        line_counts = defaultdict(int)
        station_counts = defaultdict(int)
        trainnumber_counts = defaultdict(int)

        pair_counts = Counter()
        total_trips = 0
        trip_dates = []

        # Column indices (adjust based on your CSV structure)
        DATE_IDX = 3
        TRAIN_TYPE_IDX = 2
        LINE_IDX = 4
        LILYDALE_IDX = 5
        RINGWOOD_IDX = 6
        NUMBER_IDX = 1

        # Iterate through CSV rows
        for row in reader:
            trip_date = row[DATE_IDX]
            trip_year = trip_date.split('-')[0]
            
            if trip_year == str(year):
                total_trips += 1
                train_counts[row[TRAIN_TYPE_IDX]] += 1
                line_counts[row[LINE_IDX]] += 1
                station_counts[row[LILYDALE_IDX]] += 1
                station_counts[row[RINGWOOD_IDX]] += 1
                trainnumber_counts[row[NUMBER_IDX]] += 1

                # Track the pair of Lilydale and Ringwood stations
                pair = (row[LILYDALE_IDX], row[RINGWOOD_IDX])
                pair_counts[pair] += 1

                trip_dates.append((trip_date, row))  # Store date and full row for first/last trip
        
        # Sort trips by date
        trip_dates.sort(key=lambda x: x[0])

        # Function to get top 5 entries
        def get_top_n(counts_dict, n=4):
            return nlargest(n, counts_dict.items(), key=lambda x: x[1])

        # Get top 5 for each category
        top_5_trains = get_top_n(train_counts)
        top_5_lines = get_top_n(line_counts)
        top_5_stations = get_top_n(station_counts)
        top_5_trainnumbers = get_top_n(trainnumber_counts)


        # Get the first and last trip of the year
        first_trip = trip_dates[0][1] if trip_dates else None
        last_trip = trip_dates[-1][1] if trip_dates else None

        # Get the most common pair
        top_pair = pair_counts.most_common(1)[0] if pair_counts else None

        # Prepare the summary
        summary = {
            "total_trips": total_trips,
            "top_5_trains": top_5_trains,
            "top_5_lines": top_5_lines,
            "top_5_stations": top_5_stations,
            "first_trip": first_trip,
            "last_trip": last_trip,
            "top_pair": top_pair,
            "top_number": top_5_trainnumbers
        }

        return summary

def vline_metroprecent(csv_file, year):
    metroTrains = ["X'Trapolis 100", "HCMT", 'EDI Comeng', 'Alstom Comeng', 'Siemens Nexas', "X'Trapolis 2.0"]
    vlineTrains = ['VLocity', 'N Class', 'Sprinter']
    heritage = ['Tait', 'K Class', 'S Class', 'A Class', 'R Class', 'D2 Class', 'Y Class']
    
    metro_count = 0
    vline_count = 0
    heritage_count = 0
    other_count = 0
    
    DATE_IDX = 3

    try:
        with open(f'utils/trainlogger/userdata/{csv_file}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                trip_date = row[DATE_IDX]
                trip_year = trip_date.split('-')[0]
                if trip_year == str(year):
                    train_type = row[2]
                    # Debugging the train type
                    if train_type in metroTrains:
                        metro_count += 1
                    elif train_type in vlineTrains:
                        vline_count += 1
                    elif train_type in heritage:
                        heritage_count += 1
                    else:
                        other_count += 1

    except Exception as e:
        return f"Error reading file: {str(e)}"
    
    total = metro_count + vline_count + heritage_count + other_count

    # Avoid division by zero if total is 0
    if total == 0:
        return "Cannot calculate percentages, no trips found for the given year"

    # Calculate the percentage of each variable
    percentage_a = (metro_count / total) * 100
    percentage_b = (vline_count / total) * 100
    percentage_c = (heritage_count / total) * 100
    percentage_d = (other_count / total) * 100

    # Debugging output
    print(f"Total: {total}, Metro: {metro_count}, Vline: {vline_count}, Heritage: {heritage_count}, Other: {other_count}")
    
    data = f'`{percentage_a:.2f}%` Metro, `{percentage_b:.2f}%` V/Line, `{percentage_c:.2f}%` heritage, `{percentage_d:.2f}%` other.'
    return data

