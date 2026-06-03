import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Alumni Analytics Dashboard",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f5f5f5;
}

.kpi-card {
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    color: white;
    font-weight: bold;
}

.insight-box {
    background-color: white;
    border-left: 5px solid #1f4e79;
    padding: 10px;
    border-radius: 5px;
}

.footer-box {
    background-color: #1f4e79;
    color: white;
    padding: 10px;
    border-radius: 5px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="
background-color:#1f4e79;
padding:15px;
border-radius:8px;
color:white;">
<h2>PSH Alumni Analytics Dashboard — UMPSA Advanced Education Sdn. Bhd.</h2>
<p>Data Sharing Act 2025 (Act 864) Compliant · Powered by Streamlit · 2023–2025</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# KPI ROW
# =====================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi-card" style="background-color:#1f4e79;">
    <h5>Total Alumni</h5>
    <h1>4,280</h1>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-card" style="background-color:#3b6e22;">
    <h5>Employment Rate</h5>
    <h1>88.7%</h1>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-card" style="background-color:#a14f07;">
    <h5>Avg. Monthly Salary</h5>
    <h1>RM 3,842</h1>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-card" style="background-color:#4b2c82;">
    <h5>Top Program</h5>
    <h3>Technical & Engineering</h3>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =====================================================
# ROW 1
# =====================================================

col1, col2 = st.columns(2)

with col1:

    trend_df = pd.DataFrame({
        "Year":[2023,2024,2025],
        "Alumni":[1447,1717,1116]
    })

    fig1 = px.line(
        trend_df,
        x="Year",
        y="Alumni",
        markers=True,
        title="Alumni Enrolment Trend (2023–2025)"
    )

    fig1.update_layout(height=300)

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    salary_df = pd.DataFrame({
        "Gender":["Male","Female"],
        "Salary":[4124,3287]
    })

    fig2 = px.bar(
        salary_df,
        x="Gender",
        y="Salary",
        text="Salary",
        color="Gender",
        title="Average Monthly Salary by Gender (RM)"
    )

    fig2.update_layout(
        showlegend=False,
        height=300
    )

    st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# ROW 2
# =====================================================

col3, col4 = st.columns(2)

with col3:

    job_df = pd.DataFrame({
        "Job Field":[
            "Professional & Scientific",
            "Manufacturing",
            "Mining",
            "Transport",
            "Others"
        ],
        "Count":[2674,660,282,205,127]
    })

    fig3 = px.bar(
        job_df,
        x="Count",
        y="Job Field",
        orientation="h",
        title="Enrolment by Job Field"
    )

    fig3.update_layout(height=300)

    st.plotly_chart(fig3, use_container_width=True)

with col4:

    st.markdown("""
    ### AHP Decision Summary

    🥇 **Technical & Engineering**  
    Score: **0.4187**

    🥈 **Professional Programs**  
    Score: **0.3524**

    🥉 **Management & Business**  
    Score: **0.2289**

    ---
    
    ### Recommended Program
    
    **Technical & Engineering**

    Consistency Ratio (CR): **0.0318**

    ✔ CR < 0.10

    ✔ Judgements Accepted
    """)

# =====================================================
# ROW 3
# =====================================================

col5, col6 = st.columns(2)

with col5:

    st.markdown("""
    ### Regression Results Summary

    #### Significant Predictors

    ✅ Gender

    ✅ Program Type

    ✅ Employment Status

    #### Non-Significant

    ❌ Age

    ---
    
    The MLR model identified statistically
    significant relationships between
    employment outcomes and selected
    demographic and program variables.
    """)

with col6:

    st.markdown("""
    ### Decision Support Insights

    • Employment rate remains high at 88.7%

    • Technical & Engineering programs
      achieved the highest AHP score

    • Professional & Scientific Activities
      dominate employment outcomes

    • Gender salary gap identified

    • Supports evidence-based
      curriculum planning

    • Enables AI-assisted
      decision support
    """)

# =====================================================
# FOOTER
# =====================================================

st.write("")

st.markdown("""
<div class="footer-box">

<b>NAIO Deliverable 7 Compliant</b><br>

AI Code of Ethics Compliant<br>

Data Sharing Act 2025 (Act 864) Compliant<br><br>

Cloud Architecture:<br>

Google Colab → Google Sheets → Dashboard<br><br>

UMPSA Advanced Education Sdn. Bhd.

</div>
""", unsafe_allow_html=True)
