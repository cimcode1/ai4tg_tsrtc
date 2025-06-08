import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

from utils.data_loader import (
    load_dummy_data, get_routes, get_time_slots,
    filter_data_by_routes
)
from utils.visualizer import create_forecast_chart, create_capacity_planning_chart
from utils.forecaster import get_forecaster, generate_alerts
from components.sidebar import render_forecast_sidebar, render_footer_sidebar

# Configure page
st.set_page_config(
    page_title="Forecast & Alerts - TGSRTC Analytics",
    page_icon="🔮",
    layout="wide"
)
# Add date range selector
today = datetime.now().date()
default_end_date = today + timedelta(days=7)

with st.sidebar:
    st.markdown("### 📅 Forecast Time Range")
    start_date = st.date_input("Start Date", today)
    end_date = st.date_input("End Date", default_end_date)
    
    if start_date > end_date:
        st.error("Error: Start date must be before end date")
        st.stop()
    
    forecast_days = (end_date - start_date).days + 1
    time_slots = get_time_slots()
    start_time = st.selectbox("Start Time", time_slots)
    end_time = st.selectbox("End Time", time_slots)
    
    if time_slots.index(start_time) > time_slots.index(end_time):
        st.error("Error: Start time must be before end time")
        st.stop()
# Custom CSS for dark theme
st.markdown("""
<style>
    .forecast-card {
        background: linear-gradient(135deg, #4A1F5C 0%, #6A2C70 100%);
        border: 1px solid #BA68C8;
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }
    .forecast-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    .forecast-card h3 {
        color: #BA68C8;
        margin-bottom: 0.5rem;
    }
    .forecast-card h2 {
        color: #FFFFFF;
        margin: 0.5rem 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .forecast-card p {
        color: #B0B0B0;
        margin: 0;
    }
    .alert-critical {
        background: linear-gradient(135deg, #4A1E2A 0%, #5D2631 100%);
        border-left: 4px solid #FF6B93;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .alert-warning {
        background: linear-gradient(135deg, #4A3728 0%, #5D3F2E 100%);
        border-left: 4px solid #FF9F43;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .alert-info {
        background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
        border-left: 4px solid #64B5F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .suggestion-card {
        background: linear-gradient(135deg, #1B4332 0%, #2D5A3D 100%);
        border: 1px solid #40C767;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .forecast-table {
        background: #2D2D2D;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔮 Demand Forecast & Fleet Optimization")
    st.markdown("**AI-powered demand forecasting with actionable fleet recommendations**")
    
    # Load data and forecaster
    historical_data = load_dummy_data()
    forecaster = get_forecaster()
    
    # Render sidebar and get configuration
    sidebar_config = render_forecast_sidebar()
    render_footer_sidebar()
    
    # Generate forecast data
    if sidebar_config['selected_routes']:
        forecast_data = forecaster.generate_forecast_data(
            sidebar_config['selected_routes'], 
            sidebar_config['forecast_days']
        )
        
        # Apply manual adjustments if any
        if sidebar_config['demand_adjustment'] != 0:
            adjustment_factor = 1 + (sidebar_config['demand_adjustment'] / 100)
            forecast_data['Predicted_Passengers'] = (forecast_data['Predicted_Passengers'] * adjustment_factor).round().astype(int)
            forecast_data['Lower_Bound'] = (forecast_data['Lower_Bound'] * adjustment_factor).round().astype(int)
            forecast_data['Upper_Bound'] = (forecast_data['Upper_Bound'] * adjustment_factor).round().astype(int)
        
        # Display forecast overview
        display_forecast_overview(forecast_data)
        
        # Display detailed forecasts
        display_detailed_forecast(forecast_data, historical_data, sidebar_config)
        
        # Display alerts and recommendations
        display_alerts_and_recommendations(
            forecast_data, 
            forecaster, 
            sidebar_config['warning_threshold'], 
            sidebar_config['critical_threshold']
        )
        
        # Display capacity planning
        display_capacity_planning(forecast_data, sidebar_config)
        
    else:
        st.warning("Please select at least one route to generate forecasts.")

def display_forecast_overview(forecast_data):
    """Display forecast overview metrics"""
    st.markdown("## 📊 Forecast Overview")
    
    # Calculate summary metrics
    total_predicted = forecast_data['Predicted_Passengers'].sum()
    avg_confidence = forecast_data['Confidence'].mean()
    peak_demand = forecast_data['Predicted_Passengers'].max()
    total_buses_needed = forecast_data['Required_Buses'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="forecast-card">
            <h3>👥 Total Predicted</h3>
            <h2>{total_predicted:,}</h2>
            <p>Passengers (Next {forecast_data['Date'].nunique()} days)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="forecast-card">
            <h3>🎯 Avg Confidence</h3>
            <h2>{avg_confidence:.1%}</h2>
            <p>Prediction Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="forecast-card">
            <h3>📈 Peak Demand</h3>
            <h2>{peak_demand:,}</h2>
            <p>Highest Single Period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="forecast-card">
            <h3>🚌 Buses Needed</h3>
            <h2>{total_buses_needed:,}</h2>
            <p>Total Fleet Requirement</p>
        </div>
        """, unsafe_allow_html=True)

