import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# عنوان وترحيب
st.title("Welcome, Dr. Amr Refai 👨‍⚕️")
st.subheader("Boiling Process Simulator for Sugarcane")

# تحميل البيانات
df = pd.read_excel("datatoread.xlsx")

# مدخلات المستخدم (في الصفحة الرئيسية مش في sidebar)
temperature = st.slider("Set Temperature (°C)", 200, 300, 250)
time = st.slider("Set Time (minutes)", 15, 60, 30)

# عرض البيانات المختارة
st.write(f"🧪 Selected temperature: **{temperature} °C**")
st.write(f"⏱️ Selected time: **{time} minutes**")
st.write("🌾 Crop type: **Sugarcane**")

# رسم بياني بسيط بناءً على الوقت ودرجة الحرارة (مثال)
fig, ax = plt.subplots()
ax.plot(df['Time'], df['Temperature'], label="Original Data", color='blue')
ax.axhline(temperature, color='red', linestyle='--', label='Selected Temp')
ax.axvline(time, color='green', linestyle='--', label='Selected Time')
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("Temperature (°C)")
ax.legend()
st.pyplot(fig)
