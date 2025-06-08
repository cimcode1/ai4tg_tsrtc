import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.passenger import load_weekday_trends_data
from components.sidebar import render_main_sidebar, render_eda_sidebar
from utils.revenue import get_monthly_fare_summary
import pandas as pd

# Page config
st.set_page_config(
    page_title="Exploratory Data Analysis - TGSRTC Analytics",
    page_icon="📊",
    layout="wide"
)

# Sidebar rendering
render_main_sidebar()
filters = render_eda_sidebar()

# Load weather data once and preprocess
weather_csv_path = "Wl-Upl_final.csv"
df = pd.read_csv(filters['csv_path'], parse_dates=["date"])
df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.month_name()
df["Month_Num"] = df["date"].dt.month
df["Year"] = df["date"].dt.year
df.sort_values("date", inplace=True)




# Get trend type choice
eda_type = filters['eda_view_option']

if eda_type == "Passenger & Ticket Insights":
    # Title and description
    st.title("📊 Daily Passenger Trends")
    st.markdown("""
    Explore how many passengers traveled on each day for a selected **month and year**.
    """, unsafe_allow_html=True)

    st.subheader("📆 Select Month and Year")

    # Extract date components
    # df["Day"] = df["date"].dt.day
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month
    # df["Year"] = df["date"].dt.year

    # Dropdowns for Month and Year
    available_years = sorted(df["Year"].unique())
    selected_year = st.selectbox("Select Year", available_years, key="eda_year")

    # Only show months available for selected year
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", sorted(months_in_year), key="eda_month")

    # Filter the DataFrame for selected month and year
    df_daywise = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_daywise.sort_values("date", inplace=True)

    # Plotting
    st.markdown(f"### 📈 Total Passengers in **{selected_month} {selected_year}** (Daily View)")

    fig_day_pass = px.line(
        df_daywise,
        x="date",
        y="total_passengers",
        markers=True,
        title=f"Daily Passenger Trend – {selected_month} {selected_year}",
        labels={"total_passengers": "Passengers", "date": "Date"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_day_pass, use_container_width=True)

    st.title("👶🧑 Adult vs Child Passenger Share")
    st.markdown("""
    View daily trends of **adult** and **child** passenger percentages for a selected **month and year**.
    """)

    # Ensure required columns exist
    # df["Year"] = df["date"].dt.year
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month

    # Dropdowns for selection
    available_years = sorted(df["Year"].unique())
    selected_year = st.selectbox("Select Year", available_years, key="year_pct")

    available_months = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", sorted(available_months), key="month_pct")

    # Filter the data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Calculate percentages
    df_filtered["Total"] = df_filtered["total_adults"] + df_filtered["total_children"]
    df_filtered["Adult %"] = (df_filtered["total_adults"] / df_filtered["Total"] * 100).round(2)
    df_filtered["Child %"] = (df_filtered["total_children"] / df_filtered["Total"] * 100).round(2)

    # Plot
    st.markdown(f"### 📈 Passenger Share: Adults vs Children – {selected_month} {selected_year}")

    fig_pct = go.Figure()

    fig_pct.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["Adult %"],
        name="Adult %",
        mode="lines+markers",
        line=dict(color="#42A5F5", width=2)
    ))

    fig_pct.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["Child %"],
        name="Child %",
        mode="lines+markers",
        line=dict(color="#FF7043", width=2)
    ))

    fig_pct.update_layout(
        xaxis_title="Date",
        yaxis_title="Percentage (%)",
        template="plotly_dark",
        legend=dict(orientation="h"),
        title=f"Adult vs Child Passenger Percentage – {selected_month} {selected_year}",
        height=500,
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(fig_pct, use_container_width=True)

    st.title("💰 Daily Revenue Trend")
    st.markdown("""
    View the **total fare collected** for each day in a selected **month and year**.
    """)

    # Ensure necessary date fields
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month_name()
    df["Month_Num"] = df["date"].dt.month

    # Dropdowns for year and month
    available_years = sorted(df["Year"].unique())
    selected_year = st.selectbox("Select Year", available_years, key="revenue_year")

    available_months = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", sorted(available_months), key="revenue_month")

    # Filter data
    df_revenue = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_revenue.sort_values("date", inplace=True)

    # Plot
    st.markdown(f"### 📈 Revenue Collected – {selected_month} {selected_year}")

    fig_revenue = px.line(
        df_revenue,
        x="date",
        y="total_fare",
        title=f"Daily Revenue – {selected_month} {selected_year}",
        labels={"total_fare": "Total Fare (₹)", "date": "Date"},
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig_revenue, use_container_width=True)

    
    st.title("🧾 Adults vs Full Fare Tickets")
    st.markdown("""
    Compare the number of **adults** traveling with the total number of **full fare tickets** (online + offline).  
    This helps assess how many passengers are paying full fare compared to the adult headcount.
    """)

    # Ensure date columns
    # df["Year"] = df["date"].dt.year
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month

    # Compute total full fare tickets
    df["full_fare_tickets"] = df["no_of_full_fare_tickets_online"] + df["no_of_full_fare_tickets_offline"]

    # Dropdowns
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), key="fullfare_year")
    selected_month = st.selectbox(
        "Select Month",
        sorted(df[df["Year"] == selected_year]["Month"].unique()),
        key="fullfare_month"
    )

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Plot
    st.markdown(f"### 👥 Adults vs Full Fare Tickets – {selected_month} {selected_year}")

    fig_adults_vs_fullfare = go.Figure()

    # Adults (left axis)
    fig_adults_vs_fullfare.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_adults"],
        name="Total Adults",
        mode="lines+markers",
        line=dict(width=2, color="#42A5F5"),
        yaxis="y"
    ))

    # Full Fare Tickets (right axis)
    fig_adults_vs_fullfare.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["full_fare_tickets"],
        name="Full Fare Tickets (Online + Offline)",
        mode="lines+markers",
        line=dict(width=2, color="#66BB6A"),
        yaxis="y2"
    ))

    fig_adults_vs_fullfare.update_layout(
        title=f"Adults vs Full Fare Tickets – {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis=dict(title="Total Adults", side="left"),
        yaxis2=dict(title="Full Fare Tickets", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500
    )

    st.plotly_chart(fig_adults_vs_fullfare, use_container_width=True)

    st.title("🚌 Passengers vs Total Trips")
    st.markdown("""
    Visualize the relationship between the number of **passengers** and **offline trips**  
    operated on each day in the selected month.
    """)

    # Ensure date parts
    # df["Year"] = df["date"].dt.year
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month

    # Dropdowns
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), key="pass_trip_year")
    selected_month = st.selectbox(
        "Select Month",
        sorted(df[df["Year"] == selected_year]["Month"].unique()),
        key="pass_trip_month"
    )

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Plot
    st.markdown(f"### 🚍 Passengers vs Trips – {selected_month} {selected_year}")

    fig_pass_trips = go.Figure()

    # Passengers trace
    fig_pass_trips.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_passengers"],
        name="Total Passengers",
        mode="lines+markers",
        line=dict(color="#42A5F5", width=2),
        yaxis="y"
    ))

    # Trips trace
    fig_pass_trips.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["no_of_trips_offline"],
        name="Trips",
        mode="lines+markers",
        line=dict(color="#FFA726", width=2, dash="dash"),
        yaxis="y2"
    ))

    fig_pass_trips.update_layout(
        title=f"Total Passengers vs Trips – {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis=dict(title="Total Passengers", side="left"),
        yaxis2=dict(title="Trips", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500
    )

    st.plotly_chart(fig_pass_trips, use_container_width=True)

    st.title("🎟️ Children vs C/P Tickets Analysis")
    st.markdown("""
    Compare the number of **children passengers** and **C/P (Concessional/Pass) tickets** issued each day.
    """)

    # Extract date parts
    # df["Year"] = df["date"].dt.year
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month

    # Dropdowns
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), key="cp_year")
    selected_month = st.selectbox(
        "Select Month",
        sorted(df[df["Year"] == selected_year]["Month"].unique()),
        key="cp_month"
    )

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Plot
    st.markdown(f"### 👧 Children vs C/P Tickets – {selected_month} {selected_year}")

    fig_cp = go.Figure()

    # Children trace
    fig_cp.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_children"],
        name="Children",
        mode="lines+markers",
        line=dict(color="#42A5F5", width=2),
        yaxis="y"
    ))

    # C/P Tickets trace
    fig_cp.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_C/P_tickets"],
        name="C/P Tickets",
        mode="lines+markers",
        line=dict(color="#FF7043", width=2, dash="dot"),
        yaxis="y2"
    ))

    fig_cp.update_layout(
        title=f"Children vs C/P Tickets – {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis=dict(title="Children", side="left"),
        yaxis2=dict(title="C/P Tickets", overlaying="y", side="right"),
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500
    )

    st.plotly_chart(fig_cp, use_container_width=True)



   
   

    



    




