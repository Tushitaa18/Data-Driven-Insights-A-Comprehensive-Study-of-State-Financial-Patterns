# -*- coding: utf-8 -*-
"""F Comparison of State Own Tax % and Total Expenditure.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w90AEpAmaZt9eQQNOnq8UtuSY_NihS_F
"""

# Install geopandas if you haven't already
!pip install geopandas

import geopandas as gpd
from google.colab import drive

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly.express as px

drive.mount('/content/drive')

import plotly.io as pio
pio.renderers.default = 'browser'



# Define the path to the GeoJSON file in Google Drive
geojson_file_path = '/content/drive/MyDrive/states_india.geojson'

# Load the GeoJSON file
india_states = gpd.read_file(geojson_file_path)

# Display the data
print(india_states.head())

with open(geojson_file_path, "r") as file:
    india_states = json.load(file)

# Display the loaded data
print(india_states)

state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

# Initialize the state_id_map
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    # Convert the name of the state/UT to uppercase
    state_name = feature["properties"]["st_nm"].upper()
    state_id_map[state_name] = feature["id"]

# File path to the dataset on Google Drive
file_path = '/content/drive/MyDrive/Revenue Expenditure.csv'

# Load the dataset
try:
    df2 = pd.read_csv(file_path)
    print("File loaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

df = pd.read_csv("india_census.csv")
df["Density"] = df["Density[a]"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
df["id"] = df["State or union territory"].apply(lambda x: state_id_map[x])

# Ensure 'srcStateName' is in uppercase to match keys in `state_id_map`
df2["state_code"] = df2["srcStateName"].str.upper().map(state_id_map)

# Check if mapping worked correctly
print(df2[["srcStateName", "state_code"]].head())

df.head()

# Import necessary libraries
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Set renderer to display plots inline in Colab
pio.renderers.default = 'colab'

# Load the geojson and CSV files (update paths if files are in Google Drive)
with open("india_states.geojson", "r") as f:
    india_states = json.load(f)

# Map state names to their IDs
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]

# Load and preprocess the dataset
df = pd.read_csv("/content/drive/MyDrive/Tax Collection.csv")

# Extract numerical density values from 'Density[a]' column
df["Total revenue"] = df["Total revenue[a]"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
df["id"] = df["srcStateName"].apply(lambda x: state_id_map.get(x))

# Display first few rows of the DataFrame to verify
print(df.head())

# Plot Density distribution
df["Total revenue"].plot(kind='bar', title="Population Density by State", figsize=(12, 6))

# Apply a log scale transformation
df["DensityScale"] = np.log10(df["Total revenue"])
df["DensityScale"].plot(kind='bar', title="Log-Scale Population Density by State", figsize=(12, 6))

# Plot choropleth map of India's population density
fig = px.choropleth(
    df,
    locations="id",
    geojson=india_states,
    color="DensityScale",
    hover_name="State or union territory",
    hover_data=["Total revenue"],
    title="India Population Density",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

fig = px.choropleth(
    df,
    locations="state_code",
    geojson=india_states,
    color="DensityScale",
    hover_name="State or union territory",
    hover_data=["Density"],
    title="India Population Density",
)
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

# Create a dictionary of old and new names to replace in the dataset
state_replacements = {
    'NATIONAL CAPITAL TERRITORY OF DELHI (DELHI)': 'NCT OF DELHI',
    'NATIONAL CAPITAL TERRITORY OF DELHI': 'NCT OF DELHI',
    'DELHI': 'NCT OF DELHI',
    'ARUNACHAL PRADESH': 'ARUNANCHAL PRADESH',  # Correct spelling
    'JAMMU AND KASHMIR': 'JAMMU & KASHMIR'  # Standardized to single version
}

# Use the replace() method to update the names in the 'srcStateName' column
df2['srcStateName'] = df2['srcStateName'].replace(state_replacements)

# Display the updated unique values in 'srcStateName' to confirm changes
print(df2['srcStateName'].unique())

# Use the replace() method to update the names in the 'srcStateName' column
df2['srcStateName'] = df2['srcStateName'].replace(state_replacements)


# Display the updated DataFrame
print(df2['srcStateName'].unique())

# Check all keys in state_id_map
print(state_id_map.keys())

new_state = "DELHI"
new_state_id = 36

# Adding the new state and its ID to the dictionary
state_id_map[new_state.upper()] = new_state_id

# Display the updated state_id_map
print(state_id_map)

# Apply the state_id_map by first converting the state names in df2["srcStateName"] to uppercase
df2["id"] = df2["srcStateName"].apply(lambda x: state_id_map[x.upper()])



file_path = '/content/drive/MyDrive/Tax Collection.csv'
try:

    df = pd.read_csv(file_path)
    print("File loaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

df.shape

df.isnull().sum()

file_path = '/content/drive/MyDrive/Revenue Expenditure.csv'
try:

    df2 = pd.read_csv(file_path)
    print("File loaded successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

df2.shape

df2.isnull().sum()

pd.set_option('display.max_columns', None)

df.head()

df2.head()

df['State own tax %'] = (df['State own tax revenue '] / df['Total revenue']) * 100

print(df[['srcStateName', 'srcYear', 'Total revenue', 'State own tax revenue ', 'State own tax %']].head())

# Filter the dataset for 'Budget Estimates' and the specified YearCode
filtered_df = df[(df['Budget type'] == 'Accounts') & (df['YearCode'] == 2017)]

# Drop any rows where 'State own tax %' might be NaN or zero to avoid empty slices
filtered_df_nonzero = filtered_df[filtered_df['State own tax %'] > 0]

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(filtered_df_nonzero['State own tax %'], labels=filtered_df_nonzero['srcStateName'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)

# Add a title
plt.title('State Own Tax Revenue as % of Total Revenue (Accounts, 2017)', fontsize=14)

# Show the plot
plt.show()

import seaborn as sns

# Sort data by percentage for better visualization
filtered_df_sorted = filtered_df.sort_values(by='State own tax %', ascending=False)

# Create a barplot using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='srcStateName', y='State own tax %', data=filtered_df_sorted, palette='pastel')

# Add labels and title
plt.xlabel('State/UT', fontsize=12)
plt.ylabel('State Own Tax %', fontsize=12)
plt.title('State Own Tax Contribution as % of Total Revenue (Accounts, 2017)', fontsize=14)
plt.xticks(rotation=90)  # Rotate state names for readability

# Show the plot
plt.tight_layout()
plt.show()

import pandas as pd

# Sample dataframes df and df2 for demonstration
# (assuming df and df2 are already defined as per your sample)

# Step 1: Combine the unique srcStateName from both DataFrames to ensure all states get a unique ID
unique_states = pd.DataFrame(pd.concat([df['srcStateName'], df2['srcStateName']]).unique(), columns=['srcStateName'])

# Step 2: Create a unique state ID for each srcStateName
unique_states['stateID'] = range(1, len(unique_states) + 1)

# Step 3: Merge the unique stateID back into the original DataFrames
df = df.merge(unique_states, on='srcStateName', how='left')
df2 = df2.merge(unique_states, on='srcStateName', how='left')

# Now df and df2 have a common column 'stateID' for linking them together

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df and df2 are already defined with 'stateID_x' column

# Step 1: Filter df and df2 for Budget type == 'Accounts' and YearCode == 2019
df_filtered = df[(df['Budget type'] == 'Accounts') & (df['YearCode'] == 2019)]
df2_filtered = df2[(df2['Budget type'] == 'Accounts') & (df2['YearCode'] == 2019)]

# Step 2: Merge the filtered DataFrames on 'stateID_x' to align data by state
merged_df = pd.merge(df_filtered[['stateID_x', 'srcStateName', 'State own tax %']],
                     df2_filtered[['stateID_x', 'Total expenditure']],
                     on='stateID_x',
                     how='inner')

# Step 3: Plot the comparison
plt.figure(figsize=(12, 8))

# Bar plot for State own tax %
plt.bar(merged_df['srcStateName'], merged_df['State own tax %'], color='skyblue', label='State own tax %', width=0.4, align='center')

# Line plot for Total expenditure (scaled down to match the tax % range for comparison)
plt.plot(merged_df['srcStateName'], merged_df['Total expenditure'] / 1e5, color='orange', marker='o', label='Total expenditure (scaled down)')

# Adding labels and title
plt.xlabel('State')
plt.ylabel('Values')
plt.title('Comparison of State Own Tax % and Total Expenditure for 2019 (Accounts)')
plt.xticks(rotation=90)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df and df2 are already defined with 'stateID_x' column

# Step 1: Filter df and df2 for Budget type == 'Accounts' and YearCode == 2017
df_filtered = df[(df['Budget type'] == 'Accounts') & (df['YearCode'] == 2017)]
df2_filtered = df2[(df2['Budget type'] == 'Accounts') & (df2['YearCode'] == 2017)]

# Step 2: Merge the filtered DataFrames on 'stateID_x' to align data by state
merged_df = pd.merge(df_filtered[['stateID_x', 'srcStateName', 'State own tax %']],
                     df2_filtered[['stateID_x', 'Total expenditure']],
                     on='stateID_x',
                     how='inner')

# Step 3: Plot the comparison
plt.figure(figsize=(12, 8))

# Bar plot for State own tax %
plt.bar(merged_df['srcStateName'], merged_df['State own tax %'], color='skyblue', label='State own tax %', width=0.4, align='center')

# Line plot for Total expenditure (scaled down to match the tax % range for comparison)
plt.plot(merged_df['srcStateName'], merged_df['Total expenditure'] / 1e5, color='orange', marker='o', label='Total expenditure (scaled down)')

# Adding labels and title
plt.xlabel('State')
plt.ylabel('Values')
plt.title('Comparison of State Own Tax % and Total Expenditure for 2017 (Accounts)')
plt.xticks(rotation=90)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df and df2 are already defined with 'stateID_x' column

# Step 1: Filter df and df2 for Budget type == 'Accounts' and YearCode == 2014
df_filtered = df[(df['Budget type'] == 'Accounts') & (df['YearCode'] == 2014)]
df2_filtered = df2[(df2['Budget type'] == 'Accounts') & (df2['YearCode'] == 2014)]

# Step 2: Merge the filtered DataFrames on 'stateID_x' to align data by state
merged_df = pd.merge(df_filtered[['stateID_x', 'srcStateName', 'State own tax %']],
                     df2_filtered[['stateID_x', 'Total expenditure']],
                     on='stateID_x',
                     how='inner')

# Step 3: Plot the comparison
plt.figure(figsize=(12, 8))

# Bar plot for State own tax %
plt.bar(merged_df['srcStateName'], merged_df['State own tax %'], color='skyblue', label='State own tax %', width=0.4, align='center')

# Line plot for Total expenditure (scaled down to match the tax % range for comparison)
plt.plot(merged_df['srcStateName'], merged_df['Total expenditure'] / 1e5, color='orange', marker='o', label='Total expenditure (scaled down)')

# Adding labels and title
plt.xlabel('State')
plt.ylabel('Values')
plt.title('Comparison of State Own Tax % and Total Expenditure for 2014 (Accounts)')
plt.xticks(rotation=90)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming df and df2 are already defined with 'stateID_x' column

# Step 1: Filter df and df2 for Budget type == 'Accounts' and YearCode == 2011
df_filtered = df[(df['Budget type'] == 'Accounts') & (df['YearCode'] == 2011)]
df2_filtered = df2[(df2['Budget type'] == 'Accounts') & (df2['YearCode'] == 2011)]

# Step 2: Merge the filtered DataFrames on 'stateID_x' to align data by state
merged_df = pd.merge(df_filtered[['stateID_x', 'srcStateName', 'State own tax %']],
                     df2_filtered[['stateID_x', 'Total expenditure']],
                     on='stateID_x',
                     how='inner')

# Step 3: Plot the comparison
plt.figure(figsize=(12, 8))

# Bar plot for State own tax %
plt.bar(merged_df['srcStateName'], merged_df['State own tax %'], color='skyblue', label='State own tax %', width=0.4, align='center')

# Line plot for Total expenditure (scaled down to match the tax % range for comparison)
plt.plot(merged_df['srcStateName'], merged_df['Total expenditure'] / 1e5, color='orange', marker='o', label='Total expenditure (scaled down)')

# Adding labels and title
plt.xlabel('State')
plt.ylabel('Values')
plt.title('Comparison of State Own Tax % and Total Expenditure for 2011 (Accounts)')
plt.xticks(rotation=90)
plt.legend()

# Show plot
plt.tight_layout()
plt.show()

