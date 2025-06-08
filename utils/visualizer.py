import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st

# Dark theme colors
COLORS = {
    'primary': '#FF8A65',      # Muted orange
    'secondary': '#64B5F6',    # Soft blue
    'success': '#40C767',      # Muted green
    'warning': '#FF9F43',      # Soft amber
    'danger': '#FF6B93',       # Soft red
    'info': '#17a2b8',         # Teal
    'light': '#f8f9fa',        # Light gray
    'dark': '#2D2D2D',         # Dark gray
    'purple': '#BA68C8',       # Soft purple
    'cyan': '#4DD0E1'          # Soft cyan
}

def create_demand_heatmap(data, route_filter=None):
    """Create a demand heatmap showing route vs date patterns"""
    
    # Filter data if routes specified
    if route_filter:
        data = data[data['Route'].isin(route_filter)]
    
    # Aggregate data by date and route
    heatmap_data = data.groupby(['Date', 'Route'])['Total_Passengers'].sum().reset_index()
    
    # Pivot for heatmap
    pivot_data = heatmap_data.pivot(index='Route', columns='Date', values='Total_Passengers')
    
    fig = px.imshow(
        pivot_data,
        labels=dict(x="Date", y="Route", color="Passengers"),
        title="📊 Passenger Demand Heatmap by Route and Date",
        color_continuous_scale="RdYlBu_r",
        aspect="auto"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400
    )
    
    return fig

def create_trend_chart(data, metric='Total_Passengers', split_by=None):
    """Create trend chart for various metrics"""
    
    if split_by:
        # Group by date and split_by column
        trend_data = data.groupby(['Date', split_by])[metric].sum().reset_index()
        
        fig = px.line(
            trend_data, 
            x='Date', 
            y=metric, 
            color=split_by,
            title=f"📈 {metric.replace('_', ' ').title()} Trend by {split_by.replace('_', ' ').title()}",
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success']]
        )
    else:
        # Simple trend by date
        trend_data = data.groupby('Date')[metric].sum().reset_index()
        
        fig = px.line(
            trend_data, 
            x='Date', 
            y=metric,
            title=f"📈 {metric.replace('_', ' ').title()} Trend",
            color_discrete_sequence=[COLORS['primary']]
        )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400,
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title(),
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )
    
    return fig

def create_passenger_split_chart(data):
    """Create pie chart showing paid vs free passenger split"""
    
    total_paid = data['Paid_Passengers'].sum()
    total_free = data['Free_Passengers'].sum()
    
    fig = px.pie(
        values=[total_paid, total_free],
        names=['Paid Passengers', 'Free Passengers (Mahalaxmi)'],
        title="🎯 Passenger Type Distribution",
        color_discrete_sequence=[COLORS['primary'], COLORS['success']]
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=12,
        textfont_color='white'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400
    )
    
    return fig

