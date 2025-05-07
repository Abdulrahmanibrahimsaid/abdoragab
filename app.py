import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# رسالة ترحيب
st.title("Welcome Dr. Amr Refai 👋")
st.subheader("This analysis is for Sugarcane data only.")

# قراءة الملف
df = pd.read_excel("datatoread.xlsx")

# إزالة أي مسافات من أسماء الأعمدة
df.columns = df.columns.str.strip()

# عرض أسماء الأعمدة علشان تتأكد بنفسك (ممكن تشيله بعد كده)
st.write("Detected columns:", df.columns.tolist())

# استخدام أول عمودين كـ Time و Temperature مهما كانت أسمائهم
try:
    time_col = df.columns[0]
    temp_col = df.columns[1]

    # فلترة البيانات داخل النطاق المطلوب
    filtered_df = df[(df[time_col] >= 15) & (df[time_col] <= 60) &
                     (df[temp_col] >= 200) & (df[temp_col] <= 300)]

    # إدخال وقت من المستخدم
    user_time = st.number_input("Enter time between 15 and 60:", min_value=15, max_value=60, step=1)
    user_filtered_df = filtered_df[filtered_df[time_col] == user_time]

    # رسم البيانات
    fig, ax = plt.subplots()
    ax.plot(filtered_df[time_col], filtered_df[temp_col], label='Filtered Data', color='green')
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature")
    ax.set_title("Temperature vs Time for Sugarcane")
    ax.legend()

    st.pyplot(fig)

except Exception as e:
    st.error(f"An error occurred while processing the data: {e}")

