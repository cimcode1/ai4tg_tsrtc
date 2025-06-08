import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import streamlit as st

class DummyForecaster:
    """Dummy forecasting model for TGSRTC demand prediction"""
    
    def __init__(self):
        self.model_accuracy = {
            'r2_score': 0.87,
            'rmse': 12.5,
            'mae': 9.2,
            'mape': 8.1
        }
    
    def predict_demand(self, route, date, time_slot, external_factors=None):
        """Predict passenger demand for a specific route, date, and time slot"""
        
        # Base demand based on route popularity
        route_multipliers = {
            'Hyderabad-Warangal': 1.2,
            'Secunderabad-Nizamabad': 1.1,
            'Karimnagar-Adilabad': 0.9,
            'Nalgonda-Miryalaguda': 0.8,
            'Rangareddy-Khammam': 1.0,
            'Mahbubnagar-Jadcherla': 0.7,
            'Medak-Sangareddy': 0.6,
            'Nizamabad-Kamareddy': 0.8,
            'Warangal-Hanamkonda': 0.9,
            'Khammam-Bhadrachalam': 0.7,
            'Adilabad-Mancherial': 0.6,
            'Suryapet-Kodad': 0.8
        }
        
        base_demand = 120 * route_multipliers.get(route, 1.0)
        
        # Time slot adjustments
        time_multipliers = {
            '06:00-08:00': 1.3,
            '08:00-10:00': 1.5,
            '10:00-12:00': 0.9,
            '12:00-14:00': 0.7,
            '14:00-16:00': 0.8,
            '16:00-18:00': 1.3,
            '18:00-20:00': 1.5,
            '20:00-22:00': 0.7
        }
        
        base_demand *= time_multipliers.get(time_slot, 1.0)
        
        # Day of week effect
        if date.weekday() >= 5:  # Weekend
            base_demand *= 0.8
        
        # External factors
        if external_factors:
            if external_factors.get('weather') == 'Heavy Rain':
                base_demand *= 0.6
            elif external_factors.get('weather') == 'Hot':
                base_demand *= 0.9
            
            if external_factors.get('is_festival', False):
                base_demand *= 1.4
            
            if external_factors.get('is_holiday', False):
                base_demand *= 1.2
        
        # Add some randomness to simulate model uncertainty
        predicted_demand = max(0, int(base_demand * random.uniform(0.85, 1.15)))
        
        # Calculate confidence bounds
        confidence_range = predicted_demand * 0.15
        lower_bound = max(0, int(predicted_demand - confidence_range))
        upper_bound = int(predicted_demand + confidence_range)
        
        return {
            'predicted_passengers': predicted_demand,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'confidence': random.uniform(0.82, 0.94)
        }
    
    def generate_forecast_data(self, routes, days_ahead=7):
        """Generate forecast data for multiple routes and days"""
        
        forecast_data = []
        start_date = datetime.now().date() + timedelta(days=1)
        
        time_slots = [
            "06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00",
            "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00"
        ]
        
        for day in range(days_ahead):
            forecast_date = start_date + timedelta(days=day)
            
            # Simulate external factors for this date
            external_factors = {
                'weather': np.random.choice(['Clear', 'Cloudy', 'Light Rain'], p=[0.6, 0.3, 0.1]),
                'is_festival': random.random() < 0.05,
                'is_holiday': random.random() < 0.08,
                'mahalaxmi_active': True
            }
            
            for route in routes:
                for slot in time_slots:
                    prediction = self.predict_demand(
                        route, forecast_date, slot, external_factors
                    )
                    
                    # Calculate required buses
                    bus_capacity = 50  # Average capacity
                    required_buses = max(1, int(np.ceil(prediction['predicted_passengers'] / bus_capacity)))
                    
                    # Generate alerts
                    alerts = []
                    if prediction['predicted_passengers'] > bus_capacity:
                        if prediction['predicted_passengers'] > bus_capacity * 1.2:
                            alerts.append({
                                'type': 'critical',
                                'message': f'High demand expected: {prediction["predicted_passengers"]} passengers. Add {required_buses-1} extra bus(es).'
                            })
                        else:
                            alerts.append({
                                'type': 'warning',
                                'message': f'Moderate demand spike: Consider adding 1 extra bus.'
                            })
                    
                    forecast_data.append({
                        'Date': forecast_date,
                        'Route': route,
                        'Time_Slot': slot,
                        'Predicted_Passengers': prediction['predicted_passengers'],
                        'Lower_Bound': prediction['lower_bound'],
                        'Upper_Bound': prediction['upper_bound'],
                        'Confidence': prediction['confidence'],
                        'Required_Buses': required_buses,
                        'Weather': external_factors['weather'],
                        'Is_Festival': external_factors['is_festival'],
                        'Is_Holiday': external_factors['is_holiday'],
                        'Alerts': alerts
                    })
        
        return pd.DataFrame(forecast_data)
    
    def get_route_recommendations(self, forecast_data):
        """Generate operational recommendations based on forecast"""
        
        recommendations = []
        
        # Group by route and find high-demand periods
        route_analysis = forecast_data.groupby('Route').agg({
            'Predicted_Passengers': ['mean', 'max', 'sum'],
            'Required_Buses': 'max'
        }).round(2)
        
        route_analysis.columns = ['avg_passengers', 'peak_passengers', 'total_passengers', 'max_buses_needed']
        
        for route in route_analysis.index:
            route_data = route_analysis.loc[route]
            
            if route_data['peak_passengers'] > 100:
                recommendations.append({
                    'route': route,
                    'type': 'capacity',
                    'priority': 'high' if route_data['peak_passengers'] > 120 else 'medium',
                    'message': f"Peak demand of {int(route_data['peak_passengers'])} passengers expected. Ensure {int(route_data['max_buses_needed'])} buses available.",
                    'action': f"Deploy {int(route_data['max_buses_needed'])} buses during peak hours"
                })
            
            if route_data['avg_passengers'] < 40:
                recommendations.append({
                    'route': route,
                    'type': 'optimization',
                    'priority': 'low',
                    'message': f"Low average demand ({int(route_data['avg_passengers'])} passengers). Consider frequency optimization.",
                    'action': "Review schedule frequency for cost optimization"
                })
        
        # Time slot recommendations
        time_analysis = forecast_data.groupby('Time_Slot')['Predicted_Passengers'].mean()
        peak_slots = time_analysis[time_analysis > time_analysis.mean() * 1.2].index.tolist()
        
        if peak_slots:
            recommendations.append({
                'route': 'All Routes',
                'type': 'scheduling',
                'priority': 'high',
                'message': f"Peak demand during {', '.join(peak_slots)}. Ensure adequate fleet deployment.",
                'action': "Increase bus frequency during identified peak hours"
            })
        
        return recommendations
    
    def get_model_performance_metrics(self):
        """Return model performance metrics"""
        return self.model_accuracy
    
    def get_feature_importance(self):
        """Return dummy feature importance for model interpretability"""
        return {
            'Time_Slot': 0.35,
            'Route': 0.25,
            'Day_of_Week': 0.15,
            'Weather': 0.10,
            'Is_Festival': 0.08,
            'Mahalaxmi_Active': 0.07
        }

