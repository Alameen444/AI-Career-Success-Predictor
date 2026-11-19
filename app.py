# app.py

import streamlit as st
import os

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="CareerSense AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------
# SESSION STATE
# --------------------------------

if "student" not in st.session_state:
    st.session_state["student"] = {}

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #080d1c, #101a35, #111827);
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

.brand-title {
    font-size: 35px;
    font-weight: 800;
    color: white;
}

.brand-title span {
    color: #60a5fa;
}

.brand-subtitle {
    color: #94a3b8;
    font-size: 13px;
}

.user-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 12px 18px;
    border-radius: 15px;
    text-align: center;
}

div[data-testid="stNavigation"] {
    background: rgba(255,255,255,0.05);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(37,99,235,0.4);
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

h1, h2, h3 {
    color: #ffffff;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

header1, header2 = st.columns([4, 1])

with header1:

    logo_path = "assets/logo.png"

    if os.path.exists(logo_path):
        st.image(logo_path, width=75)

    st.markdown("""
        <div class="brand-title">
            CareerSense <span>AI</span>
        </div>
        <div class="brand-subtitle">
            Your Intelligent Career Guidance Platform
        </div>
    """, unsafe_allow_html=True)

with header2:

    student = st.session_state.get("student", {})
    username = student.get("name", "Guest User")

    st.markdown(
        f'<div class="user-card">👤 {username}</div>',
        unsafe_allow_html=True
    )

st.divider()

# --------------------------------
# TOP NAVIGATION
# --------------------------------

pages = [

    st.Page(
        "pages/home.py",
        title="Dashboard",
        icon="🏠",
        default=True
    ),

    st.Page(
        "pages/student.py",
        title="Profile",
        icon="👤"
    ),

    st.Page(
        "pages/placement.py",
        title="Placement",
        icon="📈"
    ),

    st.Page(
        "pages/domain.py",
        title="Domain",
        icon="🎯"
    ),

    st.Page(
        "pages/resume.py",
        title="Resume",
        icon="📄"
    ),

    st.Page(
        "pages/skill_gap.py",
        title="Skill Gap",
        icon="🧠"
    ),

    st.Page(
        "pages/portfolio.py",
        title="Portfolio",
        icon="🌐"
    ),

    st.Page(
        "pages/report.py",
        title="Career Report",
        icon="📊"
    ),

    st.Page(
        "pages/about.py",
        title="About",
        icon="ℹ️"
    )

]

navigation = st.navigation(
    pages,
    position="top"
)

navigation.run()

# --------------------------------
# FOOTER
# --------------------------------

st.markdown("""
<hr>

<div style="
    text-align:center;
    color:#64748b;
    padding:20px;
    font-size:13px;
">
    CareerSense AI | Intelligent Career Guidance System
    <br>
    Designed with Python and Streamlit
</div>
""", unsafe_allow_html=True)
