import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# ترحيب
st.title("Welcome, Dr. Amr Refai 👨‍⚕️")
st.markdown("### This tool simulates the boiling process for Sugarcane. We hope it's helpful!")

# تحميل البيانات
df = pd.read_excel("datatoread.xlsx")

# مدخلات المستخدم - درجة الحرارة والوقت
temperature = st.slider("Set Temperature (°C)", 200, 300, 250)
time = st.number_input("Enter Time (between 15 and 60 minutes)", min_value=15, max_value=60, value=30)

# عرض المعلومات
st.write(f"🧪 Selected temperature: **{temperature} °C**")
st.write(f"⏱️ Selected time: **{time} minutes**")
st.write("🌾 Crop type: **Sugarcane**")

# رسم بياني
fig, ax = plt.subplots()
ax.plot(df['Time'], df['Temperature'], label="Original Data", color='blue')
ax.axhline(temperature, color='red', linestyle='--', label='Selected Temp')
ax.axvline(time, color='green', linestyle='--', label='Selected Time')
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Temperature (°C)")
ax.legend()
st.pyplot(fig)
