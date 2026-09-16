import streamlit as st
import pandas as pd

# =============================
# PAGE CONFIGURATION
# =============================

st.set_page_config(
    page_title="IT Job Market & Skills Analytics",
    page_icon="💼",
    layout="wide"
)

# =============================
# LOAD DATASETS
# =============================

df = pd.read_csv("data/india_job_market_2024_2026.csv")
skills_df = pd.read_csv("data/job_skills.csv")

# =============================
# DASHBOARD HEADER
# =============================

st.title("💼 IT Job Market & Skills Analytics")
st.caption("India • 2024–2026")

st.write("")

# =============================
# SIDEBAR FILTERS
# =============================

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Select one or more options")

experience_options = sorted(
    df["Experience_Level"].dropna().unique()
)

work_mode_options = sorted(
    df["Work_Mode"].dropna().unique()
)

job_type_options = sorted(
    df["Job_Type"].dropna().unique()
)

location_options = sorted(
    df["City"].dropna().unique()
)

education_options = sorted(
    df["Education_Required"].dropna().unique()
)

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
    default=experience_options
)

selected_work_mode = st.sidebar.multiselect(
    "Work Mode",
    work_mode_options,
    default=work_mode_options
)

selected_job_type = st.sidebar.multiselect(
    "Job Type",
    job_type_options,
    default=job_type_options
)

selected_location = st.sidebar.multiselect(
    "Location",
    location_options,
    default=location_options
)

selected_education = st.sidebar.multiselect(
    "Education Required",
    education_options,
    default=education_options
)

# =============================
# APPLY FILTERS
# =============================

filtered_df = df[
    df["Experience_Level"].isin(selected_experience)
    & df["Work_Mode"].isin(selected_work_mode)
    & df["Job_Type"].isin(selected_job_type)
    & df["City"].isin(selected_location)
    & df["Education_Required"].isin(selected_education)
]

# =============================
# FILTERED SKILLS DATA
# =============================

filtered_job_ids = set(filtered_df["Job_ID"])

filtered_skills_df = (
    df[df["Job_ID"].isin(filtered_job_ids)]
    .assign(
        Skill=df[df["Job_ID"].isin(filtered_job_ids)]["Skills_Required"]
        .str.split(", ")
    )
    .explode("Skill")
)

# =============================
# KPI CALCULATIONS
# =============================

total_jobs = len(filtered_df)

total_openings = filtered_df["Openings"].sum()

average_salary = (
    filtered_df["Salary_LPA"].mean()
    if not filtered_df.empty
    else 0
)

python_jobs = filtered_df["Skills_Required"].str.contains(
    "Python",
    case=False,
    na=False
).sum()

# =============================
# KPI CARDS
# =============================

st.subheader("Key Market Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Job Listings",
        f"{total_jobs:,}"
    )

with col2:
    st.metric(
        "Total Job Openings",
        f"{total_openings:,}"
    )

with col3:
    st.metric(
        "Average Salary",
        f"{average_salary:.2f} LPA"
    )

with col4:
    st.metric(
        "Python Required",
        f"{python_jobs:,}"
    )

st.write("")
st.write("")

# =============================
# EXPERIENCE ANALYSIS
# =============================

st.subheader("Experience Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Job Listings by Experience Level**")

    experience_data = (
        filtered_df["Experience_Level"]
        .value_counts()
        .rename_axis("Experience Level")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        experience_data,
        x="Experience Level",
        y="Job Listings",
        height=350
    )

with col2:
    st.markdown("**Average Salary by Experience (LPA)**")

    salary_experience = (
        filtered_df.groupby("Experience_Level")["Salary_LPA"]
        .mean()
        .rename_axis("Experience Level")
        .reset_index(name="Average Salary (LPA)")
    )

    st.bar_chart(
        salary_experience,
        x="Experience Level",
        y="Average Salary (LPA)",
        height=350
    )

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
        filtered_df["Job_Title"]
        .value_counts()
        .head(10)
        .rename_axis("Job Role")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        top_roles,
        x="Job Role",
        y="Job Listings",
        height=350
    )

with col2:
    st.markdown("**Top 10 Most Frequently Required Technical Skills**")

    top_skills = (
        filtered_skills_df["Skill"]
        .value_counts()
        .head(10)
        .rename_axis("Skill")
        .reset_index(name="Occurrences")
    )

    st.bar_chart(
        top_skills,
        x="Skill",
        y="Occurrences",
        height=350
    )

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
        filtered_df[filtered_df["City"] != "Remote"]["City"]
        .value_counts()
        .head(10)
        .rename_axis("City")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        top_locations,
        x="City",
        y="Job Listings",
        height=350
    )

with col2:
    st.markdown("**Average Salary by Location (LPA)**")

    salary_location = (
        filtered_df[filtered_df["City"] != "Remote"]
        .groupby("City")["Salary_LPA"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .rename_axis("City")
        .reset_index(name="Average Salary (LPA)")
    )

    st.bar_chart(
        salary_location,
        x="City",
        y="Average Salary (LPA)",
        height=350
    )

st.write("")
st.write("")

# =============================
# JOB TYPE ANALYSIS
# =============================

st.subheader("Job Type Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Job Type Distribution**")

    job_type_data = (
        filtered_df["Job_Type"]
        .value_counts()
        .rename_axis("Job Type")
        .reset_index(name="Job Listings")
    )

    st.bar_chart(
        job_type_data,
        x="Job Type",
        y="Job Listings",
        height=350
    )

with col2:
    st.markdown("**Average Salary by Job Type (LPA)**")

    salary_job_type = (
        filtered_df.groupby("Job_Type")["Salary_LPA"]
        .mean()
        .rename_axis("Job Type")
        .reset_index(name="Average Salary (LPA)")
    )

    st.bar_chart(
        salary_job_type,
        x="Job Type",
        y="Average Salary (LPA)",
        height=350
    )