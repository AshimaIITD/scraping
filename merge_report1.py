import pandas as pd

f1 = 'csv_files/515.csv'
f2 = 'csv_files/511.csv'
f3 = 'csv_files/141.csv'
f4 = 'csv_files/111.csv'
f5 = 'csv_files/711.csv'
f6 = 'csv_files/721.csv'

# Read each CSV file
file1 = pd.read_csv(f1)
file2 = pd.read_csv(f2)
file3 = pd.read_csv(f3)
file4 = pd.read_csv(f4)
file5 = pd.read_csv(f5)
file6 = pd.read_csv(f6)

columns_to_drop = ['jc_issued_sc', 'jc_issued_st', 'jc_issued_oth', 'jc_issued_total', 
'emp_provided_household_sc', 'emp_provided_household_st', 'emp_provided_household_oth', 
'emp_provided_women_count', 'emp_provided_persondays_sc', 'emp_provided_persondays_st', 
'families_completed_100_days_sc', 'families_completed_100_days_st', 'families_completed_100_days_oth', 
'families_completed_100_days_total', 'emp_provided_persondays_women', 'emp_provided_persondays_oth']
file1.drop(columns = columns_to_drop, inplace = True)
file1.rename(columns={'emp_provided_household_total': 'employment_provided_household'}, inplace = True)
file1.rename(columns={'emp_provided_persondays_total': 'employment_provided_total_persondays'}, inplace = True)

# Merge the files based on the specified columns
merged_data = pd.merge(file1, file2, on=['year', 'state', 'district', 'block', 'panchayat'])
merged_data = pd.merge(merged_data, file3, on=['year', 'state', 'district', 'block', 'panchayat'])
merged_data = pd.merge(merged_data, file4, on=['year', 'state', 'district', 'block', 'panchayat']) 
merged_data = pd.merge(merged_data, file5, on=['year', 'state', 'district', 'block', 'panchayat']) 
merged_data = pd.merge(merged_data, file6, on=['year', 'state', 'district', 'block', 'panchayat']) 

# Save the merged data to a new CSV file
merged_data.to_csv('merged_report1.csv', index=False)
