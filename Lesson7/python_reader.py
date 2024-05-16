import csv
import sys
import os

def apply_changes(csv_data, changes):
    for change in changes:
        try:
            col, row, value = map(str.strip, change.split(','))
            col = int(col)
            row = int(row)
            csv_data[row][col] = value
        except ValueError:
            print(f"Invalid change format: {change}")
            continue
        except IndexError:
            print(f"Invalid row or column index: {change}")
            continue

def read_csv_file(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            csv_data = list(csv_reader)
        return csv_data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        print(f"Files in directory: {', '.join(os.listdir())}")
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred while reading file: {e}")
        sys.exit(1)

def write_csv_file(file_path, csv_data):
    try:
        with open(file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(csv_data)
    except Exception as e:
        print(f"Error occurred while writing file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 4:
        print("Usage: python_reader.py <src> <dst> <change1> <change2> ...")
        sys.exit(1)

    src_file = sys.argv[1]
    dst_file = sys.argv[2]
    changes = sys.argv[3:]

    csv_data = read_csv_file(src_file)
    apply_changes(csv_data, changes)
    write_csv_file(dst_file, csv_data)

    print("Modified CSV content:")
    for row in csv_data:
        print(','.join(row))

if __name__ == "__main__":
    main()
