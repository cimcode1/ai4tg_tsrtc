import streamlit as st
from datetime import datetime, timedelta
from utils.data_loader import get_routes, get_time_slots



def render_main_sidebar():
    """Render the main dashboard sidebar with navigation and branding"""
    
    # TGSRTC Branding
    st.sidebar.image("./logo-white_xperancy.png", width=250)
    
    

def render_eda_sidebar():
    """Render sidebar for selecting trend analysis type"""

    st.sidebar.markdown("### 📈 Explore EDA Trends")

    eda_view_option = st.sidebar.selectbox(
        "🔍 Select EDA Viewpoint",
        options=["Passenger & Ticket Insights", "Temporal & Holiday Trends", "Revenue Channels & Bus Deployment", "External Factors & Derived Data"],
        index=0,
        help="Select the type of historical trend to analyze"
    )

    return {
        'eda_view_option': eda_view_option
    }


    


def render_historical_sidebar():
    """Render sidebar for selecting trend analysis type"""

    st.sidebar.markdown("### 📈 Historical Trend Type")

    trend_view_option = st.sidebar.selectbox(
        "🔍 Choose a Trend",
        options=["Passenger Trends", "Revenue Trends", "Weather Trends", "Holiday Impact"],
        index=0,
        help="Select the type of historical trend to analyze"
    )

    return {
        'trend_view_option': trend_view_option
    }

def render_forecast_sidebar():
    """Render Forecast sidebar controls"""
    
    st.sidebar.markdown("### 🎛️ Forecast Configuration")
    
    # Forecast horizon
    forecast_days = st.sidebar.slider(
        "📅 Forecast Horizon (Days)",
        min_value=1,
        max_value=7,
        value=3,
        help="Number of days to forecast ahead"
    )
    
    # Route selection
    routes = get_routes()
    selected_routes = st.sidebar.multiselect(
        "🚌 Select Routes for Forecast",
        options=routes,
        default=routes[:5],
        help="Choose routes to generate forecasts for"
    )
    
    # Alert sensitivity
    alert_sensitivity = st.sidebar.selectbox(
        "🚨 Alert Sensitivity",
        options=["Low", "Medium", "High"],
        index=1,
        help="Set the sensitivity level for generating alerts"
    )
    
    # Capacity thresholds
    st.sidebar.markdown("### ⚙️ Capacity Thresholds")
    warning_threshold = st.sidebar.slider(
        "⚠️ Warning Level (%)", 
        80, 100, 90,
        help="Utilization percentage to trigger warnings"
    )
    critical_threshold = st.sidebar.slider(
        "🚨 Critical Level (%)", 
        100, 150, 120,
        help="Utilization percentage to trigger critical alerts"
    )
    
   
    
    # Export options
    st.sidebar.markdown("### 📊 Export Options")
    export_format = st.sidebar.selectbox(
        "Export Format",
        ["CSV", "Excel", "PDF Report"],
        help="Choose format for exporting forecast data"
    )
    
    include_confidence_intervals = st.sidebar.checkbox(
        "Include Confidence Intervals", 
        value=True
    )
    
    return {
        'forecast_days': forecast_days,
        'selected_routes': selected_routes,
        'alert_sensitivity': alert_sensitivity,
        'warning_threshold': warning_threshold,
        'critical_threshold': critical_threshold,
        'export_format': export_format,
        'include_confidence_intervals': include_confidence_intervals
    }

def render_footer_sidebar():
    """Render footer information in sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #B0B0B0; padding: 1rem; font-size: 0.8rem;'>
        <p style='margin: 0;'>🚌 TGSRTC Analytics</p>
        <p style='margin: 0;'>Version 2.0</p>
        <p style='margin: 0;'>© 2024 TGSRTC</p>
    </div>
    """, unsafe_allow_html=True)