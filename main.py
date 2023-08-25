import pandas as pd
import matplotlib.pyplot as plt
import os


relative = True
acc = True

folder_path = "C:/Users/Simon/Documents/Casus-CSV/4-4-2"

# Create an empty DataFrame with the specified columns
df_plot = pd.DataFrame()


for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Read CSV file into a DataFrame
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        session_count = len(df.index)
        session_count = session_count - 1
        # Prompt the user for the name
        name = filename[:2]

        name = name + f'(n={session_count})'

        # Add the name to the last row of the DataFrame
        last_row = df.iloc[-1].copy()
        last_row['name'] = name

        # Append the last row to df_plot
        df_plot = df_plot.append(last_row, ignore_index=True)


# Display the final DataFrame
#print(df_plot.columns)
#with pd.option_context('display.max_rows', None,
#                       'display.max_columns', None,
#                       'display.precision', 3,
#                       ):
#    print(df_plot)

if acc:
    # Define custom colors
    colors = ['#E70000', '#FF7070', '#BDF560', '#90E800']
    columns_delete = ['Afstand 0-6,9km/h per sessie', 'Afstand 7-9,9km/h per sessie', 'Afstand 10-13,9km/h per sessie', 'Afstand 14-19,9km/h per sessie', 'Afstand 20-24,9km/h per sessie (m)','Afstand > 25km/h per sessie']
    df_plot = df_plot.drop(columns=columns_delete)

else:
    # Define custom colors
    colors = ['#fef9e7', '#fcf3cf', '#f7dc6f', '#f1c40f', '#b7950b', '#7d6608']
    columns_delete = ['Decceleration >3m/s²', 'Decceleration 2m/s²-3m/s²', 'Acceleration 2m/s²-3m/s²', 'Acceleration >3m/s²']
    df_plot = df_plot.drop(columns=columns_delete)

    if relative:
        df_plot['Average Distance (Session) (m)'] = df_plot['Afstand 0-6,9km/h per sessie'] + df_plot['Afstand 7-9,9km/h per sessie'] + df_plot['Afstand 10-13,9km/h per sessie']  + df_plot ['Afstand 14-19,9km/h per sessie'] + df_plot['Afstand 20-24,9km/h per sessie (m)'] + df_plot['Afstand > 25km/h per sessie']
        df_plot['Afstand 0-6,9km/h per sessie'] = df_plot['Afstand 0-6,9km/h per sessie'] / df_plot['Average Distance (Session) (m)']
        df_plot['Afstand 7-9,9km/h per sessie'] = df_plot['Afstand 7-9,9km/h per sessie'] / df_plot['Average Distance (Session) (m)']
        df_plot['Afstand 10-13,9km/h per sessie'] = df_plot['Afstand 10-13,9km/h per sessie'] / df_plot['Average Distance (Session) (m)']
        df_plot['Afstand 14-19,9km/h per sessie'] = df_plot['Afstand 14-19,9km/h per sessie'] / df_plot['Average Distance (Session) (m)']
        df_plot['Afstand 20-24,9km/h per sessie (m)'] = df_plot['Afstand 20-24,9km/h per sessie (m)'] / df_plot['Average Distance (Session) (m)']
        df_plot['Afstand > 25km/h per sessie'] = df_plot['Afstand > 25km/h per sessie'] / df_plot['Average Distance (Session) (m)']

# Specify the desired order of values in the 'name' column
name_order = ['CD', 'FB', 'CM', 'WM', 'FW']
df_plot.to_excel("C:/Users/Simon/Documents/Casus-CSV-Leeg/execel.xlsx")

# Order the DataFrame based on the 'name' column
df_plot = df_plot.sort_values(by='name', key=lambda x: x.map({v: i for i, v in enumerate(name_order)}))

columns_delete = ['Average Distance (Session) (m)', 'Session Count']
df_plot = df_plot.drop(columns=columns_delete)
# Set the index column
df_plot.set_index('name', inplace=True)


# Create the stacked bar chart with custom colors
ax = df_plot.plot(kind='barh', stacked=True, color=colors)

# Add values to the bars
for container in ax.containers:
    if relative:
        widths = [rect.get_width() for rect in container]
        percentages = [round(width * 100, 1) for width in widths]
        labels = [f"{percentage}%" for percentage in percentages]
        ax.bar_label(container, labels=labels, label_type='center', fontsize=8)
    else:
        ax.bar_label(container, label_type='center', fontsize=8)

# Customize the chart
if relative:
    ax.set_xlabel('Percentage van TD')
else:
    ax.set_xlabel('Afstand (m)')
ax.set_ylabel('positie')
titel = input('mooie titel: ')
ax.set_title(titel)
ax.legend().set_visible(False)

# Show the chart
plt.show()

