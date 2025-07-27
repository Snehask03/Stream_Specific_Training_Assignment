import pandas as pd

# Task 1: Extract and Preview the Data
# Q1. The Superstore sales team has shared a new CSV file. Load the dataset and give a preview of the top 5 records to validate its structure.
#    Load Superstore.csv into a DataFrame.
#    Check number of rows and columns.
#    Display column names and their data types.

# Load Superstore.csv into a DataFrame.
df = pd.read_csv("Superstore.csv")

# preview of the top 5 records to validate its structure.
print(df.head())

# Check number of rows and columns.
print(f"The number of rows present: {df.shape[0]}")
print(f"The number of columns present: {df.shape[1]}")
print()

# Display column names and their data types.
print(f"The column names are:{df.columns.values}\n")
print("The column names with their datatypes:\n",df.dtypes)

# Task 2: Clean Column Names and Normalize Dates
#     Q2. Some columns have inconsistent names with spaces and slashes. 
#       Also, the dates are strings. Clean the column names and 
#       convert Order Date and Ship Date to datetime format 
#       so that you can later group data by month.
#    Clean column headers using .str.replace().
#    Convert Order_Date and Ship_Date to datetime64.
df.columns = df.columns.str.replace(' ', '_')
print(df.columns.values)
df.columns = df.columns.str.replace('/', "_")
print(df.columns.values)
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')
print(df['Order_Date'])
print(df['Ship_Date'])

#Task 3: Profitability by Region and Category
# Q3.The regional manager wants to know which region and category combinations are most profitable. 
# Summarize total Sales, Profit, and average Discount grouped by Region and Category.
#     Use groupby() + agg() to generate the report.
#     Identify which Region+Category had highest profit.
total_sales = df['Sales'].sum()
average_discount = df['Discount'].mean()
max_profit = df['Profit'].sum()
report = df.groupby(['Region', 'Category']).agg({'Sales':'sum', 'Profit':'sum','Discount':'mean'}).reset_index()
print(report)
most_profitable = report.sort_values(by='Profit', ascending=False).head(1)
print(most_profitable)

# Task 4: Top 5 Most Profitable Products
# Q4. The product team is planning to promote high-profit items. Identify the top 5 products that contributed the most to overall profit.
#     Group by Product_Name, sum the profit, sort descending, and take top 5.
top_profitable_product = df.groupby('Product_Name')['Profit'].sum().sort_values(ascending=False)
print(top_profitable_product.head(5))

# Task 5: Monthly Sales Trend
# Q5. The leadership team wants to review monthly sales performance to understand seasonality. Prepare a month-wise sales trend report.
#     Extract month from Order_Date
#     Group by month and sum Sales
df['Month_Name'] = df['Order_Date'].dt.month_name()
df['Month_Number'] = df['Order_Date'].dt.month
Monthly_sales = df.groupby(['Month_Number','Month_Name'])['Sales'].sum().reset_index()
print(Monthly_sales.sort_values(by='Month_Number'))

# Task 6: Cities with Highest Average Order Value
# Q6. The business is interested in targeting high-value cities for marketing. 
# Calculate the average order value (Sales ÷ Quantity) for each city and list the top 10.
#     Create a new column Order_Value
#     Group by City and calculate average order value
#     Sort and get top 10
df['Order_Value'] = df['Sales']/df['Quantity']
city_average_order_value = df.groupby('City')['Order_Value'].mean()
print(city_average_order_value.sort_values(ascending=False).head(10))

# Task 7: Identify and Save Orders with Loss
# Q7. Finance wants to analyze all loss-making orders. 
# Filter all records where Profit < 0 and 
# save it to a new file called loss_orders.csv.
#     Use boolean filtering
#     Export the filtered DataFrame to a CSV file without index

loss_orders_df = df[df['Profit'] < 0]
print(loss_orders_df)
loss_orders_df.to_csv('loss_orders.csv', index= False)

# Task 8: Detect Null Values and Impute
# Q8. Are there any missing values in the dataset? 
# If yes, identify columns with nulls and fill missing Price values with 1.
#     Use isnull().sum()
#     Apply fillna() only on Price column
# custom column : price = sales/quantity
# Added extra five rows at the end for null values

df['Price'] = df['Sales']/df['Quantity']
df['Price'] = df['Price'].fillna(1)
print(df['Price'].isnull().sum())
print(df.tail(7))

df.to_csv("Superstore_cleaned.csv", index=False)