def create_utilization_chart(data, chart_type='bar'):
    """Create utilization chart by route"""
    
    util_data = data.groupby('Route')['Utilization_Percent'].mean().reset_index()
    util_data = util_data.sort_values('Utilization_Percent', ascending=False)
    
    # Add status categories
    util_data['Status'] = util_data['Utilization_Percent'].apply(
        lambda x: 'Overload' if x > 100 else 'Excellent' if x > 85 else 'Good'
    )
    
    if chart_type == 'bar':
        fig = px.bar(
            util_data,
            x='Route',
            y='Utilization_Percent',
            color='Status',
            title="🚌 Average Route Utilization",
            color_discrete_map={
                'Excellent': COLORS['success'],
                'Good': COLORS['warning'],
                'Overload': COLORS['danger']
            }
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        
    else:  # scatter
        fig = px.scatter(
            util_data,
            x='Route',
            y='Utilization_Percent',
            size='Utilization_Percent',
            color='Status',
            title="🚌 Route Utilization Distribution",
            color_discrete_map={
                'Excellent': COLORS['success'],
                'Good': COLORS['warning'],
                'Overload': COLORS['danger']
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
    
    # Add reference line at 100%
    fig.add_hline(y=100, line_dash="dash", line_color=COLORS['danger'], 
                  annotation_text="100% Capacity")
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400,
        xaxis_title="Route",
        yaxis_title="Utilization %",
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )
    
    return fig

def create_time_slot_analysis(data):
    """Create analysis of demand by time slots"""
    
    slot_data = data.groupby('Time_Slot').agg({
        'Total_Passengers': 'mean',
        'Utilization_Percent': 'mean'
    }).reset_index()
    
    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add passenger count
    fig.add_trace(
        go.Bar(
            x=slot_data['Time_Slot'],
            y=slot_data['Total_Passengers'],
            name='Avg Passengers',
            marker_color=COLORS['primary']
        ),
        secondary_y=False,
    )
    
    # Add utilization line
    fig.add_trace(
        go.Scatter(
            x=slot_data['Time_Slot'],
            y=slot_data['Utilization_Percent'],
            mode='lines+markers',
            name='Avg Utilization %',
            line=dict(color=COLORS['danger'], width=3)
        ),
        secondary_y=True,
    )
    
    # Update axes
    fig.update_xaxes(title_text="⏰ Time Slot", gridcolor='#444')
    fig.update_yaxes(title_text="Average Passengers", secondary_y=False, gridcolor='#444')
    fig.update_yaxes(title_text="Average Utilization %", secondary_y=True, gridcolor='#444')
    
    fig.update_layout(
        title_text="⏰ Demand and Utilization by Time Slot",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400
    )
    
    return fig

def create_weather_impact_chart(data):
    """Create chart showing weather impact on demand"""
    
    weather_data = data.groupby('Weather').agg({
        'Total_Passengers': 'mean',
        'Utilization_Percent': 'mean'
    }).reset_index()
    
    weather_data = weather_data.sort_values('Total_Passengers', ascending=True)
    
    fig = px.bar(
        weather_data,
        x='Total_Passengers',
        y='Weather',
        orientation='h',
        title="🌤️ Weather Impact on Average Demand",
        color='Total_Passengers',
        color_continuous_scale="RdYlBu_r"
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=300,
        xaxis_title="Average Passengers",
        yaxis_title="Weather Condition",
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )
    
    return fig

def create_forecast_chart(historical_data, forecast_data):
    """Create forecast visualization with confidence intervals"""
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=historical_data['Date'],
        y=historical_data['Total_Passengers'],
        mode='lines',
        name='Historical',
        line=dict(color=COLORS['primary'])
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_data['Date'],
        y=forecast_data['Predicted_Passengers'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color=COLORS['danger'], dash='dash')
    ))
    
    # Confidence interval
    if 'Upper_Bound' in forecast_data.columns:
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Upper_Bound'],
            mode='lines',
            name='Upper Bound',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Lower_Bound'],
            mode='lines',
            name='Confidence Interval',
            fill='tonexty',
            fillcolor='rgba(255,138,101,0.2)',
            line=dict(width=0)
        ))
    
    fig.update_layout(
        title="🔮 Demand Forecast with Historical Comparison",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400,
        xaxis_title="Date",
        yaxis_title="Passengers",
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )
    
    return fig

def create_revenue_analysis(data):
    """Create revenue analysis visualization"""
    
    revenue_data = data.groupby('Date').agg({
        'Revenue': 'sum',
        'Paid_Passengers': 'sum',
        'Free_Passengers': 'sum'
    }).reset_index()
    
    # Calculate revenue per passenger
    revenue_data['Revenue_Per_Passenger'] = revenue_data['Revenue'] / revenue_data['Paid_Passengers']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Revenue trend
    fig.add_trace(
        go.Scatter(
            x=revenue_data['Date'],
            y=revenue_data['Revenue'],
            mode='lines',
            name='Daily Revenue (₹)',
            line=dict(color=COLORS['success'])
        ),
        secondary_y=False,
    )
    
    # Revenue per passenger
    fig.add_trace(
        go.Scatter(
            x=revenue_data['Date'],
            y=revenue_data['Revenue_Per_Passenger'],
            mode='lines',
            name='Revenue per Passenger (₹)',
            line=dict(color=COLORS['info'], dash='dot')
        ),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Date", gridcolor='#444')
    fig.update_yaxes(title_text="Total Revenue (₹)", secondary_y=False, gridcolor='#444')
    fig.update_yaxes(title_text="Revenue per Passenger (₹)", secondary_y=True, gridcolor='#444')
    
    fig.update_layout(
        title_text="💰 Revenue Analysis",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=400
    )
    
    return fig

def create_capacity_planning_chart(data):
    """Create capacity planning visualization"""
    
    capacity_data = data.groupby(['Route', 'Time_Slot']).agg({
        'Predicted_Passengers': 'mean',
        'Required_Buses': 'first'
    }).reset_index()
    
    # Calculate utilization
    capacity_data['Utilization_Percent'] = (capacity_data['Predicted_Passengers'] / 50) * 100  # Assuming 50 seat capacity
    
    # Identify overutilized slots
    capacity_data['Status'] = capacity_data['Utilization_Percent'].apply(
        lambda x: 'Critical' if x > 120 else 'Overload' if x > 100 else 'Normal'
    )
    
    fig = px.scatter(
        capacity_data,
        x='Time_Slot',
        y='Route',
        size='Utilization_Percent',
        color='Status',
        title="🚌 Capacity Planning Matrix",
        color_discrete_map={
            'Critical': COLORS['danger'],
            'Overload': COLORS['warning'],
            'Normal': COLORS['success']
        }
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=10, color='white'),
        title_font_size=16,
        title_font_color=COLORS['primary'],
        height=500,
        xaxis_title="Time Slot",
        yaxis_title="Route",
        xaxis=dict(gridcolor='#444'),
        yaxis=dict(gridcolor='#444')
    )
    
    return fig