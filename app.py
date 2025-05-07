import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# رسالة ترحيب
st.title("Welcome Dr. Amr Refai 👋")
st.subheader("This dashboard is for Sugarcane data only.")

# قراءة البيانات
df = pd.read_excel("datatoread.xlsx")
df.columns = df.columns.str.strip()  # إزالة أي مسافات زائدة

# عرض أسماء الأعمدة لتأكيدها
st.subheader("Detected columns:")
st.write(list(df.columns))

# أسماء الأعمدة كما هي في الملف
temp_col = "Temperature"
time_col = "Time (minutes)"

# التحقق من الأعمدة المطلوبة
if temp_col in df.columns and time_col in df.columns:
    # فلترة البيانات بدرجة الحرارة بين 200 و300
    filtered_df = df[(df[temp_col] >= 200) & (df[temp_col] <= 300)]

    # اختيار وقت بين 15 و60
    user_time = st.number_input("Enter a time value between 15 and 60 minutes:", min_value=15, max_value=60, step=1)

    # فلترة بالوقت
    time_filtered_df = filtered_df[filtered_df[time_col] == user_time]

    # رسم بياني
    st.subheader("Temperature vs Time")
    fig, ax = plt.subplots()
    ax.plot(filtered_df[time_col], filtered_df[temp_col], color="green", label="Temperature Data")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Sugarcane Temperature Range (200–300 °C)")
    ax.legend()
    st.pyplot(fig)

    # إحصائيات
    st.subheader("Statistics for Filtered Data (200–300°C)")
    st.write(filtered_df.describe())

    # إظهار بيانات الوقت المُدخل
    if not time_filtered_df.empty:
        st.success(f"Data for {user_time} minutes:")
        st.write(time_filtered_df)
    else:
        st.warning(f"No data available at {user_time} minutes.")
else:
    st.error(f"Error: Required columns not found. Make sure '{time_col}' and '{temp_col}' exist in your Excel file.")
