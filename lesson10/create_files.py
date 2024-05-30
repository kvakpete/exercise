import csv
import json
import pickle

data = [
    ["door", "3", "7", "0"],
    ["sand", "12", "5", "1"],
    ["brush", "22", "34", "5"],
    ["poster", "red", "8", "stick"]
]

# Create CSV file
with open('source.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(data)

# Create JSON file
with open('source.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

# Create Pickle file
with open('source.pickle', 'wb') as pickle_file:
    pickle.dump(data, pickle_file)
