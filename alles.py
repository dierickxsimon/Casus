import pandas as pd
import matplotlib.pyplot as plt
import os




# Create an empty DataFrame with the specified columns
df_plot = pd.DataFrame()
positie = input("positie = ")
wedstrijd_count = input("wedstrijd count = ")

folder_path = f"C:/Users/Simon/Documents/Casus-CSV/juist/{positie}/totaal"

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        print(filename)
        print(folder_path)
        # Read CSV file into a DataFrame
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        #session_count = len(df.index)
        #session_count = session_count - 1
        # Prompt the user for the name
        name = filename[:2]
        print(name)

        #name = name + f'(n={session_count})'

        # Add the name to the last row of the DataFrame
        last_row = df.iloc[-1].copy()
        last_row['name'] = name

        # Append the last row to df_plot
        df_plot = df_plot.append(last_row, ignore_index=True)
        print(df_plot)

data = df_plot


def create_acc_df(df):
    columns_delete = ['Afstand 0-6,9km/h per sessie', 'Afstand 7-9,9km/h per sessie', 'Afstand 10-13,9km/h per sessie',
                      'Afstand 14-19,9km/h per sessie', 'Afstand 20-24,9km/h per sessie (m)',
                      'Afstand > 25km/h per sessie']
    df = df.drop(columns=columns_delete)

    return df


def create_distance_df(df):
    columns_delete = ['Decceleration >3m/s²', 'Decceleration 2m/s²-3m/s²', 'Acceleration 2m/s²-3m/s²',
                      'Acceleration >3m/s²']
    df = df.drop(columns=columns_delete)

    return df


def create_relatice_df(df):

    df['Average Distance (Session) (m)'] = df['Afstand 0-6,9km/h per sessie'] + df[
        'Afstand 7-9,9km/h per sessie'] + df['Afstand 10-13,9km/h per sessie'] + df[
                                                    'Afstand 14-19,9km/h per sessie'] + df[
                                                    'Afstand 20-24,9km/h per sessie (m)'] + df[
                                                    'Afstand > 25km/h per sessie']
    df['Afstand 0-6,9km/h per sessie'] = df['Afstand 0-6,9km/h per sessie'] / df[
        'Average Distance (Session) (m)']
    df['Afstand 7-9,9km/h per sessie'] = df['Afstand 7-9,9km/h per sessie'] / df[
        'Average Distance (Session) (m)']
    df['Afstand 10-13,9km/h per sessie'] = df['Afstand 10-13,9km/h per sessie'] / df[
        'Average Distance (Session) (m)']
    df['Afstand 14-19,9km/h per sessie'] = df['Afstand 14-19,9km/h per sessie'] / df[
        'Average Distance (Session) (m)']
    df['Afstand 20-24,9km/h per sessie (m)'] = df['Afstand 20-24,9km/h per sessie (m)'] / df[
        'Average Distance (Session) (m)']
    df['Afstand > 25km/h per sessie'] = df['Afstand > 25km/h per sessie'] / df[
        'Average Distance (Session) (m)']

    columns_delete = ['Decceleration >3m/s²', 'Decceleration 2m/s²-3m/s²', 'Acceleration 2m/s²-3m/s²',
                      'Acceleration >3m/s²', 'Average Distance (Session) (m)']
    df = df.drop(columns=columns_delete)

    return df


def plot(df, colors, graph):
    columns_delete = ['Session Count']
    df = df.drop(columns=columns_delete)
    df.set_index('name', inplace=True)
    # Create the stacked bar chart with custom colors
    ax = df.plot(kind='barh', stacked=True, color=colors)

    # Add values to the bars
    for container in ax.containers:
        if graph == 'r':
            widths = [rect.get_width() for rect in container]
            percentages = [round(width * 100, 1) for width in widths]
            labels = [f"{percentage}%" for percentage in percentages]
            ax.bar_label(container, labels=labels, label_type='center', fontsize=8)
            #titel = f"Gemiddelde relatieve afstand tijdens een wedstrijd {positie} \n" \
             #       f"(aantal wedstrijden = {wedstrijd_count})"
            titel = f"Gemiddelde relatieve afstand tijdens alle wedstrijden \n" \
                     f"(aantal wedstrijden = {wedstrijd_count})"
            ax.set_xlabel('Percentage van TD')
        elif graph == 'd':
            ax.bar_label(container, label_type='center', fontsize=8)
            #titel = f"Gemiddelde absolute afstand tijdens een wedstrijd {positie} \n" \
             #       f"(aantal wedstrijden = {wedstrijd_count})"
            titel = f"Gemiddelde absolute afstand tijdens alle wedstrijden \n" \
                    f"(aantal wedstrijden = {wedstrijd_count})"
            ax.set_xlabel('Afstand (m)')

        elif graph == 'a':
            ax.bar_label(container, label_type='center', fontsize=8)
            ax.set_xlabel('Aantal versnellingen en vertragingen')
            #titel = f"Gemiddelde aantal acc en decc tijdens een wedstrijd {positie} \n" \
             #       f"(aantal wedstrijden = {wedstrijd_count})"
            titel = f"Gemiddelde aantal acc en decc tijdens alle wedstrijden \n" \
                    f"(aantal wedstrijden = {wedstrijd_count})"
        else:
            print(100*'*' + "error")
            titel = "error"



    ax.set_ylabel('positie')
    #titel = input('mooie titel: ')
    ax.set_title(titel)
    ax.legend().set_visible(True)

    # Show the chart
    plt.show()




#plot acc
acc_df = create_acc_df(data)
print(acc_df)
colors = ['#E70000','#FF7070', '#BDF560', '#90E800']
plot(acc_df,colors,graph='a')


#plot distance
dist_df = create_distance_df(data)
print(dist_df)
colors = ['#fef9e7', '#fcf3cf', '#f7dc6f', '#f1c40f', '#b7950b', '#7d6608']
plot(dist_df,colors,graph='d')

#plot relatice distance
rela_df = create_relatice_df(data)
print(rela_df)
plot(rela_df, colors, graph='r')
