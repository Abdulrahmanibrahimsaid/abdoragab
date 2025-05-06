# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np

# 1. تحميل البيانات
file_path = "datatoread.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# 2. تجهيز نقاط البيانات
points = df[["Temperature", "Time(minutes)"]].values
output_vars = ["C(%)", "H(%)", "N(%)", "S(%)", "O(%)", "HHV(MJ/Kg)"]
values = {var: df[var].values for var in output_vars}

# 3. تعريف الدالة الحسابية
def get_simulation_results(temperature, time):
    results = {}
    for var in output_vars:
        results[var] = griddata(points, values[var], (temperature, time), method='linear')
    return results

# 4. واجهة Streamlit
st.title("🌿 TORREFACTION HYSYS - Sugarcane Bagasse Version")
st.markdown("Simulate torrefaction process outputs based on temperature and time inputs.")

st.sidebar.header("Input Parameters")
temp_input = st.sidebar.slider("Temperature (°C)", 200, 300, 250)
time_input = st.sidebar.selectbox("Time (minutes)", [15, 30, 45, 60])

if st.sidebar.button("Run Simulation"):
    results = get_simulation_results(temp_input, time_input)
    st.subheader("Simulation Results")
    if results:
        for var in output_vars:
            st.write(f"**{var}**: {results[var]:.2f}")
    else:
        st.warning("No result could be interpolated for the selected inputs.")

# 5. عرض الرسوم البيانية
st.subheader("📈 Variable Trends by Temperature")
time_points = df["Time(minutes)"].unique()
for var in output_vars:
    fig, ax = plt.subplots()
    for time in time_points:
        temp_data = df[df["Time(minutes)"] == time]["Temperature"]
        var_data = df[df["Time(minutes)"] == time][var]
        ax.plot(temp_data, var_data, label=f"{time} min")

    ax.set_xlabel("Temperature")
    ax.set_ylabel(var)
    ax.set_title(f"{var} vs Temperature")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
