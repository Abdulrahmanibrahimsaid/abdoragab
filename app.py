

import streamlit as st
import pandas as pd
from scipy.interpolate import griddata

# إعداد صفحة التطبيق
st.set_page_config(
    page_title="نظام محاكاة التحميص - قصب السكر",
    page_icon="🌱",
    layout="wide"
)

# تحميل البيانات
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("datatoread.xlsx", sheet_name="Sheet1")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"حدث خطأ في تحميل الملف: {e}")
        return None

df = load_data()

if df is not None:
    # تحضير نقاط البيانات للاستيفاء
    points = df[["Temperature", "Time(minutes)"]].values
    output_vars = ["C(%)", "H(%)", "N(%)", "S(%)", "O(%)", "HHV(MJ/Kg)"]
    values = {var: df[var].values for var in output_vars}

# واجهة المستخدم
st.title("🌱 نظام محاكاة عملية التحميص (قصب السكر)")
st.markdown("---")

with st.sidebar:
    st.header("إعدادات المحاكاة")
    temp_input = st.slider(
        "درجة الحرارة (مئوية)", 
        min_value=200, 
        max_value=300, 
        value=250,
        help="اختر قيمة بين 200 و 300 درجة مئوية"
    )
    
    time_input = st.selectbox(
        "مدة التحميص (دقيقة)",
        options=[15, 30, 45, 60],
        index=0
    )
    
    st.markdown("---")
    st.info("اضغط على زر الحساب لرؤية النتائج")

# وظيفة المحاكاة
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

# زر الحساب وعرض النتائج
if st.button("حساب النتائج", type="primary"):
    if df is not None:
        with st.spinner("جاري حساب النتائج..."):
            results = simulate(temp_input, time_input)
            
        st.success("تم الانتهاء من الحساب!")
        st.markdown("---")
        
        # عرض النتائج في بطاقات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("نسبة الكربون", f"{results['C(%)']:.2f}%")
            st.metric("نسبة الهيدروجين", f"{results['H(%)']:.2f}%")
        
        with col2:
            st.metric("نسبة النيتروجين", f"{results['N(%)']:.2f}%")
            st.metric("نسبة الكبريت", f"{results['S(%)']:.2f}%")
        
        with col3:
            st.metric("نسبة الأكسجين", f"{results['O(%)']:.2f}%")
            st.metric("القيمة الحرارية", f"{results['HHV(MJ/Kg)']:.2f} MJ/Kg")
        
        st.markdown("---")
        st.info("يمكنك تعديل المدخلات في الشريط الجانبي وإعادة الحساب")
    else:
        st.error("لا يمكن إجراء الحساب بسبب مشكلة في تحميل البيانات")

# تذييل الصفحة
st.markdown("---")
st.caption("تم تطوير هذا التطبيق باستخدام Streamlit و Python")
