import streamlit as st
import pandas as pd
import plotly.express as px


# PAGE CONFIGURATION

st.set_page_config(
    page_title="IT Job Market & Skills Analytics",
    page_icon="💼",
    layout="wide"
)


# CUSTOM CSS

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .main-caption {
        font-size: 18px;
        color: #666;
        margin-top: 0px;
        margin-bottom: 30px;
    }

    .section-heading {
        font-size: 28px;
        font-weight: 650;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        color: #777;
        font-size: 14px;
        margin-top: 50px;
        padding-top: 20px;
        padding-bottom: 20px;
    }

    .footer-line {
        font-weight: 600;
        margin-bottom: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# LOAD DATA

df = pd.read_csv("data/india_job_market_2024_2026.csv")
skills_df = pd.read_csv("data/job_skills.csv")


# Convert date column to datetime

df["Date_Posted"] = pd.to_datetime(df["Date_Posted"])


# HEADER

st.markdown(
    '<div class="main-title">💼 IT Job Market & Skills Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-caption">India • 2024–2026</div>',
    unsafe_allow_html=True
)


# SIDEBAR FILTERS

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Select one or more options")


# Experience Level

experience_options = sorted(
    df["Experience_Level"].dropna().unique()
)

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
    default=experience_options
)


# Work Mode

work_mode_options = sorted(
    df["Work_Mode"].dropna().unique()
)

selected_work_mode = st.sidebar.multiselect(
    "Work Mode",
    work_mode_options,
    default=work_mode_options
)


# Job Type

job_type_options = sorted(
    df["Job_Type"].dropna().unique()
)

selected_job_type = st.sidebar.multiselect(
    "Job Type",
    job_type_options,
    default=job_type_options
)


# Location

location_options = sorted(
    df["Location_Tier"].dropna().unique()
)

selected_location = st.sidebar.multiselect(
    "Location",
    location_options,
    default=location_options
)


# Education

education_options = sorted(
    df["Education_Required"].dropna().unique()
)

selected_education = st.sidebar.multiselect(
    "Education Required",
    education_options,
    default=education_options
)


# APPLY FILTERS

filtered_df = df[
    (df["Experience_Level"].isin(selected_experience))
    & (df["Work_Mode"].isin(selected_work_mode))
    & (df["Job_Type"].isin(selected_job_type))
    & (df["Location_Tier"].isin(selected_location))
    & (df["Education_Required"].isin(selected_education))
]


# EMPTY FILTER HANDLING

if filtered_df.empty:

    st.warning(
        "No jobs match the selected filters. "
        "Please select at least one option."
    )

    st.stop()


# FILTER SKILLS DATA

filtered_job_ids = set(filtered_df["Job_ID"])

filtered_skills_df = (
    df[
        df["Job_ID"].isin(filtered_job_ids)
    ][
        ["Job_ID", "Skills_Required"]
    ]
    .assign(
        Skill=lambda x: x["Skills_Required"].str.split(", ")
    )
    .explode("Skill")
)


# KPI SECTION

st.markdown(
    '<div class="section-heading">Key Metrics</div>',
    unsafe_allow_html=True
)


total_job_listings = len(filtered_df)

total_job_openings = filtered_df["Openings"].sum()

average_salary = filtered_df["Salary_LPA"].mean()

python_required = (
    filtered_skills_df["Skill"]
    .eq("Python")
    .sum()
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Job Listings",
        f"{total_job_listings:,}"
    )


with col2:
    st.metric(
        "Total Job Openings",
        f"{total_job_openings:,}"
    )


with col3:
    st.metric(
        "Average Salary",
        f"{average_salary:.2f} LPA"
    )


with col4:
    st.metric(
        "Python Required",
        f"{python_required:,}"
    )


# SECTION 1 — EXPERIENCE

