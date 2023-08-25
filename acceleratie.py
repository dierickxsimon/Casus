import pandas as pd
import matplotlib.pyplot as plt
import os


folder_path = "C:/Users/Simon/Documents/Casus-CSV/acc-dec/4-4-2"

# Create an empty DataFrame with the specified columns
df_plot = pd.DataFrame()


for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Read CSV file into a DataFrame
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        session_count = df['Session Count'].sum()
        session_count = session_count - df['Session Count'].iloc[-1]
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

#df_plot['Decceleration >-3m/s²'] = df_plot['Decceleration >3m/s²']
#df_plot['Decceleration -2m/s² - -3m/s²'] = df_plot['Decceleration 2m/s²-3m/s²']

df_plot.set_index('name', inplace=True)

columns_delete = ['Session Count', 'Name']
df_plot = df_plot.drop(columns=columns_delete)

df_plot.to_excel("C:/Users/Simon/Documents/Casus-CSV-Leeg/execel.xlsx")








# Define custom colors
colors = ['#E70000','#FF7070', '#BDF560', '#90E800']



# Create the stacked bar chart with custom colors
ax = df_plot.plot(kind='barh', stacked=True, color=colors)

# Add values to the bars
for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=8)


# Customize the chart


ax.set_xlabel('Aantal versnellingen en vertragingen')
ax.set_ylabel('positie')
titel = input('mooie titel: ')
ax.set_title(titel)
ax.legend().set_visible(False)

# Show the chart
plt.show()

