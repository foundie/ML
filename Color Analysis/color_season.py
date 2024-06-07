import pandas as pd
import numpy as np

# Function to adjust brightness
def adjust_brightness(color, factor):
    return np.clip(color * factor, 0, 255).astype(int)

# Load the original CSV file
df = pd.read_csv('D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\personal_color_season.csv', delimiter=';')  # Specify delimiter

# Print column names for debugging
print("Columns:", df.columns)

# Check if 'season' column exists
if 'season' not in df.columns:
    raise KeyError("'season' column not found in the CSV file.")

# Define brightness factors for new chroma choices
brightness_factors = [0.8, 0.9, 1.1, 1.2]

# Process each row in the dataframe
adjusted_dfs = []

for factor in brightness_factors:
    adjusted_df = df.copy()  # Create a copy of the original dataframe
    adjusted_df[['R_adjusted', 'G_adjusted', 'B_adjusted']] = np.clip(df[['R', 'G', 'B']] * factor, 0, 255).astype(int)
    adjusted_dfs.append(adjusted_df)

# Concatenate all adjusted dataframes
df_adjusted = pd.concat(adjusted_dfs, ignore_index=True)

# Save the combined dataframe to a CSV file
df_adjusted.to_csv('D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\personal_color_season_adjusted.csv', index=False)
