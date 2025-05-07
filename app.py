

import streamlit as st
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# App setup
st.set_page_config(
    page_title="Torrefaction Simulation - Sugarcane Bagasse",
    page_icon="🌱",
    layout="wide"
)

# Title and description
st.title("🌱 Torrefaction Process Simulator")
st.markdown("""
This app simulates the torrefaction process of sugarcane bagasse. 
Adjust the parameters in the sidebar and view the results.
""")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("datatoread.xlsx", sheet_name="Sheet1")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data file: {e}")
        return None

df = load_data()

if df is not None:
    # Prepare data for interpolation
    points = df[["Temperature", "Time(minutes)"]].values
    output_vars = ["C(%)", "H(%)", "N(%)", "S(%)", "O(%)", "HHV(MJ/Kg)"]
    values = {var: df[var].values for var in output_vars}

# Sidebar controls
with st.sidebar:
    st.header("Simulation Parameters")
    temp_input = st.slider(
        "Temperature (°C)",
        min_value=200,
        max_value=300,
        value=250,
        help="Select between 200-300°C"
    )
    
    time_input = st.selectbox(
        "Time (minutes)",
        options=[15, 30, 45, 60],
        index=0
    )
    
    st.markdown("---")
    st.info("Click 'Calculate' to run the simulation")

# Simulation function
def simulate(temperature, time):
    results = {}
    for var in output_vars:
        results[var] = float(griddata(
            points, 
            values[var], 
            (temperature, time), 
            method='linear'
        ))
    return results

# Main calculation and display
if st.button("Calculate Results", type="primary"):
    if df is not None:
        with st.spinner("Calculating..."):
            results = simulate(temp_input, time_input)
        
        st.success("Simulation completed!")
        st.markdown("---")
        
        # Results in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Carbon (C%)", f"{results['C(%)']:.2f}%")
            st.metric("Hydrogen (H%)", f"{results['H(%)']:.2f}%")
        
        with col2:
            st.metric("Nitrogen (N%)", f"{results['N(%)']:.2f}%")
            st.metric("Sulfur (S%)", f"{results['S(%)']:.2f}%")
        
        with col3:
            st.metric("Oxygen (O%)", f"{results['O(%)']:.2f}%")
            st.metric("Heating Value", f"{results['HHV(MJ/Kg)']:.2f} MJ/Kg")
        
        st.markdown("---")
        
        # Visualization Section
        st.subheader("Process Visualization")
        
        # 1. Temperature vs Composition Graph
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        for component in ["C(%)", "H(%)", "O(%)"]:
            ax1.plot(
                df["Temperature"].unique(),
                df.groupby("Temperature")[component].mean(),
                label=component
            )
        ax1.set_xlabel("Temperature (°C)")
        ax1.set_ylabel("Composition (%)")
        ax1.set_title("Average Composition vs Temperature")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)
        
        # 2. HHV vs Time at Selected Temperature
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        selected_temp_data = df[df["Temperature"] == temp_input]
        ax2.plot(
            selected_temp_data["Time(minutes)"],
            selected_temp_data["HHV(MJ/Kg)"],
            marker='o'
        )
        ax2.set_xlabel("Time (minutes)")
        ax2.set_ylabel("HHV (MJ/Kg)")
        ax2.set_title(f"Heating Value vs Time at {temp_input}°C")
        ax2.grid(True)
        st.pyplot(fig2)
        
        # 3. 3D Surface Plot (Advanced)
        try:
            from mpl_toolkits.mplot3d import Axes3D
            
            # Create grid for surface plot
            temp_grid = np.linspace(200, 300, 20)
            time_grid = np.linspace(15, 60, 20)
            T, t = np.meshgrid(temp_grid, time_grid)
            HHV_grid = griddata(
                points,
                values["HHV(MJ/Kg)"],
                (T, t),
                method='cubic'
            )
            
            fig3 = plt.figure(figsize=(10, 7))
            ax3 = fig3.add_subplot(111, projection='3d')
            surf = ax3.plot_surface(T, t, HHV_grid, cmap='viridis')
            ax3.set_xlabel('Temperature (°C)')
            ax3.set_ylabel('Time (minutes)')
            ax3.set_zlabel('HHV (MJ/Kg)')
            ax3.set_title('Heating Value Surface Plot')
            fig3.colorbar(surf)
            st.pyplot(fig3)
        except ImportError:
            st.warning("3D visualization requires matplotlib 3D toolkit")
        
        st.markdown("---")
        st.info("Adjust parameters in the sidebar to explore different scenarios")

# Footer
st.markdown("---")
st.caption("Developed with Python and Streamlit | Torrefaction Simulation Model")