elif eda_type == "Temporal & Holiday Trends":  # assign suitable key


    # ===================== PASSENGER DISTRIBUTION =====================
    st.markdown("## 🧾 Passenger Distribution by Weekday (2022–2024)")
    st.markdown("""
    The <strong>most popular weekday</strong> is <span style="color:#FF6B93;"><strong>highlighted with a border</strong></span>.
    """, unsafe_allow_html=True)

    df_filtered = df[df["Year"] < 2025].copy()
    df_filtered["Weekday"] = df_filtered["date"].dt.day_name()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    summary_df = df_filtered.groupby(["Year", "Weekday"])["total_passengers"].sum().reset_index()
    summary_df["Weekday"] = pd.Categorical(summary_df["Weekday"], categories=weekday_order, ordered=True)
    summary_df.sort_values(["Weekday", "Year"], inplace=True)

    total_by_weekday = summary_df.groupby("Weekday")["total_passengers"].sum()
    most_popular_day = total_by_weekday.idxmax()

    fig = go.Figure()
    years = sorted(summary_df["Year"].unique())
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]

    for i, year in enumerate(years):
        year_df = summary_df[summary_df["Year"] == year]
        line_widths = [2 if day == most_popular_day else 0 for day in year_df["Weekday"]]

        fig.add_trace(go.Bar(
            x=year_df["Weekday"],
            y=year_df["total_passengers"],
            name=str(year),
            marker_color=colors[i],
            marker_line_width=line_widths,
            marker_line_color="white",
            text=[f"{val:,.0f}" for val in year_df["total_passengers"]],
            textposition="outside",
            hoverinfo="text",
            hovertext=[
                f"{day} {year}<br>Passengers: {val:,.0f}"
                for day, val in zip(year_df["Weekday"], year_df["total_passengers"])
            ]
        ))

    fig.update_layout(
        barmode='group',
        title=dict(
            text=f"🏆 Highest Overall: {most_popular_day}",
            x=0.5,
            font=dict(size=20)
        ),
        xaxis_title="Weekday",
        yaxis_title="Total Passengers",
        template="plotly_dark",
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)

    # ===================== FARE DISTRIBUTION =====================
    st.markdown("## 💰 Fare Distribution by Weekday (2022–2024)")
    st.markdown("""
    The <strong>most profitable weekday</strong> is <span style="color:#FFD700;"><strong>highlighted with a border</strong></span>.
    """, unsafe_allow_html=True)

    fare_df = df[df["Year"] < 2025].copy()
    fare_df["Weekday"] = fare_df["date"].dt.day_name()

    fare_summary = fare_df.groupby(["Year", "Weekday"])["total_fare"].sum().reset_index()
    fare_summary["Weekday"] = pd.Categorical(fare_summary["Weekday"], categories=weekday_order, ordered=True)
    fare_summary.sort_values(["Weekday", "Year"], inplace=True)

    total_fare_by_day = fare_summary.groupby("Weekday")["total_fare"].sum()
    most_profitable_day = total_fare_by_day.idxmax()

    fig2 = go.Figure()

    for i, year in enumerate(sorted(fare_summary["Year"].unique())):
        year_df = fare_summary[fare_summary["Year"] == year]
        line_widths = [2 if day == most_profitable_day else 0 for day in year_df["Weekday"]]

        fig2.add_trace(go.Bar(
            x=year_df["Weekday"],
            y=year_df["total_fare"],
            name=str(year),
            marker_color=colors[i],
            marker_line_width=line_widths,
            marker_line_color="gold",
            text=[f"₹{val:,.0f}" for val in year_df["total_fare"]],
            textposition="outside",
            hoverinfo="text",
            hovertext=[
                f"{day} {year}<br>Fare: ₹{val:,.0f}"
                for day, val in zip(year_df["Weekday"], year_df["total_fare"])
            ]
        ))

    fig2.update_layout(
        barmode='group',
        title=dict(
            text=f"💡 Highest Overall: {most_profitable_day}",
            x=0.5,
            font=dict(size=20)
        ),
        xaxis_title="Weekday",
        yaxis_title="Total Fare (₹)",
        template="plotly_dark",
        height=550
    )
    st.plotly_chart(fig2, use_container_width=True)




    st.title("🎉 Passenger Count During Holidays vs Non-Holidays")

    # Ensure date and is_holiday columns are ready
    df_filtered = df[df["Year"].between(2022, 2025)].copy()

    # Group by holiday status
    summary_stats = df_filtered.groupby("Holiday")["total_passengers"].agg(["mean", "std"]).reset_index()

    # Map labels
    summary_stats["label"] = summary_stats["Holiday"].map({0: "Non-Holiday", 1: "Optional Holiday", 2: "Holiday", 3: "Long Weekend"})

    # Plot using Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=summary_stats["label"],
            y=summary_stats["mean"],
            error_y=dict(type='data', array=summary_stats["std"]),
            marker_color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
            name="Avg Passengers"
        )
    ])

    fig.update_layout(
        title="🎉 Mean Total Passengers During Holidays vs Non-Holidays (2022–2025)",
        xaxis_title="Day Type",
        yaxis_title="Average Total Passengers",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Optionally show data table
    st.write("### Summary Statistics")
    st.dataframe(
        summary_stats.rename(columns={"mean": "Mean", "std": "Std Dev", "is_holiday": "Is Holiday"})
        .set_index('label')
        .style.format({
            'Mean': '{:,.0f}',
            'Std Dev': '{:,.0f}'
        }),
        use_container_width=True,
        height=200
    )


    st.title("🎉 Fare Collection During Holidays vs Non-Holidays")

    # Filter for relevant years
    df_filtered = df[df["Year"].between(2022, 2025)].copy()

    # Group by holiday status and calculate mean & std for fare
    summary_stats = df_filtered.groupby("Holiday")["total_fare"].agg(["mean", "std"]).reset_index()

    # Map holiday type labels
    summary_stats["label"] = summary_stats["Holiday"].map({
        0: "Non-Holiday",
        1: "Optional Holiday",
        2: "Holiday",
        3: "Long Weekend"
    })

    # Plot the bar chart with error bars (std deviation)
    fig = go.Figure(data=[
        go.Bar(
            x=summary_stats["label"],
            y=summary_stats["mean"],
            error_y=dict(type='data', array=summary_stats["std"]),
            marker_color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
            name="Avg Fare"
        )
    ])

    fig.update_layout(
        title="🎉 Mean Fare Collection During Holidays vs Non-Holidays (2022–2025)",
        xaxis_title="Day Type",
        yaxis_title="Average Fare Collected",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Show table of fare stats
    st.write("### Summary Statistics (Fare ₹)")
    st.dataframe(
        summary_stats.rename(columns={"mean": "Mean Fare", "std": "Std Dev", "is_holiday": "Is Holiday"})
        .set_index("label")
        .style.format({
            "Mean Fare": "₹{:,.0f}",
            "Std Dev": "₹{:,.0f}"
        }),
        use_container_width=True,
        height=200
    )


    st.title("🧮 Average Passengers per Trip (Daily Trend)")

    # Extract date info
    # df["Year"] = df["date"].dt.year
    # df["Month"] = df["date"].dt.month_name()
    # df["Month_Num"] = df["date"].dt.month

    # Dropdown filters
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1, key="year_avgpass")
    months_in_year = df[df["Year"] == selected_year]["Month"].unique()
    selected_month = st.selectbox("Select Month", months_in_year, key="month_avgpass")

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Calculate average passengers per trip
    df_filtered["avg_passengers_per_trip"] = df_filtered["total_passengers"] / df_filtered["no_of_trips_offline"]
    df_filtered["avg_passengers_per_trip"].fillna(0, inplace=True)  # handle divide-by-zero if any

    # Plot line graph
    fig_avg_pass = go.Figure()

    fig_avg_pass.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["avg_passengers_per_trip"],
        mode='lines+markers',
        name="Avg Passengers/Trip",
        line=dict(width=2, color="#29B6F6")
    ))

    # # Optional: Highlight holidays
    # for idx, row in df_filtered.iterrows():
    #     if row["Holiday"] in [1, 2, 3]:
    #         fig_avg_pass.add_vrect(
    #             x0=row["date"],
    #             x1=row["date"] + pd.Timedelta(days=1),
    #             fillcolor=holiday_colors[row["Holiday"]],
    #             opacity=0.2,
    #             layer="below",
    #             line_width=0,
    #             annotation_text=holiday_labels[row["Holiday"]],
    #             annotation_position="top left",
    #             annotation=dict(
    #                 font_size=10,
    #                 font_color="white",
    #                 textangle=-90,
    #                 bgcolor=holiday_colors[row["Holiday"]],
    #                 opacity=0.8
    #             )
    #         )

    fig_avg_pass.update_layout(
        xaxis_title="Date",
        yaxis_title="Avg Passengers per Trip",
        title=f"Average Passengers per Trip – {selected_month} {selected_year}",
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig_avg_pass, use_container_width=True)




