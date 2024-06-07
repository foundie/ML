import pandas as pd
import matplotlib.pyplot as plt

# Load the adjusted colors CSV files for each season
spring_light_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\spring_light_adjusted_colors.csv')
spring_clear_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\spring_clear_adjusted_colors.csv')
spring_warm_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\spring_warm_adjusted_colors.csv')
summer_light_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\summer_light_adjusted_colors.csv')
summer_soft_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\summer_soft_adjusted_colors.csv')
summer_cool_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\summer_cool_adjusted_colors.csv')
autumn_deep_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\autumn_deep_adjusted_colors.csv')
autumn_soft_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\autumn_soft_adjusted_colors.csv')
autumn_warm_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\autumn_warm_adjusted_colors.csv')
winter_deep_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\winter_deep_adjusted_colors.csv')
winter_clear_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\winter_clear_adjusted_colors.csv')
winter_cool_df = pd.read_csv(r'D:\!KULIAH!\Semester 6\Bangkit Course\Belajar Analisi Data dengan Python\Submission\ML\Color Analysis\winter_cool_adjusted_colors.csv')

# Create a function to plot colors
def plot_colors(df, season_name):
    colors = df[['R', 'G', 'B']].values / 255.0  # Normalize RGB values to range [0, 1]
    plt.figure(figsize=(8, 2))
    for i, color in enumerate(colors):
        plt.fill_between([i, i + 1], 0, 1, color=color)
    plt.title(season_name)
    plt.axis('off')
    plt.show()

# Plot colors for each season
plot_colors(spring_light_df, 'Spring Light')
plot_colors(spring_clear_df, 'Spring Clear')
plot_colors(spring_warm_df, 'Spring Warm')
plot_colors(summer_light_df, 'Summer Light')
plot_colors(summer_soft_df, 'Summer Soft')
plot_colors(summer_cool_df, 'Summer Cool')
plot_colors(autumn_deep_df, 'Autumn Deep')
plot_colors(autumn_soft_df, 'Autumn Soft')
plot_colors(autumn_warm_df, 'Autumn Warm')
plot_colors(winter_deep_df, 'Winter Deep')
plot_colors(winter_clear_df, 'Winter Clear')
plot_colors(winter_cool_df, 'Winter Cool')
