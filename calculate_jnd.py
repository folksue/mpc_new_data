import os
import pandas as pd

def get_min_jnd(df, freq, isi):
    # Filter for the specific condition
    # Note: Using strict equality. Ensure types match (int vs float usually handled ok by pandas, but good to be aware)
    subset = df[
        (df['Condition_Freq'] == freq) & 
        (df['Condition_ISI'] == isi)
    ]
    
    if subset.empty:
        return None
    
    # The data is sorted by Comparison_Hz (and Delta_Hz) Descending.
    # User logic: "Search in reverse order within each group, and find the first instance where Accuracy=1"
    # Reverse order of Descending is Ascending (Smallest to Largest).
    
    # Let's iterate from the last row to the first row
    for index in range(len(subset) - 1, -1, -1):
        row = subset.iloc[index]
        if row['Accuracy'] == 1:
            return row['Delta_Hz']
            
    return None

def process_folder(folder_path, group_name):
    results = []
    
    if not os.path.exists(folder_path):
        print(f"Warning: Folder not found: {folder_path}")
        return results

    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]
    
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(filepath)
            
            # Assuming Subj_ID is consistent in the file, take the first one
            subj_id = df['Subj_ID'].iloc[0] if not df.empty else "Unknown"
            
            # Calculate JND for each condition
            jnd_500_1000 = get_min_jnd(df, 500, 1000)
            jnd_500_100 = get_min_jnd(df, 500, 100)
            jnd_3000_1000 = get_min_jnd(df, 3000, 1000)
            jnd_3000_100 = get_min_jnd(df, 3000, 100)
            
            results.append({
                'filename': filename,
                'Subj_ID': subj_id,
                'Group': group_name,
                'JND_500_1000': jnd_500_1000,
                'JND_500_100': jnd_500_100,
                'JND_3000_1000': jnd_3000_1000,
                'JND_3000_100': jnd_3000_100
            })
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    return results

def main():
    old_folder = r'c:\mpc_new_data\old'
    young_folder = r'c:\mpc_new_data\young'
    
    all_results = []
    
    print("Processing Old Group...")
    all_results.extend(process_folder(old_folder, 'Old'))
    
    print("Processing Young Group...")
    all_results.extend(process_folder(young_folder, 'Young'))
    
    if all_results:
        summary_df = pd.DataFrame(all_results)
        
        # Save to CSV
        output_path = r'c:\mpc_new_data\jnd_summary.csv'
        summary_df.to_csv(output_path, index=False)
        print(f"\nSummary saved to: {output_path}")
        
        # Display the result
        print("\nCalculated JND Values (Minimum Delta_Hz with Accuracy=1):")
        print(summary_df.to_markdown(index=False))
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
