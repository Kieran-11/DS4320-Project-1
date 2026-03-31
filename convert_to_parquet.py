import pandas as pd
import os

# Define the output directory name
output_folder = 'processed_parquet_data'

# Create a local directory for the files if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Print the absolute path so you know exactly where the files are being saved
print(f"Saving files to: {os.path.abspath(output_folder)}")

# Define your tables (assuming they are currently in your DuckDB connection 'con')
tables = ['players', 'combine_stats', 'pro_performance', 'position_groups']

for table in tables:
    try:
        # Fetch from DuckDB into a DataFrame
        df = con.execute(f"SELECT * FROM {table}").df()
        
        # Define the full file path
        file_path = os.path.join(output_folder, f"{table}.parquet")
        
        # Save as Parquet
        df.to_parquet(file_path, index=False)
        
        # Verify the file was created
        if os.path.exists(file_path):
            print(f"Successfully saved {table} to {file_path} ({os.path.getsize(file_path)} bytes)")
        else:
            print(f"Error: File {file_path} was not created.")
            
    except Exception as e:
        print(f"Failed to convert table '{table}': {e}")

print("\nConversion process complete. You can now upload the contents of this folder to your UVA OneDrive.")
