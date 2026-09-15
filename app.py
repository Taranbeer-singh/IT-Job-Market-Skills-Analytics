import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="IT Job Market & Skills Analytics",
    page_icon="💼",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/india_job_market_2024_2026.csv")

# Dashboard title
st.title("IT Job Market & Skills Analytics")
st.caption("India • 2024–2026")

# -----------------------------
# KPI Calculations
# -----------------------------

total_jobs = len(df)
total_openings = df["Openings"].sum()
average_salary = df["Salary_LPA"].mean()

python_jobs = df["Skills_Required"].str.contains(
    "Python",
    case=False,
    na=False
).sum()

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Job Listings", f"{total_jobs:,}")

with col2:
    st.metric("Total Job Openings", f"{total_openings:,}")

with col3:
    st.metric("Average Salary", f"{average_salary:.2f} LPA")

with col4:
    st.metric("Python Required", f"{python_jobs:,}")

# -----------------------------
# Job Listings by Experience
# -----------------------------

st.subheader("Job Listings by Experience Level")

experience_data = df["Experience_Level"].value_counts()

st.bar_chart(experience_data)

# -----------------------------
# Average Salary by Experience
# -----------------------------

st.subheader("Average Salary by Experience Level")

salary_experience = (
    df.groupby("Experience_Level")["Salary_LPA"]
    .mean()
)

st.bar_chart(salary_experience)