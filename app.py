import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# رسالة ترحيب
st.title("Welcome Dr. Amr Refai 👋")
st.subheader("This analysis is for Sugarcane data only.")

# قراءة ملف الإكسل
df = pd.read_excel("datatoread.xlsx")

# عرض أسماء الأعمدة علشان نتأكد إنها صح (ممكن تشيل السطر ده بعد كده)
# st.write(df.columns)

# تعديل الأسماء لو فيها مسافات زيادة
df.columns = df.columns.str.strip()

# فلترة البيانات: الحرارة من 200 لـ 300، الوقت من 15 لـ 60
filtered_df = df[(df['Temperature'] >= 200) & (df['Temperature'] <= 300) & 
                 (df['Time'] >= 15) & (df['Time'] <= 60)]

# إدخال وقت من المستخدم
user_time = st.number_input("Enter time between 15 and 60:", min_value=15, max_value=60, step=1)

# فلترة على الوقت اللي المستخدم كتبه (لو عايز تستخدمه تحديدًا)
time_df = filtered_df[filtered_df['Time'] == user_time]

# رسم البيانات
fig, ax = plt.subplots()
ax.plot(filtered_df['Time'], filtered_df['Temperature'], label='Filtered Data', color='green')
ax.set_xlabel("Time")
ax.set_ylabel("Temperature")
ax.set_title("Temperature vs Time (Filtered)")
ax.legend()

st.pyplot(fig)