def display_detailed_forecast(forecast_data, historical_data, sidebar_config):
    """Display detailed forecast charts and tables"""
    st.markdown("## 📈 Detailed Forecast Analysis")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Trend View", "📋 Tabular View", "🗓️ Calendar View"])
    
    with tab1:
        # Route selection for trend view
        selected_route_trend = st.selectbox(
            "Select Route for Trend Analysis",
            options=forecast_data['Route'].unique()
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Historical vs forecast trend
            route_forecast = forecast_data[forecast_data['Route'] == selected_route_trend]
            route_historical = historical_data[historical_data['Route'] == selected_route_trend].tail(30)  # Last 30 days
            
            # Aggregate by date
            forecast_daily = route_forecast.groupby('Date')['Predicted_Passengers'].sum().reset_index()
            historical_daily = route_historical.groupby('Date')['Total_Passengers'].sum().reset_index()
            
            # Create combined chart
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_daily['Date'],
                y=historical_daily['Total_Passengers'],
                mode='lines+markers',
                name='Historical',
                line=dict(color='#FF8A65')
            ))
            
            # Forecast data
            fig.add_trace(go.Scatter(
                x=forecast_daily['Date'],
                y=forecast_daily['Predicted_Passengers'],
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#BA68C8', dash='dash')
            ))
            
            fig.update_layout(
                title=f"📈 {selected_route_trend}: Historical vs Forecast",
                xaxis_title="Date",
                yaxis_title="Daily Passengers",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='#FF8A65'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Time slot breakdown for selected route
            route_forecast = forecast_data[forecast_data['Route'] == selected_route_trend]
            
            slot_summary = route_forecast.groupby('Time_Slot').agg({
                'Predicted_Passengers': 'mean',
                'Required_Buses': 'max'
            }).reset_index()
            
            slot_summary = slot_summary.sort_values('Predicted_Passengers', ascending=True)
            
            slot_fig = px.bar(
                slot_summary,
                x='Predicted_Passengers',
                y='Time_Slot',
                orientation='h',
                title=f"⏰ Average Demand by Time Slot - {selected_route_trend}",
                color='Predicted_Passengers',
                color_continuous_scale="Viridis"
            )
            slot_fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                title_font_color='#FF8A65'
            )
            st.plotly_chart(slot_fig, use_container_width=True)
    
    with tab2:
        # Detailed forecast table
        st.markdown("### 📋 Detailed Forecast Data")
        
        # Route filter for table
        table_route = st.selectbox(
            "Filter by Route",
            options=['All Routes'] + list(forecast_data['Route'].unique()),
            key="table_route"
        )
        
        display_data = forecast_data.copy()
        if table_route != 'All Routes':
            display_data = display_data[display_data['Route'] == table_route]
        
        # Format the data for display
        display_data['Date'] = pd.to_datetime(display_data['Date']).dt.strftime('%Y-%m-%d')
        display_data['Confidence'] = (display_data['Confidence'] * 100).round(1).astype(str) + '%'
        
        # Select relevant columns
        table_columns = [
            'Date', 'Route', 'Time_Slot', 'Predicted_Passengers', 
            'Lower_Bound', 'Upper_Bound', 'Confidence', 'Required_Buses', 'Weather'
        ]
        
        st.dataframe(
            display_data[table_columns].round(0),
            use_container_width=True,
            height=400
        )
        
        # Download forecast data
        csv_data = display_data[table_columns].to_csv(index=False)
        st.download_button(
            label="📥 Download Forecast Data",
            data=csv_data,
            file_name=f"tgsrtc_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab3:
        # Calendar view of demand
        st.markdown("### 🗓️ Calendar View - Daily Demand Forecast")
        
        # Aggregate forecast by date
        daily_forecast = forecast_data.groupby(['Date', 'Route'])['Predicted_Passengers'].sum().reset_index()
        
        # Create pivot for heatmap
        calendar_data = daily_forecast.pivot(index='Route', columns='Date', values='Predicted_Passengers')
        
        calendar_fig = px.imshow(
            calendar_data,
            labels=dict(x="Date", y="Route", color="Predicted Passengers"),
            title="🗓️ Daily Demand Forecast Calendar",
            color_continuous_scale="RdYlBu_r",
            aspect="auto"
        )
        calendar_fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#FF8A65'
        )
        st.plotly_chart(calendar_fig, use_container_width=True)

