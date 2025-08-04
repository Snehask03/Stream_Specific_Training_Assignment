import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Question

#1. Analyze the average quality of wine produced by different countries
# You are provided with a dataset winemag-data-130k-v2.csv which contains wine reviews, 
# including the country of origin and wine ratings (points). Your task is to:
# Group the dataset by country and calculate the average rating (points) for wines from each country.
# Sort the results in descending order to identify the top 10 countries with the highest average rating.
# Visualize these top 10 countries using a horizontal bar chart with appropriate title, labels, and layout formatting.

# 2.Wine Rating Analysis by Country
# You are working with a wine review dataset named winemag-data-130k-v2.csv, 
# which includes information such as
# wine ratings (in "points") and the country of origin.
# Your objective is to analyze which countries produce the highest-rated wines on average.
# Group the dataset by country and calculate the average wine rating (points) for each country.
# Sort the results in descending order and extract the top 10 countries with the highest average rating.
# Create a horizontal bar chart to visualize these top 10 countries.
# X-axis should show: Average Rating (Points)
# Y-axis should show: Country
# Use an appropriate color for the bars (e.g., orchid).
# Include a title: "Top 10 Countries by Average Wine Rating"
# Rotate labels or adjust layout if needed for clarity.

# Answer

df = pd.read_csv("winemag-data-130k-v2.csv", index_col=0)
country_average_points = df.groupby('country')['points'].mean().sort_values(ascending=False)
print(country_average_points.head(10))
top_10_countries = country_average_points.head(10)
plt.figure(figsize=(10,5))
top_10_countries.plot(kind="barh",color="orchid")
plt.title("Top 10 Countries by Average Wine Rating")
plt.xlabel("Average Rating (Points)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()
