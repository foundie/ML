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

# Dictionary to store dataframes for each season
season_dfs = {
    'spring_light': pd.DataFrame(),
    'spring_clear': pd.DataFrame(),
    'spring_warm': pd.DataFrame(),
    'summer_light': pd.DataFrame(),
    'summer_soft': pd.DataFrame(),
    'summer_cool': pd.DataFrame(),
    'autumn_deep': pd.DataFrame(),
    'autumn_soft': pd.DataFrame(),
    'autumn_warm': pd.DataFrame(),
    'winter_deep': pd.DataFrame(),
    'winter_clear': pd.DataFrame(),
    'winter_cool': pd.DataFrame(),
}

# Process each row in the dataframe
for index, row in df.iterrows():
    season = row['season'].replace(' ', '_').lower()
    original_rgb = np.array([row['R'], row['G'], row['B']])

    for factor in brightness_factors:
        new_rgb = adjust_brightness(original_rgb, factor)
        new_row = {
            'season': row['season'],
            'R': new_rgb[0],
            'G': new_rgb[1],
            'B': new_rgb[2]
        }
        season_dfs[season] = season_dfs[season]._append(new_row, ignore_index=True)

# Save each season dataframe to a separate CSV file
for season, season_df in season_dfs.items():
    season_df.to_csv(f'd:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\{season}_adjusted_colors.csv', index=False)
