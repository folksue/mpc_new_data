import os
import pandas as pd
import shutil

def process_directory(source_dir, dest_dir):
    print(f"Processing directory: {source_dir} -> {dest_dir}")
    
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory does not exist: {source_dir}")
        return

    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.csv')]
    
    if not files:
        print(f"No CSV files found in {source_dir}")
        return

    for filename in files:
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(dest_dir, filename)
        
        try:
            # Read CSV
            df = pd.read_csv(source_path)
            
            # Check if required columns exist
            required_columns = ['Standard_Hz', 'Condition_ISI', 'Comparison_Hz']
            if all(col in df.columns for col in required_columns):
                # Sort based on criteria:
                # Standard_Hz -> Ascending
                # Condition_ISI -> Descending
                # Comparison_Hz -> Descending
                df_sorted = df.sort_values(
                    by=['Standard_Hz', 'Condition_ISI', 'Comparison_Hz'],
                    ascending=[True, False, False]
                )
                
                # Save sorted file
                df_sorted.to_csv(dest_path, index=False)
                print(f"Processed and saved: {filename}")
            else:
                print(f"Skipping {filename}: Missing required columns. Found columns: {df.columns.tolist()}")
                # Optionally copy the file as is if columns are missing, or just skip
                # For now, let's just skip to avoid errors
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Define paths
    source_old = r'C:\Users\folks\Downloads\Older Adults'
    dest_old = r'C:\mpc_new_data\old'
    
    source_young = r'C:\Users\folks\Downloads\young people'
    dest_young = r'C:\mpc_new_data\young'
    
    # Process 'Older Adults'
    process_directory(source_old, dest_old)
    
    # Process 'young people'
    process_directory(source_young, dest_young)
    
    print("Done.")
