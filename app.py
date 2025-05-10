# app.py

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Clinic Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinic Data Dashboard")
st.markdown(
    """
    Upload your clinic’s appointment data in CSV format with at least these columns:
    - **date** (YYYY‑MM‑DD)
    - **patient_id**
    - **doctor**
    - **revenue**
    """
)

# ---- Sidebar for file upload ----
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", type="csv", accept_multiple_files=False
)

if uploaded_file is not None:
    # read CSV
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
    
    st.subheader("Raw Data")
    st.dataframe(df.head(10), use_container_width=True)
    
    # key metrics
    total_appointments = len(df)
    total_patients = df["patient_id"].nunique()
    total_revenue = df["revenue"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", total_appointments)
    col2.metric("Unique Patients", total_patients)
    col3.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    # time series: appointments per day
    df_daily = df.groupby(df["date"].dt.date).size().rename("count").reset_index()
    df_revenue = df.groupby(df["date"].dt.date)["revenue"].sum().rename("revenue").reset_index()
    
    st.subheader("Daily Appointments & Revenue")
    chart_data = pd.merge(df_daily, df_revenue, on="date")
    chart_data = chart_data.set_index("date")
    st.line_chart(chart_data)
    
    # breakdown by doctor
    st.subheader("Appointments by Doctor")
    by_doc = df["doctor"].value_counts().rename_axis("doctor").reset_index(name="appointments")
    st.bar_chart(by_doc.set_index("doctor"))
    
else:
    st.info("Please upload a CSV file to see the dashboard.")
