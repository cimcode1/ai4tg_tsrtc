import pandas as pd

def get_monthly_fare_summary(csv_path=r"C:\Users\L\Downloads\TGSRTC_CSV\Wl-Upl_final.csv"):
    # Load data
    df = pd.read_csv(csv_path)

    # Ensure 'date' column is datetime
    df['date'] = pd.to_datetime(df['date'])

    # Extract year and month
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month

    # Group by year and month and sum total_fare
    monthly_fare = df.groupby(['Year', 'Month'])['total_fare'].sum().reset_index()

    # Add month name
    monthly_fare['Month_Name'] = pd.to_datetime(monthly_fare['Month'], format='%m').dt.strftime('%B')

    # Sort the result
    monthly_fare = monthly_fare.sort_values(['Year', 'Month'])

    return monthly_fare