def display_alerts_and_recommendations(forecast_data, forecaster, warning_threshold, critical_threshold):
    """Display alerts and operational recommendations"""
    st.markdown("## 🚨 Alerts & Recommendations")
    
    # Generate alerts
    alerts = generate_alerts(forecast_data, warning_threshold, critical_threshold)
    recommendations = forecaster.get_route_recommendations(forecast_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 Active Alerts")
        
        if alerts:
            for alert in alerts[:10]:  # Show top 10 alerts
                alert_class = f"alert-{alert['type']}"
                icon = "🚨" if alert['type'] == 'critical' else "⚠️" if alert['type'] == 'warning' else "ℹ️"
                
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>{icon} {alert['route']} - {alert['time_slot']}</strong><br>
                    📅 {alert['date']}<br>
                    📝 {alert['message']}<br>
                    🎯 <em>Action: {alert['action']}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No alerts generated for current forecast period.")
    
    with col2:
        st.markdown("### 💡 Operational Recommendations")
        
        if recommendations:
            for rec in recommendations[:8]:  # Show top 8 recommendations
                priority_color = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                
                st.markdown(f"""
                <div class="suggestion-card">
                    <strong>{priority_color.get(rec['priority'], '⚪')} {rec['route']}</strong><br>
                    📝 {rec['message']}<br>
                    🎯 <em>Recommended Action: {rec['action']}</em>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific recommendations at this time.")
    
    # Summary statistics
    st.markdown("### 📊 Alert Summary")
    
    alert_summary = pd.DataFrame(alerts)
    if not alert_summary.empty:
        alert_counts = alert_summary['type'].value_counts()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            critical_count = alert_counts.get('critical', 0)
            st.metric("🚨 Critical Alerts", critical_count)
        
        with col2:
            warning_count = alert_counts.get('warning', 0)
            st.metric("⚠️ Warning Alerts", warning_count)
        
        with col3:
            info_count = alert_counts.get('info', 0)
            st.metric("ℹ️ Info Alerts", info_count)

def display_capacity_planning(forecast_data, sidebar_config):
    """Display capacity planning visualization and recommendations"""
    st.markdown("## 🚌 Fleet Capacity Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Capacity planning matrix
        capacity_fig = create_capacity_planning_chart(forecast_data)
        st.plotly_chart(capacity_fig, use_container_width=True)
    
    with col2:
        # Fleet utilization forecast
        fleet_data = forecast_data.groupby(['Route', 'Date']).agg({
            'Predicted_Passengers': 'sum',
            'Required_Buses': 'max'
        }).reset_index()
        
        # Calculate utilization assuming standard fleet allocation
        fleet_data['Standard_Fleet'] = 3  # Assume 3 buses per route as standard
        fleet_data['Utilization'] = (fleet_data['Required_Buses'] / fleet_data['Standard_Fleet']) * 100
        
        util_forecast_fig = px.line(
            fleet_data,
            x='Date',
            y='Utilization',
            color='Route',
            title="📈 Fleet Utilization Forecast",
            markers=True
        )
        util_forecast_fig.add_hline(y=100, line_dash="dash", line_color="#FF6B93", annotation_text="100% Utilization")
        util_forecast_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color='#FF8A65'
        )
        st.plotly_chart(util_forecast_fig, use_container_width=True)
    
    # Fleet optimization recommendations
    st.markdown("### 🎯 Fleet Optimization Insights")
    
    # Calculate fleet requirements by route
    fleet_requirements = forecast_data.groupby('Route').agg({
        'Required_Buses': ['max', 'mean'],
        'Predicted_Passengers': 'sum'
    }).round(2)
    
    fleet_requirements.columns = ['Peak_Buses_Required', 'Avg_Buses_Required', 'Total_Passengers']
    fleet_requirements = fleet_requirements.sort_values('Peak_Buses_Required', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🚌 Fleet Requirements by Route")
        st.dataframe(fleet_requirements, use_container_width=True)
    
    with col2:
        st.markdown("#### 💡 Optimization Opportunities")
        
        # Identify optimization opportunities
        high_demand_routes = fleet_requirements[fleet_requirements['Peak_Buses_Required'] > 2].index.tolist()
        low_demand_routes = fleet_requirements[fleet_requirements['Avg_Buses_Required'] < 1.5].index.tolist()
        
        if high_demand_routes:
            st.markdown("**🔴 High Demand Routes (Consider Additional Fleet):**")
            for route in high_demand_routes[:5]:
                peak_buses = fleet_requirements.loc[route, 'Peak_Buses_Required']
                st.markdown(f"- {route}: Peak {peak_buses:.0f} buses needed")
        
        if low_demand_routes:
            st.markdown("**🟢 Optimization Candidates (Review Frequency):**")
            for route in low_demand_routes[:5]:
                avg_buses = fleet_requirements.loc[route, 'Avg_Buses_Required']
                st.markdown(f"- {route}: Avg {avg_buses:.1f} buses utilized")
    
    # Export capacity planning data
    st.markdown("### 📊 Export Planning Data")
    
    planning_data = forecast_data.groupby(['Route', 'Date', 'Time_Slot']).agg({
        'Predicted_Passengers': 'first',
        'Required_Buses': 'first',
        'Weather': 'first'
    }).reset_index()
    
    planning_csv = planning_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Capacity Planning Data",
        data=planning_csv,
        file_name=f"tgsrtc_capacity_plan_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()