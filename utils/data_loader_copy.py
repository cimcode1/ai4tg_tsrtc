import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_historical_data(start_date, end_date):
    """
    Load historical data for the given date range
    In a real application, this would load data from a database or API
    """
    if not start_date or not end_date:
        # Default to last 30 days if dates not provided
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    
    # Create a date range
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    
    # Create dummy data
    np.random.seed(42)  # For reproducibility
    
    # Base demand with weekly seasonality
    base_demand = np.array([100, 110, 105, 115, 120, 130, 125] * ((len(date_range) // 7) + 1))[:len(date_range)]
    
    # Add some trend
    trend = np.linspace(0, 20, len(date_range))
    
    # Add some noise
    noise = np.random.normal(0, 5, len(date_range))
    
    # Combine components
    demand = base_demand + trend + noise
    
    # Create seasonal component (higher in middle of date range)
    days_total = (end_date - start_date).days
    seasonal = 15 * np.sin(np.linspace(0, np.pi, len(date_range)))
    
    # Final demand
    final_demand = demand + seasonal
    
    # Create DataFrame
    df = pd.DataFrame({
        "ds": date_range,
        "value": final_demand,
        "upper": final_demand + np.random.uniform(5, 15, len(date_range)),
        "lower": final_demand - np.random.uniform(5, 15, len(date_range))
    })
    
    return df

def load_forecast_data(start_date, end_date):
    """
    Load forecast data for the given date range
    In a real application, this would load data from a forecasting service
    """
    if not start_date or not end_date:
        # Default to next 30 days if dates not provided
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)
    
    # Create a date range
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    
    # Create dummy forecast data
    np.random.seed(43)  # Different seed for forecast
    
    # Base forecast with weekly seasonality
    base_forecast = np.array([105, 115, 110, 120, 125, 135, 130] * ((len(date_range) // 7) + 1))[:len(date_range)]
    
    # Add some trend
    trend = np.linspace(0, 25, len(date_range))
    
    # Add some noise (less noise in the near future, more in the distant future)
    noise_scale = np.linspace(2, 10, len(date_range))
    noise = np.random.normal(0, noise_scale, len(date_range))
    
    # Combine components
    forecast = base_forecast + trend + noise
    
    # Add seasonal component
    days_total = (end_date - start_date).days
    seasonal = 20 * np.sin(np.linspace(0, np.pi, len(date_range)))
    
    # Final forecast
    final_forecast = forecast + seasonal
    
    # Create uncertainty intervals (wider as we go further into the future)
    uncertainty = np.linspace(5, 20, len(date_range))
    
    # Create DataFrame
    df = pd.DataFrame({
        "ds": date_range,
        "value": final_forecast,
        "upper": final_forecast + uncertainty,
        "lower": final_forecast - uncertainty
    })
    
    return df

def get_historical_metrics(df):
    """
    Calculate metrics from historical data
    """
    return {
        "avg_demand": df["value"].mean(),
        "demand_change": 5.2,  # Dummy value for demo
        "peak_hours": "18:00-21:00",
        "peak_change": 3.8,
        "seasonal_index": 1.25,
        "seasonal_change": 2.3,
        "weather_impact": 12.5,
        "weather_change": -1.5
    }

def get_forecast_metrics(df):
    """
    Calculate metrics from forecast data
    """
    return {
        "avg_demand": df["value"].mean(),
        "demand_change": 7.5,  # Dummy value for demo
        "peak_hours": "18:00-21:00",
        "peak_change": 4.2,
        "confidence_level": 95,
        "confidence_change": 2.0,
        "fleet_efficiency": 87.5,
        "efficiency_change": 3.2
    }