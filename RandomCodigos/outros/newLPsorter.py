import pandas as pd

# Load the original Excel file
input_file = 'RandomCodigos/outros/results.xlsx'
df = pd.read_excel(input_file)

# Get unique codes from the 45th column (assuming it's the 46th column since Python uses 0-based indexing)
unique_codes = df.iloc[:, 3].unique()
code_data = {}
# Create a new DataFrame to store the results
result_df = pd.DataFrame()

# Define a similarity function that compares codes
def code_similarity(code1, code2):
    # Compare codes and check if at least 4 characters are the same
    common_chars = sum(c1 == c2 for c1, c2 in zip(code1, code2))
    return 6 > common_chars >= 4

# Create a dictionary to group similar codes
code_groups = {}

# Iterate through unique codes and group similar codes
for code in unique_codes:
    # Initialize a group for the current code
    group = [code]
    
    # Iterate through unique codes again to find similar ones
    for other_code in unique_codes:
        if type(other_code) == str and type(code) == str:
            if code_similarity(code, other_code):
                group.append(other_code)
    
    # Add the group to the dictionary
    code_groups[code] = group

# Extract unique grouped codes
unique_grouped_codes = list(set(tuple(group) for group in code_groups.values()))

# Iterate through unique grouped codes and add data to the result DataFrame
for code_group in unique_grouped_codes:
    # Create an empty list for timestamps and numbers
    timestamps = []
    numbers = []
    
    for code in code_group:
        code_df = df[df.iloc[:, 3] == code]
        timestamps.extend(code_df.iloc[:, 1].tolist())
        numbers.extend(code_df.iloc[:, 2].tolist())
    
    # Create a dictionary for the result DataFrame, # Use the first code as the representative
    code_data[code_group[0]] = {'Timestamps': timestamps, 'Numbers': numbers}
    
print(code_data)
    # Append the data to the result DataFrame
#result_df = result_df._append(pd.DataFrame(code_data))

# Reset the index of the result DataFrame
#result_df.reset_index(drop=True, inplace=True)
df = pd.DataFrame()

# Iterate through the dictionary and add the data to the DataFrame
for key, value in code_data.items():
    timestamps = value['Timestamps']
    numbers = value['Numbers']
    data_dict = {'Entry': [key]}
    data_dict.update({f'Timestamps_{i+1}': [timestamps[i]] for i in range(len(timestamps))})
    data_dict.update({f'Numbers_{i+1}': [numbers[i]] for i in range(len(numbers))})
    df = df._append(pd.DataFrame(data_dict), ignore_index=True)

# Save the DataFrame to an Excel file
df.to_excel('RandomCodigos/outros/output.xlsx', index=False)