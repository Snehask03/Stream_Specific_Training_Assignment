import pandas as pd

df = pd.read_csv("final_college_student_placement_dataset.csv")
# print(df.head())

# 1. Categorize placed students into salary bands:
#     Low: < 300,000
#     Medium: 300,000 – 600,000
#     High: > 600,000

placed_students = df[df['Placement'] == 'Yes']
def salary_band(Salary):
    if Salary < 300000:
        return 'Low'
    elif Salary <= 600000:
        return 'Medium'
    else:
        return 'High'

placed_students['Salary_band'] = placed_students['Salary'].apply(salary_band)
print(placed_students['Salary_band'].value_counts())
print(placed_students.head(5))

# 2. For each gender and specialization, calculate:
#     Placement rate
#     Average salary (only placed)
#     Avg MBA score
placement_rate = df.groupby(['Gender', 'Specialization'])['Placement'].apply(lambda x: (x == 'Yes').mean())
avg_salary = df[df['Placement'] == 'Yes'].groupby(['Gender', 'Specialization'])['Salary'].mean()
avg_mba = df.groupby(['Gender', 'Specialization'])['MBA_Percentage'].mean()
report1 = pd.DataFrame({
    'Placement_rate': placement_rate,
    'Average_Salary_placed':avg_salary,
    'Average_MBA':avg_mba
})
print(report1)

# 3.Find how many students have missing values in any column.
print(df[df.isnull().any(axis=1)])

# 4. Display all rows where salary is missing.
print(df[df['Salary'] == 0]) # 0 is used to indicate missing salary values in the dataset

# 5. Filter only students with complete records (no missing values).
complete_records = df[df.notnull().all(axis=1)]
print(complete_records)

#  6. Identify if there are any duplicate student entries.
duplicate_students_entries = df[df.duplicated()]
print(duplicate_students_entries)

#  7. Drop the duplicate records and keep only the first occurrence.
no_duplicate_df = df.drop_duplicates(keep='first')
print(no_duplicate_df)

#  8. Check for duplicates based only on student_id.
duplicate_id = df[df.duplicated('College_ID', keep=False)]
print(duplicate_id)

# 9.Find all unique specializations offered to students.
print(df['Specialization'].unique())

# 10. How many unique MBA scores are there?
print(df['MBA_Percentage'].unique())

# 11. Count of unique combinations of gender, specialization, and status
unique_combination = df[['Gender', 'Specialization', 'Placement']].drop_duplicates().shape[0]
print(unique_combination)

# 12. What is the average salary of all placed students?
print(df[df['Placement'] == 'Yes']['Salary'].mean())

# 13. What is the maximum and minimum degree percentage in the dataset?
print(df['CGPA'].max())
print(df['CGPA'].min())

# 14. Get total number of placed and unplaced students.
print(df['Placement'].value_counts())

# 15.For each specialization, calculate:
#     Average SSC
#     Average MBA
#     Placement count

report = df.groupby(['Specialization']).agg({'SSC_Percentage':'mean', 'HSC_Percentage':'mean','Placement':lambda x:(x =='Yes').sum()}).reset_index()
print(report)

# 16. Create a summary table with:
#     Column name
#     Count of nulls
#     Count of unique values
#     Duplicated value count (if applicable)
summary_df = pd.DataFrame({
    'Column_Names':df.columns,
    'Null_Values_Count':[df[col].isnull().sum() for col in df.columns],
    'Unique_Values': [len(df[Col].dropna().unique()) for Col in df.columns],
    'Duplicate Count': [df[Col].duplicated().sum() for Col in df.columns]
})
print(summary_df)






