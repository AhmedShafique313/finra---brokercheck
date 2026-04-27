import csv
import os
import tempfile

def filter_active_bc_scope():
    # Define file paths - use raw string or forward slashes for Windows paths
    input_file = r'C:\Users\Ahmed Shafique\Downloads\Projects\FINRA - BrokerCheck - n8n\BrokerCheck-Induviduals.csv'
    
    # Alternative ways to specify the path:
    # input_file = 'C:/Users/Ahmed Shafique/Downloads/Projects/FINRA - BrokerCheck - n8n/BrokerCheck-Induviduals.csv'
    # OR
    # input_file = os.path.join('C:', os.sep, 'Users', 'Ahmed Shafique', 'Downloads', 'Projects', 
    #                           'FINRA - BrokerCheck - n8n', 'BrokerCheck-Induviduals.csv')

    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Reading {input_file} and filtering for Active BC scope (memory efficient)...")

    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', newline='', dir=os.path.dirname(input_file))
    temp_path = temp_file.name

    try:
        initial_count = 0
        active_count = 0
        removed_count = 0

        # Increase field size limit for large CSV fields
        csv.field_size_limit(2147483647)

        with open(input_file, mode='r', encoding='utf-8', newline='') as fin:
            reader = csv.DictReader(fin)
            header = reader.fieldnames

            if 'ind_bc_scope' not in header:
                print("Error: Column 'ind_bc_scope' not found in the CSV.")
                print(f"Available columns: {list(header)[:10]}...")
                fin.close()
                temp_file.close()
                os.remove(temp_path)
                return

            with open(temp_path, mode='w', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, fieldnames=header)
                writer.writeheader()

                for row in reader:
                    initial_count += 1
                    
                    # Keep only rows where ind_bc_scope is "Active"
                    if row['ind_bc_scope'] == 'Active':
                        writer.writerow(row)
                        active_count += 1
                    else:
                        removed_count += 1

                    if initial_count % 100000 == 0:
                        print(f"Processed {initial_count} rows... (Active: {active_count}, Removed: {removed_count})")

        print(f"\nFiltering Complete:")
        print(f"Initial record count: {initial_count}")
        print(f"Active records kept: {active_count}")
        print(f"Non-Active records removed: {removed_count}")

        # Close and replace original file
        temp_file.close()
        # On Windows, you must remove the destination before renaming
        os.replace(temp_path, input_file)
        print(f"Successfully saved filtered data to {input_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    filter_active_bc_scope()