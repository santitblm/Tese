import pandas as pd

# Load the original Excel file
input_file = 'RandomCodigos/outros/results.xlsx'
df = pd.read_excel(input_file)

# Get unique codes from the 44th column (assuming it's the 45th column since Python uses 0-based indexing)
unique_codes = df.iloc[:, 3].unique()

# Create a new DataFrame to store the results
#result_df = pd.DataFrame()
code_data = {}
# Iterate through unique codes and add data to the result DataFrame
for code in unique_codes:
    code_df = df[df.iloc[:, 3] == code]
    
    # Extract timestamps and numbers from the code-specific DataFrame
    timestamps = code_df.iloc[:, 1].tolist()
    numbers = code_df.iloc[:, 2].tolist()
    
    # Flatten the lists and create a dictionary for the result DataFrame
    code_data[code] = {'Timestamps': timestamps,
                 'Direction': numbers}
    
    # Append the data to the result DataFrame
print(code_data)
    #result_df = pd.concat([result_df, pd.DataFrame(code_data)], ignore_index=True)

# Reset the index of the result DataFrame
#result_df.reset_index(drop=True, inplace=True)

# Save the result to a new Excel file
#output_file = 'RandomCodigos/outros/output_file.xlsx'
#result_df.to_excel(output_file, index=False)
