import streamlit as st
import pandas as pd

from groq import Groq

import os

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------



# -----------------------------------
# GROQ CLIENT
# -----------------------------------

client = Groq(

  api_key=st.secrets["GROQ_API_KEY"]
)

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

st.title("🤖 AI Cricket Assistant")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
🤖 AI Cricket Assistant
</div>

<div class="hero-subtitle">
Ask AI anything about IPL teams, players and stats
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

matches = pd.read_csv(
    "data/matches.csv"
)

# -----------------------------------
# USER QUERY
# -----------------------------------

query = st.text_input(

    "Ask your IPL question"
)

# -----------------------------------
# AI ANALYSIS
# -----------------------------------

if st.button("Analyze"):

    with st.spinner(
        "AI is analyzing IPL data..."
    ):

        # -----------------------------------
        # TOP BATSMEN
        # -----------------------------------

        top_batsmen = (

            deliveries.groupby("batter")[
                "batsman_runs"
            ]

            .sum()

            .sort_values(
                ascending=False
            )

            .head(10)

            .to_string()
        )

        # -----------------------------------
        # TOP BOWLERS
        # -----------------------------------

        top_bowlers = (

            deliveries[
                deliveries["is_wicket"] == 1
            ]

            .groupby("bowler")[
                "is_wicket"
            ]

            .sum()

            .sort_values(
                ascending=False
            )

            .head(10)

            .to_string()
        )

        # -----------------------------------
        # TEAM WINS
        # -----------------------------------

        top_teams = (

            matches["winner"]

            .value_counts()

            .head(10)

            .to_string()
        )

        # -----------------------------------
        # AI PROMPT
        # -----------------------------------

        prompt = f"""

You are an expert IPL cricket analyst.

Here are IPL statistics:

Top Batsmen:
{top_batsmen}

Top Bowlers:
{top_bowlers}

Top Teams:
{top_teams}

User Question:
{query}

Give a smart analytical answer
in simple language.

"""

        # -----------------------------------
        # GROQ RESPONSE
        # -----------------------------------

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "user",

                    "content": prompt
                }

            ]
        )

        answer = (

            response
            .choices[0]
            .message.content
        )

        # -----------------------------------
        # SHOW RESULT
        # -----------------------------------

        st.markdown(
            f"""

<div class="kpi-card">

<h2>🤖 AI Response</h2>

<p>{answer}</p>

</div>

""",
            unsafe_allow_html=True
        )

# -----------------------------------
# SAMPLE QUESTIONS
# -----------------------------------

st.markdown("---")

st.subheader("🔥 Example Questions")

st.info("Who is the best IPL batsman?")

st.info("Which team has most wins?")

st.info("Compare Virat Kohli and Rohit Sharma")

st.info("Who is best finisher in IPL?")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "🏏 Powered by Groq AI + LLaMA 3"
)