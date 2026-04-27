import csv
import os
import tempfile

def remove_duplicates():
    # Define file paths
    input_file = os.path.join('..', 'BrokerCheck-Induviduals.csv')

    # Check if the file exists
    if not os.path.exists(input_file):
        # Try local path if called from root
        input_file = 'BrokerCheck-Induviduals.csv'
        if not os.path.exists(input_file):
            print(f"Error: {input_file} not found.")
            return

    print(f"Reading {input_file} and removing duplicates (memory efficient)...")

    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', newline='', dir=os.path.dirname(input_file))
    temp_path = temp_file.name

    try:
        seen_ids = set()
        initial_count = 0
        final_count = 0

        # Increase field size limit for large CSV fields
        csv.field_size_limit(2147483647)

        with open(input_file, mode='r', encoding='utf-8', newline='') as fin:
            reader = csv.DictReader(fin)
            header = reader.fieldnames

            if 'ind_source_id' not in header:
                print("Error: Column 'ind_source_id' not found in the CSV.")
                print(f"Available columns: {header[:5]}...")
                fin.close()
                temp_file.close()
                os.remove(temp_path)
                return

            with open(temp_path, mode='w', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, fieldnames=header)
                writer.writeheader()

                for row in reader:
                    initial_count += 1
                    source_id = row['ind_source_id']

                    if source_id not in seen_ids:
                        seen_ids.add(source_id)
                        writer.writerow(row)
                        final_count += 1

                    if initial_count % 100000 == 0:
                        print(f"Processed {initial_count} rows...")

        removed_count = initial_count - final_count

        print(f"Initial record count: {initial_count}")
        print(f"Removed {removed_count} duplicate records.")
        print(f"Final record count: {final_count}")

        # Close and replace original file
        temp_file.close()
        # On Windows, you must remove the destination before renaming
        os.replace(temp_path, input_file)
        print(f"Successfully saved cleaned data to {input_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    remove_duplicates()
