import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Sample data in a DataFrame

positie = input("positie = ")
wedstrijd_count = input("wedstrijd count = ")

def file_read(folder_path):
    df_plot = pd.DataFrame()
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Read CSV file into a DataFrame
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            name = filename[:2]

            last_row = df.iloc[-1].copy()
            last_row['name'] = name

            # Append the last row to df_plot
            df_plot = df_plot.append(last_row, ignore_index=True)

    return df_plot




def plot(df, titel):

    # Grouped bar chart
    fig, ax = plt.subplots()

    color1 = '#F7FF00'
    color2 = '#000000'
    width = 0.35  # Width of each bar
    opacity = 0.6  # Opacity of bars
    labels = df.index
    x = np.arange(len(labels))

    # Plotting the grouped bars
    p1 = ax.bar(x - width/2, df['Eerste Helft'], width, alpha=opacity, color=color2, label='Eerste Helft')
    p2 = ax.bar(x + width/2, df['Tweede Helft'], width, alpha=opacity, color=color1, label='Tweede Helft')

    # Set the x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels)


    # Set the axis labels and title
    ax.set_xlabel('Positie')
    ax.set_ylabel('Afstand (m)')
    ax.set_title(titel)

    ax.bar_label(p1, padding=3, fmt="%.2f")
    ax.bar_label(p2, padding=3, fmt="%.2f")

    # Add legend
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def data_cleaning(df,name, intensity):
    if intensity == 'sprinting':
        df_cleaned = pd.DataFrame()
        #print(df['Afstand > 25km/h per sessie'])
        df_cleaned[f'{name}'] = df['Afstand > 25km/h per sessie']
        df_cleaned['name'] = df['name']

    elif intensity == 'HIR':
        df_cleaned = pd.DataFrame()
        df_cleaned[f'{name}'] = df['Afstand 20-24,9km/h per sessie (m)']
        df_cleaned['name'] = df['name']

    else:
        error = 'somthing went wrong'
        return error

    df_cleaned.set_index('name', inplace=True)
    return df_cleaned

folder_path_eerste = f"C:/Users/Simon/Documents/Casus-CSV/juist/{positie}/eerste"
folder_path_tweede = f"C:/Users/Simon/Documents/Casus-CSV/juist/{positie}/tweede"

df_eerste = file_read(folder_path_eerste)
df_tweede = file_read(folder_path_tweede)


#plot sprinting
#titel = f"Aantal meters sprinten (>25km/u) tijdens een wedstrijd {positie} \n (aantal wedstrijden = {wedstrijd_count})"
titel = f"Aantal meters sprinten (>25km/u) tijdens alle wedstrijden \n (aantal wedstrijden = {wedstrijd_count})"
df_to_plot_eerste_s = data_cleaning(df_eerste,name='Eerste Helft', intensity='sprinting')
df_to_plot_tweede_s = data_cleaning(df_tweede,name='Tweede Helft', intensity='sprinting')
df_to_plot_s = pd.merge(df_to_plot_eerste_s,df_to_plot_tweede_s, on='name')
plot(df_to_plot_s, titel)

#plot HIR
#titel = f"Aantal meters HIR (20-24,9km/u) tijdens een wedstrijd {positie} \n (aantal wedstrijden = {wedstrijd_count})"
titel = f"Aantal meters HIR (20-24,9km/u) tijdens alle wedstrijden \n (aantal wedstrijden = {wedstrijd_count})"
df_to_plot_eerste_h = data_cleaning(df_eerste,name='Eerste Helft', intensity='HIR')
df_to_plot_tweede_h = data_cleaning(df_tweede,name='Tweede Helft', intensity='HIR')
df_to_plot_h = pd.merge(df_to_plot_eerste_h,df_to_plot_tweede_h, on='name')
plot(df_to_plot_h, titel)
