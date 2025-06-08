import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_dummy_data, get_routes, get_time_slots
from utils.visualizer import create_demand_heatmap, create_trend_chart
from components.sidebar import render_main_sidebar, render_footer_sidebar

# Configure page
st.set_page_config(
    page_title="TGSRTC Analytics Dashboard",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

from PIL import Image

# Optional: Add logo
# Create a two-column layout
col1, col2 = st.columns([1, 4])

# Logo in first column
with col1:
    logo1 = Image.open("tsrtc-logo-compressed-image5x.jpg")
    st.image(logo1, width=150)

# Title in second column
with col2:
    st.markdown("""
        <h1 style='color: #FF4B4B; margin-top: 20px;'>
            🚌 AI-Driven Fleet Optimization
        </h1>
        <h3 style='color: #FFFFFF; margin-top: -10px;'>
            for Telangana State Road Transport Corporation (TGSRTC)
        </h3>
    """, unsafe_allow_html=True)

st.markdown("---")

# Summary box
st.markdown("""
<div style="background-color: #262730; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
    <h4 style='color: #F0F0F0;'>📌 Overview</h4>
    <p style='color: #DDDDDD;'>
        TGSRTC operates a vast fleet that faces frequent mismatches between bus supply and passenger demand. This dashboard showcases an AI-powered approach to forecast demand, optimize fleet allocation, and improve operational efficiency while accounting for fare-paying and Mahalaxmi (free) passengers.
    </p>
</div>
""", unsafe_allow_html=True)

# Problem statement
with st.expander("🚨 Problem Statement"):
    st.markdown("""
    - ❌ Underutilized and overcrowded buses on different routes
    - ❌ Missed revenue opportunities
    - ❌ Static scheduling with no dynamic response to real-time data
    - ❌ Inadequate modeling of free-ticket (Mahalaxmi) passengers
    - ❌ Poor responsiveness to external factors like holidays or weather
    """)

# Solution section
with st.expander("💡 Proposed AI Solution"):
    st.markdown("""
    - 🔍 **Demand Forecasting** using ML models (XGBoost, LSTM)
    - 📈 **Revenue-Aware Optimization** for bus allocation
    - ☁️ **Integration with External Data** like weather, holidays, and events
    - 📊 **Interactive Dashboard** to visualize trends and insights
    """)

# Call to Action
st.markdown("""
<div style="text-align: center; padding-top: 20px;">
    <h4 style="color: #33FF99;">Use the sidebar to explore trend analysis, forecasting tools, and optimization insights</h4>
</div>
""", unsafe_allow_html=True)