st.markdown(
    '<div class="section-heading">Experience & Salary</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Job Listings by Experience

experience_counts = (
    filtered_df["Experience_Level"]
    .value_counts()
    .reset_index()
)

experience_counts.columns = [
    "Experience Level",
    "Job Listings"
]


with col1:

    st.markdown("**Job Listings by Experience Level**")

    st.bar_chart(
        experience_counts.set_index("Experience Level"),
        height=350
    )


# Average Salary by Experience

salary_experience = (
    filtered_df
    .groupby("Experience_Level")["Salary_LPA"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

salary_experience.columns = [
    "Experience Level",
    "Average Salary"
]


with col2:

    st.markdown("**Average Salary by Experience Level**")

    st.bar_chart(
        salary_experience.set_index("Experience Level"),
        height=350
    )


# SECTION 2 — JOB ROLES & SKILLS

st.markdown(
    '<div class="section-heading">Roles & Skills</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Top Job Roles

top_roles = (
    filtered_df["Job_Title"]
    .value_counts()
    .head(10)
    .sort_values()
)


with col1:

    st.markdown("**Top 10 Most Common IT Job Roles**")

    st.bar_chart(
        top_roles,
        height=350
    )


# Top Technical Skills

top_skills = (
    filtered_skills_df["Skill"]
    .value_counts()
    .head(10)
    .sort_values()
)


with col2:

    st.markdown(
        "**Top 10 Most Frequently Required Technical Skills**"
    )

    st.bar_chart(
        top_skills,
        height=350
    )


# SECTION 3 — LOCATION

st.markdown(
    '<div class="section-heading">Location Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Top Locations

top_locations = (
    filtered_df[
        filtered_df["City"] != "Remote"
    ]["City"]
    .value_counts()
    .head(10)
    .sort_values()
)


with col1:

    st.markdown(
        "**Top 10 IT Job Locations (Excluding Remote)**"
    )

    st.bar_chart(
        top_locations,
        height=350
    )


# Average Salary by Location

salary_location = (
    filtered_df[
        filtered_df["City"] != "Remote"
    ]
    .groupby("City")["Salary_LPA"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)


with col2:

    st.markdown(
        "**Average Salary by Job Location (Excluding Remote)**"
    )

    st.bar_chart(
        salary_location,
        height=350
    )


# SECTION 4 — JOB TYPE

st.markdown(
    '<div class="section-heading">Job Type Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# Job Type Distribution

job_type_counts = (
    filtered_df["Job_Type"]
    .value_counts()
    .sort_values()
)


with col1:

    st.markdown("**Job Type Distribution**")

    st.bar_chart(
        job_type_counts,
        height=350
    )


# Average Salary by Job Type

salary_job_type = (
    filtered_df
    .groupby("Job_Type")["Salary_LPA"]
    .mean()
    .sort_values(ascending=False)
)


with col2:

    st.markdown("**Average Salary by Job Type**")

    st.bar_chart(
        salary_job_type,
        height=350
    )


# SECTION 5 — JOB POSTING TREND

st.markdown(
    '<div class="section-heading">Job Posting Trend</div>',
    unsafe_allow_html=True
)


monthly_jobs = (
    filtered_df
    .set_index("Date_Posted")
    .resample("ME")
    .size()
    .rename("Job Listings")
    .reset_index()
)


st.markdown("**Monthly Job Listings (2024–2026)**")


# Plotly Line Chart

fig = px.line(
    monthly_jobs,
    x="Date_Posted",
    y="Job Listings",
    markers=True
)


fig.update_xaxes(
    title="Month",
    tickformat="%b %Y",
    dtick="M1",
    tickangle=-45
)


fig.update_yaxes(
    title="Job Listings"
)


fig.update_layout(
    height=400,
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=70
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# FOOTER

st.markdown(
    """
    <div class="footer">
        <div class="footer-line">
            IT Job Market & Skills Analytics • India 2024–2026
        </div>
        <div>
            Built with Python, Pandas & Streamlit
        </div>
    </div>
    """,
    unsafe_allow_html=True
)