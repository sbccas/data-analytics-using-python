'''Understanding customer preferences and restaurant trends is important for making informed
business decisions in food industry. In this article, we will analyze Zomato’s restaurant dataset
using Python to find meaningful insights.
We aim to answer questions such as:

1. identify popular restaurant categories. (step-7)
2. Which restaurants are preferred by a larger number of individuals based on votes (step-8)
3. Find the restaurant with the highest number of votes. (step-9)
4. Exploring the online_order column to see how many restaurants accept online orders (step-10)
5. Analyze distribution of customer rating (step-11)
6. What price range do couples prefer for dining? (step-12)
7. Analyze customer ratings for Online vs Offline Orders (step-13)
8. Analyze order mode (online/offline) preference by restaurant type (step-14)'''


#Step 1: Importing necessary Python libraries.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Step 2: Creating the data frame.

dataframe = pd.read_csv("zomato-data.csv")

# display all column names
print(dataframe.columns)

# setting pandas display option to display all columns
pd.set_option('display.max_columns', None)

# display top few lines of data
print(dataframe.head(5))
# display shape of data
print(dataframe.shape)

#Step 3: Data Cleaning and Preparation
'''Before moving further we need to clean and process the data.
1. Convert the rate column to a float by removing denominator characters.
dataframe['rate']=dataframe['rate'].apply(handleRate):
Applies the handleRate function to clean and convert each rating value in the
'rate' column.'''

def handleRate(value):
    value=str(value).split('/')
    value=value[0];
    return float(value)

dataframe['rate']=dataframe['rate'].apply(handleRate)

print("----------After cleaning rate column, printing top few records")
print(dataframe[['name','rate']].head())

# Step 4: Getting summary of the dataframe using df.info()
print("----------Dataset summary------------------")
dataframe.info()

# Step 4.1: Getting description of the dataframe using df.describe()
print("----------Dataset description------------------")
print(dataframe.describe())

# Step 5: Checking for missing or null values to identify any data gaps (EDA)
print("---------Checking for missing or null values")
print(dataframe.isnull().sum())

# Step 6: Handling missing data: filling gaps with mean value (Data Preparation)
'''inplace parameter of fillna() if it is true it will update original dataset
and if it is false(default) it will not update original dataset, instead it will
return updated data'''
'''mean_votes = dataframe['votes'].mean()
dataframe['votes'].fillna(mean_votes,inplace=True)


mean_cost = dataframe['approx_cost(for two people)'].mean()
dataframe['approx_cost(for two people)'].fillna(mean_cost,inplace=True)'''

df_cleaned = dataframe.fillna(dataframe.mean(numeric_only=True))
print("displaying null value count after handling missing data with mean value")
print(df_cleaned.isnull().sum())
dataframe = df_cleaned

# step 6.1: understanding spread of data
# 1. Visualize the spread of 'rate' using a Histogram
plt.figure(figsize=(8, 5))
sns.histplot(dataframe['rate'], bins=10, kde=True)
plt.title("Distribution and Spread of Restaurant Ratings")
plt.show()
# 2. Compare the spread of 'approx_cc' across 'online_or' categories using Box Plots
plt.figure(figsize=(8, 5))
sns.boxplot(x='online_order', y='approx_cost(for two people)', data=dataframe)
plt.title("Cost Spread by Online Order Availability")
plt.show()

# Step 7: Exploring Restaurant Types (EDA - Univariate Analysis)
'''countplot() using Seaborn is commonly used in EDA to visualize categorical data.
A countplot shows the count (frequency) of each unique category in a categorical variable using bars.'''

'''order = dataframe['listed_in(type)'].value_counts().index
print("order=" + order)
sns.countplot(x='listed_in(type)',data=dataframe,order=order)'''
sns.countplot(x=dataframe['listed_in(type)'])
plt.title("Count of Restaurants")
plt.xlabel("Type of restaurant")
plt.show()
# Conclusion: The majority of the restaurants fall into the dining category.

# Step 8: Exploring Votes by Restaurant Type (EDA - Bivariate Analysis)

grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
print(grouped_data)
result = pd.DataFrame({'votes': grouped_data})
print(result)
plt.plot(result, c='green', marker='o')
plt.xlabel('Type of restaurant')
plt.ylabel('Votes')
plt.show()

#Conclusion: Dining restaurants are preferred by a larger number of individuals.

# Step 9: Identify the Most Voted Restaurant

max_votes = dataframe['votes'].max()
restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']

print('Restaurant(s) with the maximum votes:')
print(restaurant_with_max_votes)
# Conclusion: Empire State restaurant is most voted restaurant

# Step 10: Online Order Availability

sns.countplot(x=dataframe['online_order'])
plt.show()

#Conclusion: majority of the restaurants do not accept online orders.

# Step 11: Analyze customer Ratings

plt.hist(dataframe['rate'],bins=5)
plt.title('Ratings Distribution')
plt.show()

#Conclusion: The majority of restaurants received ratings ranging from 3.5 to 4.

# Step 12: Approximate Cost for Couples
# Analysing approx_cost(for two people) column to find the preferred price range

couple_data=dataframe['approx_cost(for two people)']
sns.countplot(x=couple_data)
plt.show()

#Conclusion: The majority of couples prefer restaurants with an approximate cost of 300 rupees.

# Step 13: Ratings Comparison - Online vs Offline Orders

plt.figure(figsize = (6,6))
sns.boxplot(x = 'online_order', y = 'rate', data = dataframe)
plt.show()

#Conclusion: Offline orders received lower ratings in comparison to online orders which obtained excellent ratings.

# Step 14: Order Mode Preferences by Restaurant Type

pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Heatmap')
plt.xlabel('Online Order')
plt.ylabel('Listed In (Type)')
plt.show()

'''With this we can say that dining restaurants primarily receive offline orders whereas
cafes primarily receive online orders. This suggests that clients prefer to place orders
in person at restaurants but prefer online ordering at cafes.'''
