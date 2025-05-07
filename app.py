import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# رسالة ترحيب
st.title("Welcome Dr. Amr Refai 👋")
st.subheader("This analysis is for Sugarcane data only.")

# قراءة البيانات
df = pd.read_excel("datatoread.xlsx")

# إزالة المسافات من أسماء الأعمدة
df.columns = df.columns.str.strip()

# التحقق من وجود الأعمدة المطلوبة
if "Time (minutes)" in df.columns and "Temperature" in df.columns:
    # فلترة البيانات لدرجة الحرارة بين 200 و300
    filtered_df = df[(df["Temperature"] >= 200) & (df["Temperature"] <= 300)]

    # إدخال الوقت من المستخدم
    user_time = st.number_input("Enter time between 15 and 60 minutes:", min_value=15, max_value=60, step=1)
    
    # فلترة الوقت بناءً على اختيار المستخدم
    time_filtered_df = filtered_df[filtered_df["Time (minutes)"] == user_time]

    # رسم البيانات
    fig, ax = plt.subplots()
    ax.plot(filtered_df["Time (minutes)"], filtered_df["Temperature"], label="Filtered Data", color='green')
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature vs Time for Sugarcane")
    ax.legend()
    st.pyplot(fig)

    # إحصائيات
    st.subheader("Filtered Data Statistics")
    st.write(filtered_df.describe())

    if not time_filtered_df.empty:
        st.success(f"Data for time = {user_time} minutes:")
        st.write(time_filtered_df)
    else:
        st.warning(f"No data available exactly at time = {user_time} minutes.")
else:
    st.error("Error: Required columns not found. Make sure 'Time (minutes)' and 'Temperature' exist.")
