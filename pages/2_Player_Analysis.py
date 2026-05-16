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

st.title("IPL Player Analysis")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
 Player Profiles
</div>

<div class="hero-subtitle">
Analyze IPL player performance and batting stats
</div>

</div>

""",
    unsafe_allow_html=True
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

deliveries = pd.read_csv(
    "data/deliveries.csv"
)

# -----------------------------------
# PLAYER FILTER
# -----------------------------------

players = sorted(

    deliveries["batter"]

    .dropna()

    .unique()
)

selected_player = st.sidebar.selectbox(

    "Select Player",

    players
)

# -----------------------------------
# FILTER PLAYER DATA
# -----------------------------------

player_data = deliveries[

    deliveries["batter"]
    == selected_player
]

# -----------------------------------
# PLAYER STATS
# -----------------------------------

total_runs = player_data["batsman_runs"].sum()

balls_played = player_data.shape[0]

fours = player_data[
    player_data["batsman_runs"] == 4
].shape[0]

sixes = player_data[
    player_data["batsman_runs"] == 6
].shape[0]

strike_rate = round(

    (total_runs / balls_played) * 100,

    2
)

# -----------------------------------
# KPI PROFILE CARD
# -----------------------------------

st.markdown(
    f"""

<div class="kpi-card">

<h1>{selected_player}</h1>

<p>Total Runs: {total_runs}</p>

<p>Balls Played: {balls_played}</p>

<p>Strike Rate: {strike_rate}</p>

<p>Fours: {fours}</p>

<p>Sixes: {sixes}</p>

</div>

""",
    unsafe_allow_html=True
)

# -----------------------------------
# RUN DISTRIBUTION
# -----------------------------------

run_dist = (

    player_data["batsman_runs"]

    .value_counts()

    .reset_index()
)

run_dist.columns = [

    "Runs",

    "Count"
]

# -----------------------------------
# CHART
# -----------------------------------

st.markdown("---")

st.subheader(" Run Distribution")

st.markdown(
    '<div class="chart-box">',
    unsafe_allow_html=True
)

fig = px.bar(

    run_dist,

    x="Runs",

    y="Count",

    color="Count"
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
# PLAYER DATA
# -----------------------------------

st.markdown("---")

st.subheader(" Ball-by-Ball Data")

st.dataframe(

    player_data.head(),

    use_container_width=True
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    " IPL Player Analytics Dashboard"
)