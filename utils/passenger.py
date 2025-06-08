import pandas as pd

def load_weekday_trends_data(csv_path=None):
    # Load data
    if csv_path:
        df = pd.read_csv(csv_path)
    else:
        df = pd.read_csv("Wl-Upl_final.csv")  # default path

    # Map integers to weekday names
    day_map = {
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
        3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
    }
    df['Weekday'] = df['Day Type'].map(day_map)

    # Extract year from date
    df['Year'] = pd.to_datetime(df['date']).dt.year

    # Group and sum
    grouped = df.groupby(['Year', 'Weekday'])['total_passengers'].sum().reset_index()

    # Keep only 2022–2024
    grouped = grouped[grouped['Year'].isin([2022, 2023, 2024])]

    # Ensure weekday order
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    grouped['Weekday'] = pd.Categorical(grouped['Weekday'], categories=weekday_order, ordered=True)

    pie_data = grouped.groupby('Weekday')['total_passengers'].sum().reset_index()

    # Calculate percentage share
    total = pie_data['total_passengers'].sum()
    pie_data['percentage'] = round(100 * pie_data['total_passengers'] / total, 2)

    return grouped.sort_values(['Weekday', 'Year']), pie_data

