import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="IT Job Market & Skills Analytics",
    page_icon="💼",
    layout="wide"
)

# Load datasets
df = pd.read_csv("data/india_job_market_2024_2026.csv")
skills_df = pd.read_csv("data/job_skills.csv")

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

# Space after KPI section
st.write("")

# =============================
# EXPERIENCE ANALYSIS
# =============================

st.subheader("Experience Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Job Listings by Experience Level**")

    experience_data = (
        df["Experience_Level"]
        .value_counts()
        .rename_axis("Experience Level")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        experience_data,
        x="Experience Level",
        y="Job Listings"
    )

with col2:
    st.markdown("**Average Salary by Experience Level**")

    salary_experience = (
        df.groupby("Experience_Level")["Salary_LPA"]
        .mean()
        .rename_axis("Experience Level")
        .reset_index(name="Average Salary")
    )

    st.bar_chart(
        salary_experience,
        x="Experience Level",
        y="Average Salary"
    )

# Space between sections
st.write("")

st.write("")

# =============================
# JOB ROLES & SKILLS
# =============================

st.subheader("Job Roles & Technical Skills")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Most Common IT Job Roles**")

    top_roles = (
        df["Job_Title"]
        .value_counts()
        .head(10)
        .rename_axis("Job Role")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        top_roles,
        x="Job Role",
        y="Job Listings"
    )

with col2:
    st.markdown("**Top 10 Most Frequently Required Technical Skills**")

    top_skills = (
        skills_df["Skill"]
        .value_counts()
        .head(10)
        .rename_axis("Skill")
        .reset_index(name="Occurrences")
    )

    st.bar_chart(
        top_skills,
        x="Skill",
        y="Occurrences"
    )

# Space between sections
st.write("")

st.write("")

# =============================
# LOCATION ANALYSIS
# =============================

st.subheader("Location Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 IT Job Locations**")

    top_locations = (
        df[df["City"] != "Remote"]["City"]
        .value_counts()
        .head(10)
        .rename_axis("City")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        top_locations,
        x="City",
        y="Job Listings"
    )

with col2:
    st.markdown("**Average Salary by Job Location**")

    salary_location = (
        df[df["City"] != "Remote"]
        .groupby("City")["Salary_LPA"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .rename_axis("City")
        .reset_index(name="Average Salary")
    )

    st.bar_chart(
        salary_location,
        x="City",
        y="Average Salary"
    )