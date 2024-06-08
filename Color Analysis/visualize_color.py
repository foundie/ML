import pandas as pd
import matplotlib.pyplot as plt

# Load the original and adjusted CSV files
df_original = pd.read_csv('D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\personal_color_season.csv', delimiter=';')
df_adjusted = pd.read_csv('D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\personal_color_season_adjusted.csv')

# Concatenate both dataframes
df = pd.concat([df_original, df_adjusted])

# Define a function to convert RGB values to hex color code
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Convert RGB values to hex color code
df['Color'] = df[['R', 'G', 'B']].apply(rgb_to_hex, axis=1)

# Group colors by season and sort them by hue
seasons = df['season'].unique()

plt.figure(figsize=(14, 6 * len(seasons)))

for i, season in enumerate(seasons, start=1):
    plt.subplot(len(seasons), 1, i)
    df_season = df[df['season'] == season]
    colors = df_season[['R', 'G', 'B']].values / 255.0  # Normalize RGB values to range [0, 1]
    colors = sorted(colors, key=lambda x: (x[0], x[1], x[2]))  # Sort colors by hue
    for j, color in enumerate(colors):
        plt.fill_between([j, j + 1], 0, 1, color=color)
    plt.title(season)
    plt.axis('off')

plt.tight_layout()
plt.show()
