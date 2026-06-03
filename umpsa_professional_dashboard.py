
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="UMPSA Alumni Analytics Dashboard", layout="wide")

# Branding
st.title("🎓 UMPSA Alumni Analytics Dashboard")
st.caption("Faculty Graduate Employability & Salary Intelligence System")

logo = st.sidebar.file_uploader("Upload UMPSA/Faculty Logo (Optional)", type=["png","jpg","jpeg"])
if logo:
    st.sidebar.image(logo, use_container_width=True)

uploaded_file = st.file_uploader("Upload Alumni Dataset (CSV)", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df["SALARY"] = pd.to_numeric(df["SALARY"], errors="coerce")

    st.sidebar.header("Dashboard Filters")

    # Dynamic filters
    if "GENDER" in df.columns:
        gender = st.sidebar.multiselect(
            "Gender",
            df["GENDER"].dropna().unique(),
            default=df["GENDER"].dropna().unique()
        )
        df = df[df["GENDER"].isin(gender)]

    if "STATE" in df.columns:
        state = st.sidebar.multiselect(
            "State",
            df["STATE"].dropna().unique(),
            default=df["STATE"].dropna().unique()
        )
        df = df[df["STATE"].isin(state)]

    if "PROGRAM TYPE" in df.columns:
        ptype = st.sidebar.multiselect(
            "Program Type",
            df["PROGRAM TYPE"].dropna().unique(),
            default=df["PROGRAM TYPE"].dropna().unique()
        )
        df = df[df["PROGRAM TYPE"].isin(ptype)]

    if "JOB STATUS" in df.columns:
        status = st.sidebar.multiselect(
            "Employment Status",
            df["JOB STATUS"].dropna().unique(),
            default=df["JOB STATUS"].dropna().unique()
        )
        df = df[df["JOB STATUS"].isin(status)]

    total = len(df)
    employed = (df["JOB STATUS"] == "BEKERJA SEPENUH MASA").sum() if "JOB STATUS" in df.columns else 0
    emp_rate = employed / total * 100 if total else 0

    salary_df = df[df["SALARY"] > 0]
    avg_salary = salary_df["SALARY"].mean() if len(salary_df) else 0

    top_program = "-"
    if "PROGRAM NAME" in df.columns and len(df):
        top_program = df["PROGRAM NAME"].value_counts().idxmax()

    # Executive Summary
    st.header("📊 Executive Summary")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Alumni", f"{total:,}")
    c2.metric("Employment Rate", f"{emp_rate:.1f}%")
    c3.metric("Average Salary", f"RM {avg_salary:,.0f}")
    c4.metric("Top Program", top_program)

    st.markdown("---")

    # Employment Analytics
    st.header("💼 Employment Analytics")

    col1,col2 = st.columns(2)

    with col1:
        if "PROGRAM NAME" in df.columns and "JOB STATUS" in df.columns:
            emp_prog = pd.crosstab(df["PROGRAM NAME"], df["JOB STATUS"])
            fig = px.bar(emp_prog, title="Employment by Program")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "STATE" in df.columns and "JOB STATUS" in df.columns:
            emp_state = pd.crosstab(df["STATE"], df["JOB STATUS"])
            fig = px.bar(emp_state, title="Employment by State")
            st.plotly_chart(fig, use_container_width=True)

    if "YEAR GRAD" in df.columns:
        emp_year = pd.crosstab(df["YEAR GRAD"], df["JOB STATUS"])
        fig = px.bar(emp_year, title="Employment by Graduation Year")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Salary Analytics
    st.header("💰 Salary Analytics")

    col3,col4 = st.columns(2)

    with col3:
        salary_df["Salary Band"] = pd.cut(
            salary_df["SALARY"],
            bins=[0,2000,3000,4000,5000,100000],
            labels=["<2000","2000-3000","3000-4000","4000-5000","5000+"]
        )
        band = salary_df["Salary Band"].value_counts().reset_index()
        band.columns = ["Salary Band","Count"]
        fig = px.bar(band, x="Salary Band", y="Count",
                     title="Salary Band Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        if "PROGRAM NAME" in salary_df.columns:
            top_salary = (
                salary_df.groupby("PROGRAM NAME")["SALARY"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            fig = px.bar(
                top_salary,
                x="SALARY",
                y="PROGRAM NAME",
                orientation="h",
                title="Top Earning Programs"
            )
            st.plotly_chart(fig, use_container_width=True)

    if {"PROGRAM NAME","GENDER","SALARY"}.issubset(df.columns):
        heat = pd.pivot_table(
            salary_df,
            values="SALARY",
            index="PROGRAM NAME",
            columns="GENDER",
            aggfunc="mean"
        )
        fig = px.imshow(
            heat,
            aspect="auto",
            title="Salary Heatmap by Program and Gender"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Interactive Drill-down
    st.header("🔍 Interactive Drill-Down")

    if "PROGRAM NAME" in df.columns:
        selected_program = st.selectbox(
            "Select Program",
            sorted(df["PROGRAM NAME"].dropna().unique())
        )

        program_df = df[df["PROGRAM NAME"] == selected_program]

        col5,col6 = st.columns(2)

        with col5:
            fig = px.histogram(
                program_df,
                x="SALARY",
                title=f"Salary Distribution - {selected_program}"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col6:
            if "STATE" in program_df.columns:
                fig = px.pie(
                    program_df,
                    names="STATE",
                    title=f"State Distribution - {selected_program}"
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Download Section
    st.header("⬇️ Export Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered CSV",
        csv,
        "filtered_alumni_data.csv",
        "text/csv"
    )

    st.dataframe(df, use_container_width=True)

else:
    st.info("Upload a CSV dataset to begin analysis.")
