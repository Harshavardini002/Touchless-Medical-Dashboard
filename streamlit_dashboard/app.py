import streamlit as st
st.set_page_config(page_title="Medical Dashboard", layout="wide")
import pandas as pd
import altair as alt
import json
import os
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 2 seconds
st_autorefresh(interval=2000, key="gesture_refresh")

# Load dataset
DATA_PATH = 'C:/Users/harsh/OneDrive/Desktop/touchless_dashboard_project/synthetic_data/patient_vitals.csv'
df = pd.read_csv(DATA_PATH)

# Print column names for debugging
print("DataFrame columns:", df.columns.tolist())

# Read hover from gesture detection
hover_file = "gesture_module/hover.json"
hovered_param = None
if os.path.exists(hover_file):
    with open(hover_file, "r") as f:
        hover_data = json.load(f)
        hovered_param = hover_data.get("hover", None)

# Gesture-to-vital mapping
gesture_map = {
    "1": "Heart Rate",
    "2": "Blood Pressure",
    "3": "Oxygen Saturation",
    "4": "Temperature",
    "5": "Medication"
}

# If hovered_param is a number (finger count), map to vital name
if hovered_param in gesture_map:
    hovered_param = gesture_map[hovered_param]

# Custom styling
st.markdown("""
<style>
body, .block-container {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: #e0e6eb;
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    text-align: center;
    font-weight: 700;
    font-size: 2.8rem;
    color: #cfe2f3;
    margin-bottom: 0.5rem;
}
h4 {
    text-align: center;
    font-weight: 300;
    color: #b0c4d8;
    margin-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background-color: #1b2a38;
    color: #dde9f4;
}
.card {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: border 0.3s ease;
}
.card h3 {
    font-size: 1.3rem;
    color: #dbeeff;
    margin-bottom: 0.5rem;
}
.card p {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f1f6fa;
    margin: 0;
}
.card.highlight {
    border: 3px solid #39ff14;
}
.alert {
    background-color: #d9534f;
    color: white;
    font-weight: 700;
    padding: 0.75rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# Touchless Medical Dashboard")
st.markdown("#### Real-time patient vitals for professional clinical monitoring")

# Sidebar
st.sidebar.header("Patient Selection")
patient_ids = df['Patient_ID'].unique()
selected_patient = st.sidebar.selectbox("Patient ID", patient_ids)
patient_df = df[df['Patient_ID'] == selected_patient].sort_values('DateTime')

st.sidebar.markdown("### Patient Info")
st.sidebar.write(f"**Patient ID:** {selected_patient}")
st.sidebar.write(f"**Condition:** {patient_df.iloc[-1]['Condition']}")
st.sidebar.write(f"**Last Update:** {patient_df.iloc[-1]['DateTime']}")

# Latest data
latest = patient_df.iloc[-1]

# Define default vitals and filter based on available columns
default_vitals = ["Heart Rate", "Blood Pressure", "Oxygen Saturation", "Temperature", "Medication"]
available_vitals = []
for v in default_vitals:
    if v == "Blood Pressure" and "BP_Systolic" in latest.index and "BP_Diastolic" in latest.index:
        available_vitals.append(v)
    elif v.replace(" ", "_") in latest.index:
        available_vitals.append(v)

vital_options = ["All"] + available_vitals
selected_vital = st.sidebar.selectbox("Select Vital to Highlight", vital_options)

# Alerts
alerts = []
if latest['Heart_Rate'] > 110:
    alerts.append("High Heart Rate")
if latest['Oxygen_Saturation'] < 90:
    alerts.append("Low Oxygen Saturation")
if latest['BP_Systolic'] > 140 or latest['BP_Diastolic'] > 90:
    alerts.append("High Blood Pressure")
if latest['Temperature'] > 100.4:
    alerts.append("Fever")

if alerts:
    alert_msg = " | ".join(alerts)
    st.markdown(f'<div class="alert">{alert_msg}</div>', unsafe_allow_html=True)

# Helper: determine if highlight
def get_card_class(vital_name):
    if hovered_param and hovered_param == vital_name:
        return "card highlight"
    elif selected_vital != "All" and selected_vital == vital_name:
        return "card highlight"
    else:
        return "card"

# Card layout
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="{get_card_class("Heart Rate")}"><h3>Heart Rate</h3><p>{int(latest["Heart_Rate"])} bpm</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="{get_card_class("Blood Pressure")}"><h3>Blood Pressure</h3><p>{int(latest["BP_Systolic"])}/{int(latest["BP_Diastolic"])} mmHg</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="{get_card_class("Oxygen Saturation")}"><h3>Oxygen Saturation</h3><p>{int(latest["Oxygen_Saturation"])}%</p></div>', unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown(f'<div class="{get_card_class("Temperature")}"><h3>Temperature</h3><p>{latest["Temperature"]}°F</p></div>', unsafe_allow_html=True)
with col5:
    medication_value = latest.get("Medication", "Data not available")
    st.markdown(f'<div class="{get_card_class("Medication")}"><h3>Medication</h3><p>{medication_value}</p></div>', unsafe_allow_html=True)

# Chart: Filter based on selected or hovered vital
st.markdown("## Vital Sign Trends")
chart_vitals = {
    "Heart Rate": ["Heart_Rate"],
    "Blood Pressure": ["BP_Systolic", "BP_Diastolic"],
    "Oxygen Saturation": ["Oxygen_Saturation"],
    "Temperature": ["Temperature"],
    "Medication": [],  # Exclude Medication from chart (non-numeric)
    "All": ["Heart_Rate", "BP_Systolic", "BP_Diastolic", "Oxygen_Saturation", "Temperature"]
}
selected_chart_vitals = chart_vitals.get(hovered_param or selected_vital, ["Heart_Rate", "BP_Systolic", "BP_Diastolic", "Oxygen_Saturation", "Temperature"])

# Only create chart if there are numeric columns to display
if selected_chart_vitals:
    vital_long_df = patient_df.melt(id_vars=["DateTime"], value_vars=selected_chart_vitals)
    chart = alt.Chart(vital_long_df).mark_line().encode(
        x='DateTime:T',
        y='value:Q',
        color='variable:N'
    ).properties(width=1000, height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.markdown("### No numeric data available for Medication trend")