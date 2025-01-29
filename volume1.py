# Open the text file and read the data
file_path = 'UDP.txt'  # Replace with your file path

with open(file_path, 'r') as file:
    lines = file.readlines()

# Parse the data into a 2D array
data = []
for line in lines[1:]:  # Skip the first line (assumes it's a header or count)
    parts = line.strip().split(',')
    row = [parts[0]] + list(map(int, parts[1:]))
    data.append(row)

# Calculate the combined volume
combined_volume = 0
for row in data:
    length, breadth, height = row[1], row[2], row[3]
    combined_volume += length * breadth * height
    print(length * breadth * height)

# Print the result
print("Combined Volume:", combined_volume)


# Volume : 105171504