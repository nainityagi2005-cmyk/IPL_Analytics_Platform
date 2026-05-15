import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# LOAD CSS
# -----------------------------------

with open("styles.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -----------------------------------
# PAGE TITLE
# -----------------------------------

st.title("🏆 IPL Team Analysis")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
🏆 Team Analytics
</div>

<div class="hero-subtitle">
Analyze IPL team performance and season wins
</div>

</div>

""",
    unsafe_allow_html=True
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

matches = pd.read_csv(
    "data/matches.csv"
)

# -----------------------------------
# SIDEBAR FILTER
# -----------------------------------

season = st.sidebar.selectbox(

    "Select Season",

    sorted(matches["season"].unique())
)

# -----------------------------------
# FILTER DATA
# -----------------------------------

filtered = matches[
    matches["season"] == season
]

# -----------------------------------
# TEAM WINS
# -----------------------------------

team_wins = (

    filtered["winner"]

    .value_counts()

    .reset_index()
)

team_wins.columns = [

    "Team",

    "Wins"
]

# -----------------------------------
# KPI CARDS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Total Matches</h3>

<h1>{filtered.shape[0]}</h1>

</div>

""",
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Top Team</h3>

<h1>{team_wins.iloc[0]['Team']}</h1>

</div>

""",
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Highest Wins</h3>

<h1>{team_wins.iloc[0]['Wins']}</h1>

</div>

""",
        unsafe_allow_html=True
    )

# -----------------------------------
# CHART SECTION
# -----------------------------------

st.markdown("---")

st.subheader("📈 Team Wins")

st.markdown(
    '<div class="chart-box">',
    unsafe_allow_html=True
)

fig = px.bar(

    team_wins,

    x="Team",

    y="Wins",

    color="Wins"
)

fig.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(color="white")
)

st.plotly_chart(

    fig,

    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# -----------------------------------
# DATA TABLE
# -----------------------------------

st.markdown("---")

st.subheader("📄 Match Data")

st.dataframe(

    filtered.head(),

    use_container_width=True
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "🏏 IPL Team Analytics Dashboard"
)