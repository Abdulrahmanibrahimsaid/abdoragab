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

# عرض أسماء الأعمدة للتأكد (ممكن تشيل السطر ده بعد ما تتأكد)
# st.write("Columns:", df.columns)

# التأكد من وجود الأعمدة المطلوبة
if 'Time' not in df.columns or 'Temperature' not in df.columns:
    st.error("Error: 'Time' or 'Temperature' column not found in the Excel file. Please check column names.")
else:
    # فلترة البيانات حسب المطلوب
    filtered_df = df[(df['Temperature'] >= 200) & (df['Temperature'] <= 300) &
                     (df['Time'] >= 15) & (df['Time'] <= 60)]

    # اختيار الوقت من المستخدم
    user_time = st.number_input("Enter time between 15 and 60:", min_value=15, max_value=60, step=1)

    # فلترة حسب الوقت المدخل (اختياري)
    user_filtered_df = filtered_df[filtered_df['Time'] == user_time]

    # رسم البيانات
    fig, ax = plt.subplots()
    ax.plot(filtered_df['Time'], filtered_df['Temperature'], label='Filtered Data', color='green')
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature")
    ax.set_title("Temperature vs Time (Filtered)")
    ax.legend()

    st.pyplot(fig)


