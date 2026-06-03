import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="UMPSA Alumni Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# TITLE
# =====================================================

st.title("🎓 UMPSA Alumni Analytics Dashboard")
st.caption("Graduate Employability & Salary Intelligence System")

# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload gpcombined.csv",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # =================================================
    # DATA CLEANING
    # =================================================

    if "SALARY" in df.columns:
        df["SALARY"] = pd.to_numeric(
            df["SALARY"],
            errors="coerce"
        )

    # =================================================
    # FILTERS
    # =================================================

    st.subheader("Filters")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        gender_options = sorted(
            df["GENDER"].dropna().unique()
        ) if "GENDER" in df.columns else []

        gender_filter = st.multiselect(
            "Gender",
            gender_options,
            default=gender_options
        )

    with f2:
        state_options = sorted(
            df["STATE"].dropna().unique()
        ) if "STATE" in df.columns else []

        state_filter = st.multiselect(
            "State",
            state_options,
            default=state_options
        )

    with f3:
        program_options = sorted(
            df["PROGRAM TYPE"].dropna().unique()
        ) if "PROGRAM TYPE" in df.columns else []

        program_filter = st.multiselect(
            "Program Type",
            program_options,
            default=program_options
        )

    with f4:
        status_options = sorted(
            df["JOB STATUS"].dropna().unique()
        ) if "JOB STATUS" in df.columns else []

        status_filter = st.multiselect(
            "Employment Status",
            status_options,
            default=status_options
        )

    # =================================================
    # APPLY FILTERS
    # =================================================

    filtered_df = df.copy()

    if "GENDER" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["GENDER"].isin(gender_filter)
        ]

    if "STATE" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["STATE"].isin(state_filter)
        ]

    if "PROGRAM TYPE" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["PROGRAM TYPE"].isin(program_filter)
        ]

    if "JOB STATUS" in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df["JOB STATUS"].isin(status_filter)
        ]

    salary_df = filtered_df[
        filtered_df["SALARY"] > 0
    ].copy()

    # =================================================
    # KPI SECTION
    # =================================================

    total_alumni = len(filtered_df)

    employed = 0
    if "JOB STATUS" in filtered_df.columns:
        employed = (
            filtered_df["JOB STATUS"]
            .eq("BEKERJA SEPENUH MASA")
            .sum()
        )

    employment_rate = (
        employed / total_alumni * 100
        if total_alumni > 0 else 0
    )

    average_salary = (
        salary_df["SALARY"].mean()
        if len(salary_df) > 0 else 0
    )

    highest_salary = (
        salary_df["SALARY"].max()
        if len(salary_df) > 0 else 0
    )

    top_program = "-"

    if (
        "PROGRAM NAME" in filtered_df.columns
        and len(filtered_df) > 0
    ):
        top_program = (
            filtered_df["PROGRAM NAME"]
            .value_counts()
            .idxmax()
        )

    st.subheader("Executive Summary")

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric(
        "Total Alumni",
        f"{total_alumni:,}"
    )

    k2.metric(
        "Employment Rate",
        f"{employment_rate:.1f}%"
    )

    k3.metric(
        "Average Salary",
        f"RM {average_salary:,.0f}"
    )

    k4.metric(
        "Highest Salary",
        f"RM {highest_salary:,.0f}"
    )

    k5.metric(
        "Top Program",
        top_program
    )

    # =================================================
    # ROW 1
    # =================================================

    c1, c2 = st.columns(2)

    with c1:

        if "YEAR GRAD" in filtered_df.columns:

            trend = (
                filtered_df.groupby("YEAR GRAD")
                .size()
                .reset_index(name="Count")
            )

            fig1 = px.line(
                trend,
                x="YEAR GRAD",
                y="Count",
                markers=True,
                title="Graduation Trend"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

    with c2:

        if "PROGRAM NAME" in filtered_df.columns:

            top_programs = (
                filtered_df["PROGRAM NAME"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            top_programs.columns = [
                "Program",
                "Count"
            ]

            fig2 = px.bar(
                top_programs,
                x="Count",
                y="Program",
                orientation="h",
                title="Top Programs"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    # =================================================
    # ROW 2
    # =================================================

    c3, c4 = st.columns(2)

    with c3:

        if len(salary_df) > 0:

            fig3 = px.histogram(
                salary_df,
                x="SALARY",
                nbins=20,
                title="Salary Distribution"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

    with c4:

        if (
            "PROGRAM NAME" in salary_df.columns
            and len(salary_df) > 0
        ):

            top_salary = (
                salary_df.groupby("PROGRAM NAME")["SALARY"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            fig4 = px.bar(
                top_salary,
                x="SALARY",
                y="PROGRAM NAME",
                orientation="h",
                title="Top Earning Programs"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

    # =================================================
    # ROW 3
    # =================================================

    c5, c6 = st.columns(2)

    with c5:

        if "STATE" in filtered_df.columns:

            state_df = (
                filtered_df["STATE"]
                .value_counts()
                .head(10)
                .reset_index()
            )

            state_df.columns = [
                "State",
                "Count"
            ]

            fig5 = px.bar(
                state_df,
                x="Count",
                y="State",
                orientation="h",
                title="Top States"
            )

            st.plotly_chart(
                fig5,
                use_container_width=True
            )

    with c6:

        if (
            "PROGRAM NAME" in salary_df.columns
            and "GENDER" in salary_df.columns
            and len(salary_df) > 0
        ):

            heatmap_df = pd.pivot_table(
                salary_df,
                values="SALARY",
                index="PROGRAM NAME",
                columns="GENDER",
                aggfunc="mean"
            )

            fig6 = px.imshow(
                heatmap_df,
                aspect="auto",
                title="Salary Heatmap"
            )

            st.plotly_chart(
                fig6,
                use_container_width=True
            )

    # =================================================
    # DOWNLOAD DATA
    # =================================================

    st.subheader("Download Data")

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered CSV",
        data=csv,
        file_name="filtered_alumni.csv",
        mime="text/csv"
    )

    # =================================================
    # DATA PREVIEW
    # =================================================

    with st.expander("Preview Dataset"):
        st.dataframe(
            filtered_df,
            use_container_width=True
        )

else:
    st.info(
        "Upload gpcombined.csv to begin analysis."
    )
