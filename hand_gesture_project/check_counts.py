import csv
from collections import Counter

# Open the gesture data CSV file
with open("gesture_data.csv", mode='r') as file:
    reader = csv.reader(file)
    
    labels = []
    for row in reader:
        if row:  # skip empty lines
            label = int(float(row[-1]))  # last value is the gesture label
            labels.append(label)

# Count how many samples for each gesture
count = Counter(labels)

# Print the counts
for label in sorted(count):
    print(f"Gesture {label}: {count[label]} samples")

# If needed, print total
print(f"\nTotal samples: {sum(count.values())}")