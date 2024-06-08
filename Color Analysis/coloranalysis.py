import pandas as pd
import numpy as np

# Function to adjust brightness
def adjust_brightness(color, factor):
    return np.clip(color * factor, 0, 255).astype(int)

# Load the original CSV file
df = pd.read_csv('D:/!KULIAH!/Semester 6/Bangkit Course/Belajar Analisi Data dengan Python/Submission/ML/Color Analysis/personal_color_season.csv', delimiter=';')

# Print column names for debugging
print("Columns:", df.columns)

# Check if 'season' column exists
if 'season' not in df.columns:
    raise KeyError("'season' column not found in the CSV file.")

# Define brightness factors for new chroma choices
brightness_factors = [0.8, 0.9, 1.1, 1.2]

# Function to calculate similarity (Euclidean distance)
def calculate_similarity(original, adjusted):
    return np.sqrt(np.sum((original - adjusted) ** 2, axis=1))

# Recommender system function
def recommend_season(user_brightness_factor):
    # Adjust the colors based on user-selected brightness factor
    user_adjusted_colors = adjust_brightness(df[['R', 'G', 'B']].values, user_brightness_factor)
    
    # Calculate similarity with original colors
    similarities = calculate_similarity(df[['R', 'G', 'B']].values, user_adjusted_colors)
    
    # Calculate match percentage
    max_distance = np.sqrt(3 * (255 ** 2))  # Maximum possible distance in RGB space
    match_percentage = (1 - similarities / max_distance) * 100
    
    # Append the match percentage to the dataframe
    df['match_percentage'] = match_percentage
    
    # Calculate average match percentage for each season
    season_match = df.groupby('season')['match_percentage'].mean().reset_index()
    
    return season_match

# User input for brightness factor
user_brightness_factor = float(input("Enter the chroma brightness factor (e.g., 0.8, 0.9, 1.1, 1.2): "))

# Get the recommendation
season_recommendation = recommend_season(user_brightness_factor)

# Display the recommendation
print("Seasonal Match Percentage Based on Your Chroma Brightness Choice:")
print(season_recommendation)
