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

st.title(" IPL Team Comparison")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
 Team Comparison
</div>

<div class="hero-subtitle">
Compare IPL team performances side by side
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
# TEAMS
# -----------------------------------

teams = sorted(

    pd.concat([

        matches["team1"],

        matches["team2"]

    ])

    .dropna()

    .unique()
)

# -----------------------------------
# SELECT TEAMS
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    team1 = st.selectbox(

        "Select Team 1",

        teams
    )

with col2:

    team2 = st.selectbox(

        "Select Team 2",

        teams,

        index=1
    )

# -----------------------------------
# TEAM STATS FUNCTION
# -----------------------------------

def get_team_stats(team):

    matches_played = matches[

        (matches["team1"] == team)

        |

        (matches["team2"] == team)

    ].shape[0]

    wins = matches[

        matches["winner"] == team

    ].shape[0]

    toss_wins = matches[

        matches["toss_winner"] == team

    ].shape[0]

    win_percentage = round(

        (wins / matches_played) * 100,

        2
    )

    return {

        "Matches": matches_played,

        "Wins": wins,

        "Toss Wins": toss_wins,

        "Win %": win_percentage
    }

# -----------------------------------
# GET STATS
# -----------------------------------

stats1 = get_team_stats(team1)

stats2 = get_team_stats(team2)

# -----------------------------------
# KPI CARDS
# -----------------------------------

col3, col4 = st.columns(2)

with col3:

    st.markdown(
        f"""

<div class="kpi-card">

<h1>{team1}</h1>

<p>Matches: {stats1['Matches']}</p>

<p>Wins: {stats1['Wins']}</p>

<p>Toss Wins: {stats1['Toss Wins']}</p>

<p>Win %: {stats1['Win %']}%</p>

</div>

""",
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""

<div class="kpi-card">

<h1>{team2}</h1>

<p>Matches: {stats2['Matches']}</p>

<p>Wins: {stats2['Wins']}</p>

<p>Toss Wins: {stats2['Toss Wins']}</p>

<p>Win %: {stats2['Win %']}%</p>

</div>

""",
        unsafe_allow_html=True
    )

# -----------------------------------
# COMPARISON CHART
# -----------------------------------

st.markdown("---")

st.subheader("Team Comparison Chart")

fig = go.Figure()

fig.add_trace(

    go.Bar(

        name=team1,

        x=list(stats1.keys()),

        y=list(stats1.values())
    )
)

fig.add_trace(

    go.Bar(

        name=team2,

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

better_team = (

    team1

    if stats1["Win %"] > stats2["Win %"]

    else team2
)

st.success(

    f" Based on win percentage, "
    f"{better_team} has performed better historically."
)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    " IPL Team Comparison Dashboard"
)