from commands.traintimleyfetcher import getchannelstocheck
from utils.search import trainData
from utils.trainlogger.map.line_coordinates_log_train_map_pre_munnel import getTotalLines
from utils.trainlogger.map.readlogs import logMap
from utils.trainlogger.map.lines_dictionaries import *
from utils.trainlogger.stats import getTotalTrips

import os
import csv
from collections import defaultdict
from datetime import datetime
import pandas as pd

# Directory to scan
root_dir = 'utils/trainlogger/userdata'

# Date is in the 4th column (0-based index 3)
date_column_index = 3

# Dictionary to hold count of logs per day
daily_counts = defaultdict(int)

# Traverse the directory and subdirectories
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(subdir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    header = next(reader, None)  # Skip header if exists
                    for row in reader:
                        if len(row) > date_column_index:
                            date_str = row[date_column_index].strip()
                            # Validate date format (yyyy-mm-dd)
                            try:
                                datetime.strptime(date_str, '%Y-%m-%d')
                                daily_counts[date_str] += 1
                            except ValueError:
                                print(f"Invalid date format in {file_path}: {date_str}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# If no data, exit
if not daily_counts:
    print("No logs found.")
    exit()

# Convert to DataFrame for sorting and cumulative sum
df = pd.DataFrame(list(daily_counts.items()), columns=['date', 'daily_logs'])
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df['cumulative_logs'] = df['daily_logs'].cumsum()

# Create a copy to avoid modifying a slice
output_df = df[['date', 'cumulative_logs']].copy()  # Explicit copy
output_df.loc[:, 'date'] = output_df['date'].dt.strftime('%Y-%m-%d')  # Use .loc for assignment

# Write to new CSV
output_file = 'cumulative_logs.csv'
output_df.to_csv(output_file, index=False)

print(f"Output written to {output_file}")
