from auth import (
    create_user,
    login_user
)
import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False
# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="IPL Analytics",

    page_icon="cricket.jpeg",

    layout="wide"
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
# AUTHENTICATION
# -----------------------------------

if not st.session_state.logged_in:

    st.title(" Login To Continue")

    auth_mode = st.sidebar.selectbox(

        "Select Option",

        ["Login", "Signup"]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(

        "Password",

        type="password"
    )

    # -----------------------------------
    # SIGNUP
    # -----------------------------------

    if auth_mode == "Signup":

        if st.button("Create Account"):

            success = create_user(

                username,

                password
            )

            if success:

                st.success(
                    " Account created!"
                )

            else:

                st.error(
                    " Username already exists."
                )

    # -----------------------------------
    # LOGIN
    # -----------------------------------

    if auth_mode == "Login":

        if st.button("Login"):

            valid = login_user(

                username,

                password
            )

            if valid:

                st.session_state.logged_in = True

                st.success(
                    " Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    " Invalid credentials"
                )

    st.stop()

# -----------------------------------
# LOAD DATA
# -----------------------------------

matches = pd.read_csv(
    "data/matches.csv"
)

deliveries = pd.read_csv(
    "data/deliveries.csv"
)

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
IPL Analytics Platform
</div>

<div class="hero-subtitle">
AI Powered Cricket Analytics Dashboard
</div>

</div>

""",
    unsafe_allow_html=True
)

# -----------------------------------
# KPI VALUES
# -----------------------------------

matches_count = matches.shape[0]

teams_count = len(
    pd.concat([
        matches["team1"],
        matches["team2"]
    ]).unique()
)

players_count = len(
    deliveries["batter"].unique()
)

# -----------------------------------
# KPI CARDS
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Total Matches</h3>

<h1>{matches_count}</h1>

</div>

""",
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Total Teams</h3>

<h1>{teams_count}</h1>

</div>

""",
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""

<div class="kpi-card">

<h3>Total Players</h3>

<h1>{players_count}</h1>

</div>

""",
        unsafe_allow_html=True
    )

# -----------------------------------
# FEATURES
# -----------------------------------

st.markdown("---")

st.subheader(" Platform Features")

st.info(" Team Analytics")

st.info(" Player Profiles")

st.info(" Match Winner Prediction")

st.info(" AI Cricket Assistant")

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    " Built with Streamlit, Plotly, Scikit-Learn & Groq AI"
)
# -----------------------------------
# LOGOUT
# -----------------------------------

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()
    