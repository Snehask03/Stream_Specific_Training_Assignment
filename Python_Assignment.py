import pandas as pd

df = pd.read_csv("updated_college_student_placement_dataset.csv")
# print(df.head())

# SET-1

# 1. How many students are in the dataset?
print(df.shape[0])

# 2.Display the number of male and female students.
print(df['Gender'].value_counts())

# 3.What is the average percentage in MBA?
print(df.MBA_Percentage.mean())

#  4.Show students who scored more than 80% in both SSC and HSC.
print(df[(df['SSC_Percentage'] > 80) & (df['HSC_Percentage'] > 80)])

#  5.Filter only students who have prior work experience.
print(df[df['Internship_Experience'] == 'Yes'])

#  6. Average MBA score per specialization.

# 7. Count of placed vs not placed students.
print(df['Placement'].value_counts())

# 8.Placement ratio per specialization.

# 9. Create a new column placement_success with:
#  	"High" if placed and salary > ₹950,000
#  	"Average" if placed and salary <= ₹400,000
#  	"Unplaced" if not placed
placed_students = df[df['Placement'] == 'Yes']
def placed_Success(row):
    if row['Placement'] == 'Yes'  and row['Salary'] > 950000:
        return 'High'
    elif row['Placement'] == 'Yes'  and row['Salary'] <= 400000:
        return "Average"
    elif row['Placement'] == 'No':
        return "Unplaced"
    else:
        return "Moderate"
    
df['Placement_success'] = df.apply(placed_Success, axis=1)
print(df[['Placement', 'Salary', 'Placement_success']].head())
print(df['Placement_success'].value_counts())

#  10. Among placed students, which degree percentage range leads to highest average salary?
def cgpa_range(CGPA):
    if CGPA < 6:
        return "Above 6"
    elif CGPA < 7:
        return "Above 7"
    elif CGPA < 8:
        return "7-8"
    elif CGPA < 9:
        return "8-9"
    else:
        return "9+"
placed_students['cgpa_range'] = placed_students['CGPA'].apply(cgpa_range)
average_salary_by_cgpa = placed_students.groupby('cgpa_range')['Salary'].mean().sort_values(ascending= False)
print(average_salary_by_cgpa)

# SET-2
#1. Categorize placed students into salary bands:
 	# Low: < 300,000
 	# Medium: 300,000 – 600,000
 	# High: > 600,000

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
#  	Placement rate
#  	Average salary (only placed)
#  	Avg MBA score

# 3.Find how many students have missing values in any column.
print(df[df.isnull().any(axis=1)]) # no missing values

#  4. Display all rows where salary is missing.
print(df[df['Salary'] == 0])

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



