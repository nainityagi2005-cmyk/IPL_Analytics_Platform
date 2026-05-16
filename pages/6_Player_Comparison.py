import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

st.title(" Player Comparison")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
 Player Comparison
</div>

<div class="hero-subtitle">
Compare IPL players side by side
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
# PLAYER LIST
# -----------------------------------

players = sorted(

    deliveries["batter"]

    .dropna()

    .unique()
)

# -----------------------------------
# SELECT PLAYERS
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    player1 = st.selectbox(

        "Select Player 1",

        players
    )

with col2:

    player2 = st.selectbox(

        "Select Player 2",

        players,

        index=1
    )

# -----------------------------------
# PLAYER STATS FUNCTION
# -----------------------------------

def get_player_stats(player):

    player_data = deliveries[

        deliveries["batter"] == player
    ]

    total_runs = player_data[
        "batsman_runs"
    ].sum()

    balls = player_data.shape[0]

    fours = player_data[
        player_data["batsman_runs"] == 4
    ].shape[0]

    sixes = player_data[
        player_data["batsman_runs"] == 6
    ].shape[0]

    strike_rate = round(

        (total_runs / balls) * 100,

        2
    )

    return {

        "Runs": total_runs,

        "Balls": balls,

        "4s": fours,

        "6s": sixes,

        "SR": strike_rate
    }

# -----------------------------------
# GET STATS
# -----------------------------------

stats1 = get_player_stats(player1)

stats2 = get_player_stats(player2)

# -----------------------------------
# PROFILE CARDS
# -----------------------------------

col3, col4 = st.columns(2)

with col3:

    st.markdown(
        f"""

<div class="kpi-card">

<h1>{player1}</h1>

<p>Runs: {stats1['Runs']}</p>

<p>Balls: {stats1['Balls']}</p>

<p>4s: {stats1['4s']}</p>

<p>6s: {stats1['6s']}</p>

<p>SR: {stats1['SR']}</p>

</div>

""",
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""

<div class="kpi-card">

<h1>{player2}</h1>

<p>Runs: {stats2['Runs']}</p>

<p>Balls: {stats2['Balls']}</p>

<p>4s: {stats2['4s']}</p>

<p>6s: {stats2['6s']}</p>

<p>SR: {stats2['SR']}</p>

</div>

""",
        unsafe_allow_html=True
    )

# -----------------------------------
# COMPARISON CHART
# -----------------------------------

st.markdown("---")

st.subheader(" Player Comparison")

fig = go.Figure()

fig.add_trace(

    go.Bar(

        name=player1,

        x=list(stats1.keys()),

        y=list(stats1.values())
    )
)

fig.add_trace(

    go.Bar(

        name=player2,

        x=list(stats2.keys()),

        y=list(stats2.values())
    )
)

fig.update_layout(

    barmode="group",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(color="white")
)

st.plotly_chart(

    fig,

    use_container_width=True
)

# -----------------------------------
# AI INSIGHT
# -----------------------------------

st.markdown("---")

better_player = (

    player1

    if stats1["Runs"] > stats2["Runs"]

    else player2
)

st.success(

    f" Based on total runs, "
    f"{better_player} has stronger batting performance."
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    " IPL Player Comparison Dashboard"
)