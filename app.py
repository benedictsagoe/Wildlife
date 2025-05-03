import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import requests
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import seaborn as sns

# Rule-based mock model for demonstration
# Replace with real model if available

def predict_poaching_risk(features):
    heart_rate = features.get('heart_rate', 0)
    movement_speed = features.get('movement_speed', 0)
    if heart_rate < 30 or heart_rate > 150:
        return 0.8
    if movement_speed > 20:
        return 0.7
    return 0.2

def generate_animal_data():
    center_lat = 5.5303
    center_lon = -1.3107
    species_list = [
        'African Elephant', 'Lion', 'Leopard', 'Spotted Hyena', 'African Buffalo',
        'Waterbuck', 'Kob', 'Bushbuck', 'Red River Hog', 'Giant Pangolin',
        'Chimpanzee', 'Colobus Monkey', 'Green Monkey', 'Olive Baboon',
        'African Fish Eagle', 'Grey Parrot', 'Helmeted Guineafowl', 'Yellow-casqued Hornbill',
        'Forest Cobra'
    ]
    data = {
        'species': [],
        'lat': [],
        'lon': [],
        'timestamp': [],
        'heart_rate': [],
        'movement_speed': []
    }
    # Introduce broader and more realistic dispersion
    for species in species_list:
        population = np.random.randint(10, 31)
        lat_spread = np.random.uniform(0.05, 0.2)
        lon_spread = np.random.uniform(0.05, 0.2)
        for _ in range(population):
            data['species'].append(species)
            data['lat'].append(center_lat + np.random.normal(0, lat_spread))
            data['lon'].append(center_lon + np.random.normal(0, lon_spread))
            data['timestamp'].append(datetime.now())
            data['heart_rate'].append(np.random.randint(40, 120))
            data['movement_speed'].append(np.random.uniform(0, 15))
    df = pd.DataFrame(data)
    df['poaching_risk'] = df.apply(lambda row: predict_poaching_risk(row), axis=1)
    return df

def get_free_satellite_layer():
    return {
        "source": [
            {
                "type": "raster",
                "url": "https://tile.openstreetmap.org/{z}/{y}/{x}.png"
            }
        ]
    }

def main():
    st.set_page_config(layout="wide")
    st.title("Ghana Forest Reserve & Wildlife Protection System 🐘")

    animal_data = generate_animal_data()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Real-time Animal Tracking")
        fig = px.scatter_mapbox(
            animal_data,
            lat="lat",
            lon="lon",
            color="species",
            size="movement_speed",
            hover_data=["heart_rate", "species", "poaching_risk"],
            zoom=9,
            center=dict(lat=5.3333, lon=-1.4167),
            title="Animal Locations in Forest Reserve"
        )
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_layers=[get_free_satellite_layer()],
            height=600,
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Threat Alerts ⚠️")
        if not animal_data.empty:
            latest_animal = animal_data.iloc[-1]
            features = {
                'heart_rate': latest_animal['heart_rate'],
                'movement_speed': latest_animal['movement_speed']
            }
            prediction = predict_poaching_risk(features)

            if prediction > 0.7:
                st.error(f"High Poaching Risk Alert ({prediction*100:.1f}%)")
                st.write("Recommended actions:")
                st.write("- Alert ranger team (Mock Action)")
                st.write("- Activate camera traps (Mock Action)")
            else:
                st.success("No immediate high-risk alerts.")
        else:
            st.info("No animal data available yet.")

    st.subheader("System Status")
    st.metric("Last Update", current_time)
    st.metric("Connected Drones", "3/3 Online")
    st.metric("Camera Traps Active", "28/30")

    st.subheader("Forest Health")
    st.write("Vegetation Density")
    st.progress(0.85)
    st.write("Water Availability")
    st.progress(0.63)

    st.sidebar.title("Ranger Controls")

    st.sidebar.header("Risk Prediction")
    moon_phase = st.sidebar.slider("Moon Phase (0-4)", 0, 4, 2, help="Full moon increases poaching risk")
    rainfall = st.sidebar.slider("Rainfall (mm)", 0, 50, 10)
    risk = 0.0

    if st.sidebar.button("Calculate Risk"):
        risk = 0.1
        if moon_phase > 3:
            risk += 0.3
        if rainfall < 5:
            risk += 0.2
        st.sidebar.warning(f"Poaching Risk: {risk*100:.1f}% ")
    else:
        st.sidebar.warning(f"Poaching Risk: {risk*100:.1f}% ")

if __name__ == "__main__":
    main()

