import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import streamlit as st

@st.cache_data
def load_dummy_data():
    """Generate comprehensive dummy data for TGSRTC analytics"""
    
    # Define routes
    routes = [
        "Hyderabad-Warangal", "Secunderabad-Nizamabad", "Karimnagar-Adilabad",
        "Nalgonda-Miryalaguda", "Rangareddy-Khammam", "Mahbubnagar-Jadcherla",
        "Medak-Sangareddy", "Nizamabad-Kamareddy", "Warangal-Hanamkonda",
        "Khammam-Bhadrachalam", "Adilabad-Mancherial", "Suryapet-Kodad"
    ]
    
    # Generate date range (last 6 months + next 7 days)
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now() + timedelta(days=7)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Time slots
    time_slots = [
        "06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00",
        "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00"
    ]
    
    data = []
    
    for date in dates:
        is_weekend = date.weekday() >= 5
        is_festival = random.random() < 0.05  # 5% chance of festival
        is_holiday = random.random() < 0.08   # 8% chance of holiday
        
        # Weather simulation
        weather_conditions = ['Clear', 'Cloudy', 'Light Rain', 'Heavy Rain', 'Hot']
        weather = np.random.choice(weather_conditions, p=[0.4, 0.3, 0.15, 0.05, 0.1])
        
        # Mahalaxmi scheme effect (higher free passengers after certain date)
        mahalaxmi_active = date >= datetime(2023, 6, 1)
        
        for route in routes:
            route_popularity = random.uniform(0.7, 1.3)  # Route-specific multiplier
            
            for slot in time_slots:
                # Base demand calculation
                base_demand = random.randint(80, 200)
                
                # Apply modifiers
                if is_weekend:
                    base_demand *= 0.8  # Less demand on weekends
                if is_festival or is_holiday:
                    base_demand *= 1.4  # More demand during festivals
                if weather == 'Heavy Rain':
                    base_demand *= 0.6  # Less travel during heavy rain
                elif weather == 'Hot':
                    base_demand *= 0.9
                
                # Peak hours effect
                if slot in ["08:00-10:00", "18:00-20:00"]:
                    base_demand *= 1.5
                elif slot in ["06:00-08:00", "16:00-18:00"]:
                    base_demand *= 1.3
                elif slot in ["12:00-14:00", "20:00-22:00"]:
                    base_demand *= 0.7
                
                # Apply route popularity
                total_demand = int(base_demand * route_popularity)
                
                # Split between paid and free passengers
                if mahalaxmi_active:
                    free_passengers = int(total_demand * random.uniform(0.25, 0.45))
                else:
                    free_passengers = int(total_demand * random.uniform(0.05, 0.15))
                
                paid_passengers = total_demand - free_passengers
                
                # Bus capacity and utilization
                bus_capacity = random.choice([45, 50, 55])  # Different bus types
                utilization = min((total_demand / bus_capacity) * 100, 150)  # Can exceed 100%
                
                data.append({
                    'Date': date.date(),
                    'Route': route,
                    'Time_Slot': slot,
                    'Total_Passengers': total_demand,
                    'Paid_Passengers': paid_passengers,
                    'Free_Passengers': free_passengers,
                    'Bus_Capacity': bus_capacity,
                    'Utilization_Percent': utilization,
                    'Weather': weather,
                    'Is_Weekend': is_weekend,
                    'Is_Festival': is_festival,
                    'Is_Holiday': is_holiday,
                    'Mahalaxmi_Active': mahalaxmi_active,
                    'Revenue': paid_passengers * random.uniform(25, 45)  # Revenue per paid passenger
                })
    
    return pd.DataFrame(data)

@st.cache_data
def get_routes():
    """Get list of all routes"""
    return [
        "Hyderabad-Warangal", "Secunderabad-Nizamabad", "Karimnagar-Adilabad",
        "Nalgonda-Miryalaguda", "Rangareddy-Khammam", "Mahbubnagar-Jadcherla",
        "Medak-Sangareddy", "Nizamabad-Kamareddy", "Warangal-Hanamkonda",
        "Khammam-Bhadrachalam", "Adilabad-Mancherial", "Suryapet-Kodad"
    ]

@st.cache_data
def get_time_slots():
    """Get list of all time slots"""
    return [
        "06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00",
        "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00"
    ]

@st.cache_data
def get_weather_data():
    """Get weather impact analysis data"""
    return {
        'Clear': {'demand_multiplier': 1.0, 'reliability': 0.95},
        'Cloudy': {'demand_multiplier': 0.95, 'reliability': 0.92},
        'Light Rain': {'demand_multiplier': 0.85, 'reliability': 0.88},
        'Heavy Rain': {'demand_multiplier': 0.6, 'reliability': 0.75},
        'Hot': {'demand_multiplier': 0.9, 'reliability': 0.90}
    }

@st.cache_data
def get_festival_calendar():
    """Get festival and special events calendar"""
    festivals = [
        {'name': 'Diwali', 'date': '2023-11-12', 'impact': 'High'},
        {'name': 'Dussehra', 'date': '2023-10-24', 'impact': 'High'},
        {'name': 'Ganesh Chaturthi', 'date': '2023-09-19', 'impact': 'Medium'},
        {'name': 'Independence Day', 'date': '2023-08-15', 'impact': 'Medium'},
        {'name': 'Raksha Bandhan', 'date': '2023-08-31', 'impact': 'Low'},
        {'name': 'Ugadi', 'date': '2024-04-09', 'impact': 'High'},
        {'name': 'Ram Navami', 'date': '2024-04-17', 'impact': 'Medium'}
    ]
    return pd.DataFrame(festivals)

@st.cache_data 
def get_mahalaxmi_impact_data():
    """Get Mahalaxmi scheme impact statistics"""
    return {
        'launch_date': '2023-06-01',
        'beneficiaries_monthly': [0, 0, 0, 0, 0, 45000, 52000, 58000, 63000, 67000, 71000, 75000],
        'revenue_impact_percent': -15.5,
        'ridership_increase_percent': 23.2,
        'routes_most_impacted': [
            'Hyderabad-Warangal', 'Secunderabad-Nizamabad', 'Karimnagar-Adilabad'
        ]
    }

def filter_data_by_date_range(data, start_date, end_date):
    """Filter data by date range"""
    data['Date'] = pd.to_datetime(data['Date'])
    return data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

def filter_data_by_routes(data, selected_routes):
    """Filter data by selected routes"""
    if selected_routes:
        return data[data['Route'].isin(selected_routes)]
    return data

def get_summary_metrics(data):
    """Calculate summary metrics from the data"""
    total_passengers = data['Total_Passengers'].sum()
    total_revenue = data['Revenue'].sum()
    avg_utilization = data['Utilization_Percent'].mean()
    free_passenger_percent = (data['Free_Passengers'].sum() / total_passengers) * 100
    
    return {
        'total_passengers': total_passengers,
        'total_revenue': total_revenue,
        'avg_utilization': avg_utilization,
        'free_passenger_percent': free_passenger_percent,
        'active_routes': data['Route'].nunique(),
        'peak_utilization': data['Utilization_Percent'].max(),
        'total_trips': len(data)
    }