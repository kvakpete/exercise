import csv
import json
import pickle
import os
import sys

class FileReaderWriter:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        raise NotImplementedError("Read method not implemented.")

    def write(self, data, destination_path):
        raise NotImplementedError("Write method not implemented.")

class CSVReaderWriter(FileReaderWriter):
    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                csv_reader = csv.reader(file)
                return [row for row in csv_reader]
        except Exception as e:
            print(f"Error occurred while reading CSV file: {e}")
            sys.exit(1)

    def write(self, data, destination_path):
        try:
            with open(destination_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(data)
        except Exception as e:
            print(f"Error occurred while writing CSV file: {e}")
            sys.exit(1)

class JSONReaderWriter(FileReaderWriter):
    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error occurred while reading JSON file: {e}")
            sys.exit(1)

    def write(self, data, destination_path):
        try:
            with open(destination_path, 'w') as file:
                json.dump(data, file)
        except Exception as e:
            print(f"Error occurred while writing JSON file: {e}")
            sys.exit(1)

class PickleReaderWriter(FileReaderWriter):
    def read(self):
        try:
            with open(self.file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"Error occurred while reading Pickle file: {e}")
            sys.exit(1)

    def write(self, data, destination_path):
        try:
            with open(destination_path, 'wb') as file:
                pickle.dump(data, file)
        except Exception as e:
            print(f"Error occurred while writing Pickle file: {e}")
            sys.exit(1)

def get_file_reader_writer(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension == '.csv':
        return CSVReaderWriter(file_path)
    elif extension == '.json':
        return JSONReaderWriter(file_path)
    elif extension == '.pickle':
        return PickleReaderWriter(file_path)
    else:
        raise ValueError("Unsupported file extension.")

def apply_changes(data, changes):
    for change in changes:
        try:
            col, row, value = map(str.strip, change.split(','))
            col = int(col)
            row = int(row)
            data[row][col] = value
        except ValueError:
            print(f"Invalid change format: {change}")
            continue
        except IndexError:
            print(f"Invalid row or column index: {change}")
            continue
    return data

def main():
    if len(sys.argv) < 4:
        print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
        sys.exit(1)

    src_file = sys.argv[1]
    dst_file = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.isfile(src_file):
        print(f"Error: {src_file} does not exist or is not a file.")
        print("Files in the current directory:")
        for file in os.listdir('.'):
            print(file)
        sys.exit(1)

    try:
        reader_writer = get_file_reader_writer(src_file)
        data = reader_writer.read()

        print("Original Data:")
        for row in data:
            print(row)

        modified_data = apply_changes(data, changes)

        print("Modified Data:")
        for row in modified_data:
            print(row)

        reader_writer.write(modified_data, dst_file)
        print(f"Data successfully written to {dst_file}")

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
