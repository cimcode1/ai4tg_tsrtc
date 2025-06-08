import streamlit as st
from datetime import datetime, timedelta
from utils.data_loader import get_routes, get_time_slots



def get_route_selector():
    """Dropdown to choose route and return corresponding CSV path"""
    st.sidebar.markdown("### 🛣️ Select Route")
    route_options = {
        "Warangal - Uppal": "Wl-Upl_final.csv",
        "49 M Route": "49M Route_final.csv"
    }
    selected_route = st.sidebar.selectbox("Route", list(route_options.keys()))
    return selected_route, route_options[selected_route]


def render_main_sidebar():
    """Render the main dashboard sidebar with navigation and branding"""
    
    # TGSRTC Branding
    st.sidebar.image("./logo-white_xperancy.png", width=250)
    
    

def render_eda_sidebar():
    selected_route, csv_path = get_route_selector()

    st.sidebar.markdown("### 📈 Explore EDA Trends")

    eda_view_option = st.sidebar.selectbox(
        "🔍 Select EDA Viewpoint",
        options=[
            "Passenger & Ticket Insights",
            "Temporal & Holiday Trends",
            "Revenue Channels & Bus Deployment",
            "External Factors & Derived Data"
        ],
        index=0
    )

    return {
        'eda_view_option': eda_view_option,
        'selected_route': selected_route,
        'csv_path': csv_path
    }


    


def render_historical_sidebar():
    selected_route, csv_path = get_route_selector()

    st.sidebar.markdown("### 📈 Historical Trend Type")

    trend_view_option = st.sidebar.selectbox(
        "🔍 Choose a Trend",
        options=["Passenger Trends", "Revenue Trends", "Weather Trends", "Holiday Impact"],
        index=0
    )

    return {
        'trend_view_option': trend_view_option,
        'selected_route': selected_route,
        'csv_path': csv_path
    }


def render_modelling_sidebar():
    selected_route, csv_path = get_route_selector()

    st.sidebar.markdown("### 🧠 Modeling Trend Type")

    trend_view_option = st.sidebar.selectbox(
        "🔍 Choose a Trend",
        options=["Passenger Trends", "Revenue Trends", "Weather Trends", "Holiday Impact"],
        index=0
    )

    return {
        'trend_view_option': trend_view_option,
        'selected_route': selected_route,
        'csv_path': csv_path
    }


def render_forecast_sidebar():
    selected_route, csv_path = get_route_selector()

    st.sidebar.markdown("### 🎛️ Forecast Configuration")

    # Rest of your sliders & settings...
    forecast_days = st.sidebar.slider("📅 Forecast Horizon (Days)", 1, 7, 3)
    routes = get_routes()
    selected_routes = st.sidebar.multiselect("🚌 Select Routes for Forecast", routes, default=routes[:5])
    alert_sensitivity = st.sidebar.selectbox("🚨 Alert Sensitivity", ["Low", "Medium", "High"], index=1)
    warning_threshold = st.sidebar.slider("⚠️ Warning Level (%)", 80, 100, 90)
    critical_threshold = st.sidebar.slider("🚨 Critical Level (%)", 100, 150, 120)
    export_format = st.sidebar.selectbox("Export Format", ["CSV", "Excel", "PDF Report"])
    include_confidence_intervals = st.sidebar.checkbox("Include Confidence Intervals", value=True)

    return {
        'forecast_days': forecast_days,
        'selected_routes': selected_routes,
        'alert_sensitivity': alert_sensitivity,
        'warning_threshold': warning_threshold,
        'critical_threshold': critical_threshold,
        'export_format': export_format,
        'include_confidence_intervals': include_confidence_intervals,
        'selected_route': selected_route,
        'csv_path': csv_path
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