elif eda_type == "Revenue Channels & Bus Deployment": 

    st.title("🧍 Passenger Trends: Total vs Online vs Offline")

    # Dropdowns for selecting Year and Month
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1, key="passenger_year")
    selected_month = st.selectbox("Select Month", df[df["Year"] == selected_year]["Month"].unique(), key="passenger_month")

    # Filter DataFrame for selected year and month
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Create line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_passengers"],
        mode="lines+markers",
        name="Total Passengers",
        line=dict(color="#66BB6A")
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["no_of_passengers_online"],
        mode="lines+markers",
        name="Online Passengers",
        line=dict(color="#42A5F5")
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["no_of_passengers_offline"],
        mode="lines+markers",
        name="Offline Passengers",
        line=dict(color="#FFA726")
    ))

    fig.update_layout(
        title=f"📈 Passenger Trend – {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis_title="Number of Passengers",
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


    st.title("💰 Revenue Trends: Total vs Online vs Offline")

    # Dropdowns for year and month
    selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()), index=len(df["Year"].unique()) - 1, key="revenue_year_1")
    selected_month = st.selectbox("Select Month", df[df["Year"] == selected_year]["Month"].unique(), key="revenue_month_1")

    # Filter data
    df_filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)].copy()
    df_filtered.sort_values("date", inplace=True)

    # Line Chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_fare"],
        mode="lines+markers",
        name="Total Revenue",
        line=dict(color="#66BB6A")
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_fare_collected_online"],
        mode="lines+markers",
        name="Online Revenue",
        line=dict(color="#42A5F5")
    ))

    fig.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["total_fare_collected_offline"],
        mode="lines+markers",
        name="Offline Revenue",
        line=dict(color="#FFA726")
    ))

    fig.update_layout(
        title=f"📈 Revenue Trend – {selected_month} {selected_year}",
        xaxis_title="Date",
        yaxis_title="Revenue (₹)",
        template="plotly_dark",
        legend=dict(orientation="h"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)




elif eda_type == "External Factors & Derived Data":

    import plotly.graph_objects as go

    st.title("🌙 Impact of Moon Calendar on Total Passengers")

    # Filter and clean data
    # Calculate date 6 months ago from the latest date
    latest_date = df['date'].max()
    six_months_ago = latest_date - pd.DateOffset(months=6)
    
    # Filter data for last 6 months
    df_filtered = df[df['date'] >= six_months_ago].copy()
    df_filtered["Moon Calendar"] = pd.to_numeric(df_filtered["Moon Calendar"], errors='coerce')
    df_filtered = df_filtered.dropna(subset=["Moon Calendar", "total_passengers"])

    # Calculate mean and std for each Moon Calendar value
    stats_df = df_filtered.groupby("Moon Calendar")["total_passengers"].agg(["mean", "std"]).reset_index()

    # Scatter plot: raw points
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_filtered["Moon Calendar"],
        y=df_filtered["total_passengers"],
        mode="markers",
        name="Raw Data",
        marker=dict(color="rgba(31, 119, 180, 0.5)"),
        showlegend=True
    ))

    # Line plot with error bars: mean ± std
    fig.add_trace(go.Scatter(
        x=stats_df["Moon Calendar"],
        y=stats_df["mean"],
        mode="lines+markers",
        name="Mean ± Std Dev",
        line=dict(color="#FF7F0E", width=2),
        error_y=dict(type="data", array=stats_df["std"], visible=True)
    ))

    # Layout
    fig.update_layout(
        title="🌙 Total Passengers vs Moon Calendar with Mean ± Std Dev (last 6 months)",
        xaxis_title="Moon Calendar Day",
        yaxis_title="Total Passengers",
        template="plotly_dark",
        height=550,
        legend=dict(
            orientation="h",
            y=-0.2,
            yanchor="top",
            x=0.5,
            xanchor="center"
        )
    )

    st.plotly_chart(fig, use_container_width=True)


    st.title("📈 Correlation: Weather, Events & Holiday Impact on Total Passengers")

    st.markdown("""
    This heatmap shows the correlation of various factors (rainfall, holiday, school events, temperatures) with **total passengers**.
    A high correlation indicates a stronger relationship (positive or negative).
    """)

    # Select and clean relevant columns
    corr_cols = [
        "total_passengers",
        "Rainfall_mm",
        "Holiday",
        "School Events",
        "Max_temp_celsius",
        "Min_temp_celsius"
    ]

    df_corr = df[corr_cols].copy()
    df_corr = df_corr.dropna()

    # Convert to numeric
    for col in corr_cols:
        df_corr[col] = pd.to_numeric(df_corr[col], errors="coerce")

    # Compute correlation matrix
    corr_matrix = df_corr.corr()

    # Plot using Plotly
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlation Matrix: Factors Impacting Total Passengers"
    )

    st.plotly_chart(fig_corr, use_container_width=True)


    
    st.subheader("🌦️ Seasonal Impact on Trends (Daily – Year View)")

    # Pick the year (default 2024 or latest)
    years = sorted(df["Year"].unique())
    default_index = years.index(2024) if 2024 in years else len(years) - 1
    yr = st.selectbox("Select Year", years, index=default_index, key="year_season")

    dff = (
        df[df["Year"] == yr]
        .sort_values("date")
        .reset_index(drop=True)
    )

    # Colour / label maps
    season_colors = {
        0: "#ADD8E6",   # Winter
        1: "#FFA500",   # Summer
        2: "#32CD32",   # Monsoon
        3: "#9370DB",   # Post-Monsoon
    }
    season_labels = {
        0: "Winter", 1: "Summer", 2: "Monsoon", 3: "Post Monsoon"
    }

    # ---------- FAST SHAPES: one per contiguous season block ----------
    shapes = []
    for _, grp in dff.groupby((dff["Season"].diff().fillna(0) != 0).cumsum()):
        code = int(grp["Season"].iloc[0])
        shapes.append(
            dict(
                type="rect",
                xref="x",
                yref="paper",
                x0=grp["date"].iloc[0],
                x1=grp["date"].iloc[-1] + pd.Timedelta(days=1),
                y0=0, y1=1,
                fillcolor=season_colors[code],
                opacity=0.15,
                layer="below",
                line_width=0,
            )
        )

    # ---------- FIG ----------
    fig = go.Figure()

    # 1 trace for the passenger line (hover shows date & passengers)
    fig.add_trace(
        go.Scatter(
            x=dff["date"],
            y=dff["total_passengers"],
            mode="lines+markers",
            name="Total Passengers",
            marker=dict(size=6),
            line=dict(color="#1f77b4"),
            hovertemplate="<b>%{x|%d-%b}</b><br>Total: %{y}<extra></extra>",
        )
    )

    # ONE invisible scatter for season hover—even 365 pts is fine
    fig.add_trace(
        go.Scatter(
            x=dff["date"],
            y=[dff["total_passengers"].max()] * len(dff),
            mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            hovertemplate=[
                f"<b>{season_labels.get(c, 'Unknown')}</b><extra></extra>"
                for c in dff["Season"]
            ],
            showlegend=False,
        )
    )

    # Attach shapes
    fig.update_layout(shapes=shapes)

    # Layout tweaks
    fig.update_layout(
        title=f"🌦️ Seasonal Influence on Total Passengers – {yr}",
        xaxis_title="Date",
        yaxis_title="Total Passengers",
        template="plotly_dark",
        height=550,
        legend=dict(
            orientation="h",
            y=-0.2,
            yanchor="top",
            x=0.5,
            xanchor="center",
        ),
        margin=dict(l=40, r=30, t=70, b=80),
    )

    # ---------- Custom legend HTML (fast & lightweight) ----------
    legend_html = "  ".join(
        f"<span style='color:{season_colors[k]};'><strong>⬤ {v}</strong></span>"
        for k, v in season_labels.items()
    )
    st.markdown(legend_html, unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)