@st.cache_data
def get_forecaster():
    """Get cached forecaster instance"""
    return DummyForecaster()

def generate_alerts(forecast_data, threshold_high=100, threshold_critical=120):
    """Generate operational alerts based on forecast data"""
    
    alerts = []
    
    # High demand alerts
    high_demand = forecast_data[forecast_data['Predicted_Passengers'] > threshold_high]
    for _, row in high_demand.iterrows():
        alert_type = 'critical' if row['Predicted_Passengers'] > threshold_critical else 'warning'
        alerts.append({
            'type': alert_type,
            'route': row['Route'],
            'time_slot': row['Time_Slot'],
            'date': row['Date'],
            'message': f"High demand forecast: {row['Predicted_Passengers']} passengers",
            'action': f"Deploy {row['Required_Buses']} buses"
        })
    
    # Weather-based alerts
    weather_issues = forecast_data[forecast_data['Weather'].isin(['Heavy Rain', 'Hot'])]
    for _, row in weather_issues.iterrows():
        alerts.append({
            'type': 'info',
            'route': row['Route'],
            'time_slot': row['Time_Slot'],
            'date': row['Date'],
            'message': f"Weather alert: {row['Weather']} conditions expected",
            'action': "Monitor demand and adjust capacity if needed"
        })
    
    return alerts