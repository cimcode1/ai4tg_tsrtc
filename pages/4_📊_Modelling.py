import streamlit as st

st.set_page_config(
    page_title="Exploratory Data Analysis - TGSRTC Analytics",
    page_icon="📊",
    layout="wide"
)




st.title("📈 Actual vs Predicted – Modeling Results (Date-wise)")

import pandas as pd
import plotly.graph_objects as go

# Load data
df_actual = pd.read_csv("Wl-Upl_final.csv", parse_dates=["date"])
df_model_passenger = pd.read_csv("no_of_passengers.csv_684590184c070ad092a36edb.csv", parse_dates=["date"])
df_model_fare = pd.read_csv("total_revenue.csv_68459479ad6bfad9f7a36f2a.csv", parse_dates=["date"])

# Merge model predictions
df = df_actual.copy()
df["Year"] = df["date"].dt.year

df = df.merge(
    df_model_passenger[["date", "total_passengers"]].rename(columns={"total_passengers": "passenger_model"}),
    on="date", how="left"
)
df = df.merge(
    df_model_fare[["date", "total_fare"]].rename(columns={"total_fare": "fare_model"}),
    on="date", how="left"
)

# Dropdown to select year
years = sorted(df["Year"].unique())
selected_year = st.selectbox("Select Year", years, index=len(years) - 1)

df_year = df[df["Year"] == selected_year].sort_values("date")

# Passengers Chart
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_year["date"], y=df_year["total_passengers"], mode='lines+markers', name="Actual Passengers", line=dict(color="#1f77b4")))
fig1.add_trace(go.Scatter(x=df_year["date"], y=df_year["passenger_model"], mode='lines+markers', name="Predicted Passengers", line=dict(color="#ff7f0e")))
fig1.update_layout(
    title=f"🧍 Total Passengers – Actual vs Predicted ({selected_year})",
    xaxis_title="Date",
    yaxis_title="Total Passengers",
    template="plotly_dark",
    height=500,
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", yanchor="top")
)
st.plotly_chart(fig1, use_container_width=True)

# Fare Chart
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_year["date"], y=df_year["total_fare"], mode='lines+markers', name="Actual Fare", line=dict(color="#2ca02c")))
fig2.add_trace(go.Scatter(x=df_year["date"], y=df_year["fare_model"], mode='lines+markers', name="Predicted Fare", line=dict(color="#d62728")))
fig2.update_layout(
    title=f"💰 Total Fare – Actual vs Predicted ({selected_year})",
    xaxis_title="Date",
    yaxis_title="Total Fare (₹)",
    template="plotly_dark",
    height=500,
    legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", yanchor="top")
)
st.plotly_chart(fig2, use_container_width=True)
