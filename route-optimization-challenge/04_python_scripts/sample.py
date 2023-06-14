import csv
import random

# Set the paths for the input and output files
input_file = "G:/Shared drives/common/personal-folders-team/Ujjwal-Dhiman/data-training/route-optimization-challenge/singapore_taxi_stand_data.csv"
output_file = "50_sampled.csv"

# Set the number of data points to sample
sample_size = 50

# Read the input CSV file
with open(input_file, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the header row
    data = list(reader)    # Read the remaining data rows

# Sample the data points
sample = random.sample(data, sample_size)

# Write the sampled data to a new CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Write the header row
    writer.writerows(sample)  # Write the sampled data rows

print("Sampled data has been saved to", output_file)
