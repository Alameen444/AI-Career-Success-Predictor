import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("placement_model.pkl")

st.set_page_config(
    page_title="AI Career Success Predictor",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Career Success Predictor")
st.write("Predict placement chances and get career recommendations.")

# -----------------------------
# INPUTS
# -----------------------------

student_id = st.number_input("Student ID", 1, 10000, 1)

age = st.number_input("Age", 18, 35, 22)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

degree = st.selectbox(
    "Degree",
    ["B.Tech", "BCA", "MCA", "B.Sc"]
)

branch = st.selectbox(
    "Branch",
    ["ECE", "ME", "Civil", "CSE", "IT"]
)

cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=10.0,
    value=7.5
)

internships = st.number_input(
    "Internships",
    min_value=0,
    max_value=10,
    value=1
)

projects = st.number_input(
    "Projects",
    min_value=0,
    max_value=20,
    value=2
)

coding = st.slider(
    "Coding Skills",
    0,
    100,
    70
)

communication = st.slider(
    "Communication Skills",
    0,
    100,
    70
)

aptitude = st.slider(
    "Aptitude Test Score",
    0,
    100,
    70
)

softskills = st.slider(
    "Soft Skills Rating",
    0,
    100,
    70
)

certifications = st.number_input(
    "Certifications",
    0,
    20,
    1
)

backlogs = st.number_input(
    "Backlogs",
    0,
    10,
    0
)

# -----------------------------------
# IMPORTANT:
# REPLACE THESE WITH YOUR ACTUAL
# LABEL ENCODER VALUES
# -----------------------------------

gender_map = {
    "Female": 0,
    "Male": 1
}

degree_map = {
    "B.Tech": 0,
    "BCA": 1,
    "MCA": 2,
    "B.Sc": 3
}

branch_map = {
    "Civil": 0,
    "CSE": 1,
    "ECE": 2,
    "IT": 3,
    "ME": 4
}

# -----------------------------
# PREDICTION
# -----------------------------

if st.button("Predict Placement"):

    input_df = pd.DataFrame([{
        "Student_ID": student_id,
        "Age": age,
        "Gender": gender_map[gender],
        "Degree": degree_map[degree],
        "Branch": branch_map[branch],
        "CGPA": cgpa,
        "Internships": internships,
        "Projects": projects,
        "Coding_Skills": coding,
        "Communication_Skills": communication,
        "Aptitude_Test_Score": aptitude,
        "Soft_Skills_Rating": softskills,
        "Certifications": certifications,
        "Backlogs": backlogs
    }])

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    placement_probability = max(probability) * 100

    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("✅ PLACED")
    else:
        st.error("❌ NOT PLACED")

    st.info(
        f"Placement Probability: {placement_probability:.2f}%"
    )

    # -----------------------------
    # READINESS SCORE
    # -----------------------------

    score = (
        cgpa * 10 +
        coding * 0.3 +
        communication * 0.2 +
        internships * 5
    )

    if score > 100:
        score = 100

    st.metric(
        "Placement Readiness Score",
        f"{score:.0f}/100"
    )

    # -----------------------------
    # RECOMMENDATIONS
    # -----------------------------

    st.subheader("Career Recommendations")

    if cgpa < 7:
        st.warning(
            "Improve CGPA through academic performance."
        )

    if coding < 70:
        st.warning(
            "Improve coding skills by practicing DSA and projects."
        )

    if communication < 70:
        st.warning(
            "Improve communication and presentation skills."
        )

    if aptitude < 70:
        st.warning(
            "Practice aptitude and reasoning questions."
        )

    if internships == 0:
        st.warning(
            "Try to complete at least one internship."
        )

    if backlogs > 0:
        st.warning(
            "Clear all active backlogs."
        )

    # -----------------------------
    # SKILL GAP ANALYZER
    # -----------------------------

    st.subheader("Skill Gap Analyzer")

    missing_skills = []

    if coding < 70:
        missing_skills.append("Python / DSA")

    if aptitude < 70:
        missing_skills.append("Aptitude")

    if communication < 70:
        missing_skills.append("Communication Skills")

    if internships == 0:
        missing_skills.append("Industry Experience")

    if len(missing_skills) == 0:
        st.success(
            "No major skill gaps detected."
        )
    else:
        for skill in missing_skills:
            st.write("•", skill)