import streamlit as st
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score

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

st.title(" IPL Match Prediction")

# -----------------------------------
# HERO SECTION
# -----------------------------------

st.markdown(
    """

<div class="hero-box">

<div class="hero-title">
 AI Match Prediction
</div>

<div class="hero-subtitle">
Predict IPL winners using Machine Learning
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
# CLEAN DATA
# -----------------------------------

matches = matches.dropna(

    subset=[
        "team1",
        "team2",
        "winner",
        "toss_winner"
    ]
)

# -----------------------------------
# LABEL ENCODER
# -----------------------------------

encoder = LabelEncoder()

teams = pd.concat([

    matches["team1"],

    matches["team2"],

    matches["winner"]

]).unique()

encoder.fit(teams)

# -----------------------------------
# ENCODE COLUMNS
# -----------------------------------

matches["team1_encoded"] = encoder.transform(
    matches["team1"]
)

matches["team2_encoded"] = encoder.transform(
    matches["team2"]
)

matches["toss_encoded"] = encoder.transform(
    matches["toss_winner"]
)

matches["winner_encoded"] = encoder.transform(
    matches["winner"]
)

# -----------------------------------
# FEATURES & TARGET
# -----------------------------------

X = matches[[

    "team1_encoded",

    "team2_encoded",

    "toss_encoded"

]]

y = matches["winner_encoded"]

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42
)

# -----------------------------------
# MODEL
# -----------------------------------

model = RandomForestClassifier()

model.fit(

    X_train,

    y_train
)

# -----------------------------------
# MODEL ACCURACY
# -----------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(

    y_test,

    predictions
)

# -----------------------------------
# USER INPUT
# -----------------------------------

st.sidebar.header("Match Details")

team1 = st.sidebar.selectbox(

    "Select Team 1",

    sorted(teams)
)

team2 = st.sidebar.selectbox(

    "Select Team 2",

    sorted(teams)
)

toss = st.sidebar.selectbox(

    "Toss Winner",

    [team1, team2]
)

# -----------------------------------
# PREDICTION BUTTON
# -----------------------------------

if st.button("Predict Winner"):

    input_data = pd.DataFrame({

        "team1_encoded": [
            encoder.transform([team1])[0]
        ],

        "team2_encoded": [
            encoder.transform([team2])[0]
        ],

        "toss_encoded": [
            encoder.transform([toss])[0]
        ]
    })

    prediction = model.predict(
        input_data
    )

    result = encoder.inverse_transform(
        prediction
    )[0]

    # -----------------------------------
    # RESULT CARD
    # -----------------------------------

    st.markdown(
        f"""

<div class="kpi-card">

<h1> {result}</h1>

<p>Predicted Winner</p>

<p>Model Accuracy: {round(accuracy * 100, 2)}%</p>

</div>

""",
        unsafe_allow_html=True
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    " IPL Match Prediction using Machine Learning"
)