```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="UMPSA Alumni Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.main {
    padding-top: 0.5rem;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 10px;
}

h1 {
    color: #003366;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
col_logo, col_title = st.columns([1,5])

with col_logo:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Universiti_Malaysia_Pahang_logo.svg/512px-Universiti_Malaysia_Pahang_logo.svg.png",
        width=100
    )

with col_title:
    st.title("UMPSA Alumni Analytics Dashboard")
    st.caption("Graduate Employability & Salary Intelligence System")

st.divider()

# --------------------------------------------------
# DATA UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload gpcombined.csv",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df["SALARY"] = pd.to_numeric(
        df["SALARY"],
        errors="coerce"
    )

    # --------------------------------------------------
    # TOP FILTERS
    # --------------------------------------------------
    st.subheader("Filters")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        gender = st.multiselect(
            "Gender",
            sorted(df["GENDER"].dropna().unique()),
            default=list(df["GENDER"].dropna().unique())
        )

    with f2:
        state = st.multiselect(
            "State",
            sorted(df["STATE"].dropna().unique()),
            default=list(df["STATE"].dropna().unique())
        )

    with f3:
        program = st.multiselect(
            "Program Type",
            sorted(df["PROGRAM TYPE"].dropna().unique()),
            default=list(df["PROGRAM TYPE"].dropna().unique())
        )

    with f4:
        status = st.multiselect(
            "Employment Status",
            sorted(df["JOB STATUS"].dropna().unique()),
            default=list(df["JOB STATUS"].dropna().unique())
        )

    df = df[
        (df["GENDER"].isin(gender)) &
        (df["STATE"].isin(state)) &
        (df["PROGRAM TYPE"].isin(program)) &
        (df["JOB STATUS"].isin(status))
    ]

    salary_df = df[df["SALARY"] > 0]

    # --------------------------------------------------
    # KPI ROW
    # --------------------------------------------------
    total = len(df)

    employed = (
        df["JOB STATUS"]
        .eq("BEKERJA SEPENUH MASA")
        .sum()
    )

    emp_rate = (
        employed / total * 100
        if total > 0 else 0
    )

    avg_salary = (
        salary_df["SALARY"].mean()
        if len(salary_df) > 0 else 0
    )

    highest_salary = (
        salary_df["SALARY"].max()
        if len(salary_df) > 0 else 0
    )

    top_program = (
        df["PROGRAM NAME"]
        .value_counts()
        .idxmax()
        if total > 0 else "-"
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total Alumni", f"{total:,}")
    k2.metric("Employment Rate", f"{emp_rate:.1f}%")
    k3.metric("Average Salary", f"RM {avg_salary:,.0f}")
    k4.metric("Highest Salary", f"RM {highest_salary:,.0f}")
    k5.metric("Top Program", top_program)

    st.divider()

    # --------------------------------------------------
    # CHARTS ROW 1
    # --------------------------------------------------
    c1, c2 = st.columns(2)

    with c1:
        trend = (
            df.groupby("YEAR GRAD")
            .size()
            .reset_index(name="Count")
        )

        fig1 = px.line(
            trend,
            x="YEAR GRAD",
            y="Count",
            markers=True,
            title="Employment Trend by Graduation Year"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with c2:

        prog = (
            df["PROGRAM NAME"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        prog.columns = [
            "Program",
            "Count"
        ]

        fig2 = px.bar(
            prog,
            x="Count",
            y="Program",
            orientation="h",
            title="Top Programs"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # --------------------------------------------------
    # CHARTS ROW 2
    # --------------------------------------------------
    c3, c4 = st.columns(2)

    with c3:

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

    # --------------------------------------------------
    # CHARTS ROW 3
    # --------------------------------------------------
    c5, c6 = st.columns(2)

    with c5:

        state_df = (
            df["STATE"]
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
            title="Top States by Alumni"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    with c6:

        heat = pd.pivot_table(
            salary_df,
            values="SALARY",
            index="PROGRAM NAME",
            columns="GENDER",
            aggfunc="mean"
        )

        fig6 = px.imshow(
            heat,
            aspect="auto",
            title="Salary Heatmap"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

    # --------------------------------------------------
    # DOWNLOAD BUTTON
    # --------------------------------------------------
    st.divider()

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Filtered Dataset",
        csv,
        "filtered_alumni.csv",
        "text/csv"
    )

else:
    st.info(
        "Upload gpcombined.csv to display dashboard."
    )
```
