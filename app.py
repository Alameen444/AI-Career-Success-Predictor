# ============================================================
# CareerSense AI - Complete single-file Streamlit application
# Save as app.py in the root of your GitHub repository.
#
# Expected repository:
#   app.py
#   placement_model.pkl   (optional, for placement prediction)
#   train.csv             (optional, for dataset overview)
#   requirements.txt
# ============================================================

import io
import re
import pickle
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore")

# ---------------------------- PAGE SETUP ----------------------------
st.set_page_config(
    page_title="CareerSense AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ROOT = Path(__file__).resolve().parent
MODEL_FILE = ROOT / "placement_model.pkl"
DATA_FILE = ROOT / "train.csv"

# ------------------------------- CSS --------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: Inter, sans-serif; }
    .stApp {
        background:
          radial-gradient(circle at 12% 8%, rgba(37,99,235,.20), transparent 28%),
          radial-gradient(circle at 90% 18%, rgba(124,58,237,.16), transparent 27%),
          linear-gradient(135deg,#080d1c 0%,#101a32 55%,#0b1224 100%);
        color: #f8fafc;
    }
    [data-testid="stHeader"] { background: rgba(8,13,28,.92); }
    [data-testid="stSidebar"] { display:none; }
    .block-container { max-width:1450px; padding-top:1.5rem; padding-bottom:2rem; }
    h1,h2,h3,h4,p,label { color:#f8fafc; }
    .brand { font-size:2.25rem; font-weight:800; letter-spacing:-1px; }
    .brand span { color:#60a5fa; }
    .subtitle { color:#9fb0ca; margin-top:-8px; }
    .glass {
        background:rgba(255,255,255,.065);
        border:1px solid rgba(255,255,255,.12);
        border-radius:18px;
        padding:20px;
        box-shadow:0 12px 35px rgba(0,0,0,.14);
        transition:transform .2s ease,border-color .2s ease;
    }
    .glass:hover { transform:translateY(-3px); border-color:rgba(96,165,250,.5); }
    .metric-label { color:#9fb0ca; font-size:.88rem; }
    .metric-value { color:white; font-size:1.65rem; font-weight:800; margin-top:6px; }
    .muted { color:#9fb0ca; }
    .pill {
        display:inline-block; padding:5px 10px; margin:3px;
        border-radius:999px; color:#bfdbfe;
        background:rgba(59,130,246,.18);
        border:1px solid rgba(96,165,250,.25); font-size:.82rem;
    }
    div.stButton > button, div.stDownloadButton > button {
        border:0; border-radius:11px; color:white; font-weight:700;
        background:linear-gradient(90deg,#2563eb,#7c3aed);
        padding:.65rem 1.1rem; transition:all .2s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform:translateY(-2px); box-shadow:0 8px 22px #2563eb55; color:white;
    }
    [data-testid="stMetric"] {
        background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.1);
        padding:15px; border-radius:14px;
    }
    div[role="radiogroup"] { gap:8px; }
    div[role="radiogroup"] label {
        background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.1);
        border-radius:10px; padding:8px 12px;
    }
    .footer { text-align:center; color:#73839f; padding:24px 0 8px; font-size:.82rem; }
    hr { border-color:rgba(255,255,255,.14); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------- LOAD FILES ----------------------------
@st.cache_data(show_spinner=False)
def read_csv_file(file_path):
    try:
        path = Path(file_path)
        return pd.read_csv(path) if path.exists() else None
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def read_model(file_path):
    try:
        path = Path(file_path)
        if not path.exists():
            return None, "placement_model.pkl was not found in the repository."
        with open(path, "rb") as file:
            return pickle.load(file), None
    except Exception as exc:
        return None, str(exc)


dataset = read_csv_file(str(DATA_FILE))
model, model_error = read_model(str(MODEL_FILE))


# -------------------------- SESSION DEFAULTS ------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "",
        "degree": "B.Tech",
        "branch": "Computer Science",
        "cgpa": 7.5,
        "interest": "Data Analytics",
        "skills": "Python, SQL, Excel",
        "projects": 1,
        "internships": 0,
        "certifications": 0,
    }

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


# ----------------------------- HELPERS ------------------------------
DOMAINS = [
    "Data Analytics",
    "Data Science",
    "Machine Learning",
    "Software Development",
    "Web Development",
    "Cloud Computing",
    "Cybersecurity",
]

ROADMAPS = {
    "Data Analytics": ["Excel", "SQL", "Python", "Pandas", "Statistics", "Power BI", "Dashboard projects"],
    "Data Science": ["Python", "Statistics", "SQL", "Pandas", "NumPy", "Machine Learning", "Model evaluation"],
    "Machine Learning": ["Python", "Statistics", "NumPy", "Pandas", "Scikit-learn", "Feature engineering", "Model deployment"],
    "Software Development": ["Programming fundamentals", "Data structures", "OOP", "Git", "APIs", "Testing", "Projects"],
    "Web Development": ["HTML", "CSS", "JavaScript", "Frontend framework", "Backend", "Database", "Deployment"],
    "Cloud Computing": ["Linux", "Networking", "Python", "Cloud fundamentals", "Containers", "CI/CD", "Cloud project"],
    "Cybersecurity": ["Networking", "Linux", "Python", "Security fundamentals", "Web security", "SIEM basics", "Practice labs"],
}


def target_column(data):
    if data is None:
        return None
    aliases = {
        "placement_status", "placementstatus", "placed", "placement",
        "status", "target", "result", "label"
    }
    for column in data.columns:
        normalized = str(column).strip().lower().replace(" ", "_")
        if normalized in aliases:
            return column
    if len(data.columns) and data.iloc[:, -1].nunique(dropna=True) <= 10:
        return data.columns[-1]
    return None


def model_features(loaded_model, data):
    names = getattr(loaded_model, "feature_names_in_", None)
    if names is not None:
        return list(names)
    if data is not None:
        target = target_column(data)
        return [column for column in data.columns if column != target]
    return []


def numeric_default(column, data):
    if data is not None and column in data.columns:
        values = pd.to_numeric(data[column], errors="coerce").dropna()
        if not values.empty:
            return float(values.median()), float(values.min()), float(values.max())
    return 0.0, 0.0, 100.0


def resume_text(upload):
    raw = upload.getvalue()
    filename = upload.name.lower()

    if filename.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(raw))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError(
                "Could not read this PDF. Check that it is a text-based PDF "
                f"and that pypdf is installed. Details: {exc}"
            )

    if filename.endswith(".docx"):
        try:
            from docx import Document
            document = Document(io.BytesIO(raw))
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
        except Exception as exc:
            raise ValueError(f"Could not read this DOCX file. Details: {exc}")

    raise ValueError("Upload a PDF, DOCX, or TXT file.")


def review_resume(text):
    text_lower = text.lower()
    keywords = [
        "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
        "machine learning", "scikit-learn", "java", "c++", "html", "css",
        "javascript", "streamlit", "statistics", "data analysis", "spark",
        "hadoop", "communication", "problem solving"
    ]
    found_skills = sorted({skill for skill in keywords if skill in text_lower})
    email_match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone_match = re.findall(r"(?:\+?\d[\d\s().-]{8,}\d)", text)
    headings = ["education", "experience", "projects", "skills", "certifications"]
    found_headings = [heading.title() for heading in headings if heading in text_lower]

    # This is a transparent keyword-based indicator, not a real ATS algorithm.
    score = min(
        100,
        25 + len(found_skills) * 4 + len(found_headings) * 5
        + (10 if email_match else 0) + (5 if phone_match else 0),
    )
    return {
        "score": score,
        "skills": found_skills,
        "email": email_match[0] if email_match else "Not detected",
        "phone": phone_match[0].strip() if phone_match else "Not detected",
        "headings": found_headings,
        "words": len(text.split()),
    }


# ------------------------------- HEADER -----------------------------
left, right = st.columns([4, 1])
with left:
    st.markdown('<div class="brand">CareerSense <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Intelligent Career Guidance Platform</div>', unsafe_allow_html=True)
with right:
    current_name = st.session_state.profile.get("name") or "Guest User"
    st.markdown(
        f'<div class="glass" style="text-align:center;padding:12px">👤 {current_name}</div>',
        unsafe_allow_html=True,
    )

st.write("")
page = st.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Student Profile",
        "📈 Placement Prediction",
        "🎯 Domain Recommendation",
        "📄 Resume Analyzer",
        "🧠 Skill Gap Analysis",
        "📊 Career Report",
        "ℹ️ About",
    ],
    horizontal=True,
    label_visibility="collapsed",
)
st.divider()

# =============================== DASHBOARD ==========================
if page == "🏠 Dashboard":
    profile = st.session_state.profile
    st.title("Welcome to CareerSense AI")
    st.write("Understand your strengths, estimate placement readiness, and plan your next career steps.")

    metrics = st.columns(4)
    cards = [
        ("Student", profile["name"] or "Not set"),
        ("CGPA", f'{profile["cgpa"]:.2f}'),
        ("Projects", str(profile["projects"])),
        ("Internships", str(profile["internships"])),
    ]
    for column, (label, value) in zip(metrics, cards):
        with column:
            st.markdown(
                f'<div class="glass"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.subheader("Your career snapshot")
    first, second = st.columns(2)
    with first:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Career interest")
        st.write(profile["interest"])
        st.markdown("#### 💻 Current skills")
        skill_items = [item.strip() for item in profile["skills"].split(",") if item.strip()]
        st.markdown(
            "".join(f'<span class="pill">{item}</span>' for item in skill_items)
            or '<span class="muted">Add skills in your profile.</span>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with second:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("#### 🚀 Recommended actions")
        st.write("1. Complete your student profile.")
        st.write("2. Check placement prediction when the trained model is available.")
        st.write("3. Upload your resume for a keyword-based review.")
        st.write("4. Identify missing skills for your target domain.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Project data")
    d1, d2, d3 = st.columns(3)
    d1.metric("Training records", f"{len(dataset):,}" if dataset is not None else "Not loaded")
    d2.metric("Dataset columns", len(dataset.columns) if dataset is not None else "—")
    detected_target = target_column(dataset)
    d3.metric("Detected target column", str(detected_target) if detected_target else "Not detected")
    if dataset is None:
        st.info("Add train.csv beside app.py in GitHub to display your training dataset overview.")

# ============================ STUDENT PROFILE ======================
elif page == "👤 Student Profile":
    st.title("Student Profile")
    st.write("Enter your academic details and career interests.")
    profile = st.session_state.profile

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full name", value=profile["name"])
            degree_options = ["B.Tech", "B.E", "B.Sc", "BCA", "MCA", "M.Sc", "Other"]
            degree = st.selectbox(
                "Degree",
                degree_options,
                index=degree_options.index(profile["degree"]) if profile["degree"] in degree_options else 0,
            )
            branch = st.text_input("Department / Branch", value=profile["branch"])
            cgpa = st.number_input(
                "CGPA", min_value=0.0, max_value=10.0,
                value=float(profile["cgpa"]), step=0.01,
            )
        with col2:
            interest = st.selectbox(
                "Career interest",
                DOMAINS,
                index=DOMAINS.index(profile["interest"]) if profile["interest"] in DOMAINS else 0,
            )
            skills = st.text_area("Skills (comma separated)", value=profile["skills"])
            projects = st.number_input("Number of projects", min_value=0, max_value=100, value=int(profile["projects"]))
            internships = st.number_input("Number of internships", min_value=0, max_value=20, value=int(profile["internships"]))
            certifications = st.number_input("Number of certifications", min_value=0, max_value=100, value=int(profile["certifications"]))

        submitted = st.form_submit_button("Save Student Profile")

    if submitted:
        st.session_state.profile = {
            "name": name.strip(),
            "degree": degree,
            "branch": branch.strip(),
            "cgpa": cgpa,
            "interest": interest,
            "skills": skills,
            "projects": projects,
            "internships": internships,
            "certifications": certifications,
        }
        st.success("Profile saved for this browser session.")
        st.rerun()

# ========================== PLACEMENT PREDICTION ===================
elif page == "📈 Placement Prediction":
    st.title("AI Placement Prediction")
    st.write("This section uses your saved machine-learning model, if it is compatible with the input fields.")
    if model is None:
        st.error("The placement model is not available.")
        st.caption(f"Expected model location: {MODEL_FILE}")
        st.info("Upload placement_model.pkl to the same root folder as app.py.")
    else:
        features = model_features(model, dataset)
        if not features:
            st.error("Could not identify the model's input feature names.")
            st.write("Save the model with feature names, or provide train.csv with the training feature columns.")
        else:
            st.caption("Input columns detected from the model/data: " + ", ".join(map(str, features)))
            st.warning(
                "For a valid prediction, the values and encoding must match the exact preprocessing "
                "used when training placement_model.pkl."
            )
            inputs = {}
            col_list = st.columns(2)
            for index, feature in enumerate(features):
                target_col = col_list[index % 2]
                label = str(feature).replace("_", " ").title()
                with target_col:
                    if dataset is not None and feature in dataset.columns:
                        series = dataset[feature].dropna()
                    else:
                        series = pd.Series(dtype="object")

                    if not series.empty and pd.api.types.is_numeric_dtype(series):
                        default, minimum, maximum = numeric_default(feature, dataset)
                        inputs[feature] = st.number_input(
                            label,
                            min_value=float(minimum),
                            max_value=float(maximum),
                            value=float(default),
                            key=f"model_input_{feature}",
                        )
                    elif not series.empty:
                        choices = sorted(series.astype(str).unique().tolist())
                        inputs[feature] = st.selectbox(
                            label, choices, key=f"model_input_{feature}"
                        )
                    else:
                        inputs[feature] = st.text_input(label, key=f"model_input_{feature}")

            if st.button("Predict Placement", type="primary"):
                try:
                    input_frame = pd.DataFrame([inputs], columns=features)

                    # Convert categorical values to integer category codes only
                    # when the training CSV confirms that the feature is categorical.
                    if dataset is not None:
                        for feature in features:
                            if feature in dataset.columns and not pd.api.types.is_numeric_dtype(dataset[feature]):
                                categories = sorted(dataset[feature].dropna().astype(str).unique().tolist())
                                if categories:
                                    mapping = {value: idx for idx, value in enumerate(categories)}
                                    input_frame[feature] = input_frame[feature].astype(str).map(mapping).fillna(0)

                    result = model.predict(input_frame)[0]
                    result_text = str(result)
                    st.session_state.prediction_result = result_text
                    st.success(f"Model prediction: **{result_text}**")

                    if hasattr(model, "predict_proba"):
                        probabilities = model.predict_proba(input_frame)[0]
                        classes = getattr(model, "classes_", range(len(probabilities)))
                        probability_df = pd.DataFrame({
                            "Class": [str(item) for item in classes],
                            "Probability": [f"{float(prob) * 100:.2f}%" for prob in probabilities],
                        })
                        st.dataframe(probability_df, use_container_width=True, hide_index=True)

                    st.caption("This is a model estimate, not a guarantee of employment.")
                except Exception as exc:
                    st.error("Prediction failed. The model's expected feature format may differ from the supplied inputs.")
                    st.exception(exc)

# ========================== DOMAIN RECOMMENDATION ==================
elif page == "🎯 Domain Recommendation":
    st.title("Career Domain Recommendation")
    profile = st.session_state.profile
    selected_domain = st.selectbox(
        "Select your target domain",
        DOMAINS,
        index=DOMAINS.index(profile["interest"]) if profile["interest"] in DOMAINS else 0,
    )
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader(f"Learning roadmap: {selected_domain}")
    for number, skill in enumerate(ROADMAPS[selected_domain], start=1):
        st.write(f"**{number}.** {skill}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("This is a general roadmap. Prioritize skills that appear repeatedly in job descriptions for your target role.")

# ============================== RESUME =============================
elif page == "📄 Resume Analyzer":
    st.title("Resume Analyzer")
    st.write("Upload a text-based PDF, DOCX, or TXT resume for a basic keyword review.")
    uploaded_resume = st.file_uploader("Choose your resume", type=["pdf", "docx", "txt"])
    if uploaded_resume is not None:
        try:
            extracted = resume_text(uploaded_resume)
            if not extracted.strip():
                st.warning("No selectable text was found. A scanned PDF may require OCR before analysis.")
            else:
                review = review_resume(extracted)
                a, b, c = st.columns(3)
                a.metric("Indicative keyword score", f'{review["score"]}/100')
                b.metric("Words detected", review["words"])
                c.metric("Skills detected", len(review["skills"]))
                st.subheader("Contact information")
                st.write(f'**Email:** {review["email"]}')
                st.write(f'**Phone:** {review["phone"]}')
                st.subheader("Detected skills")
                st.write(", ".join(review["skills"]) if review["skills"] else "No supported skills detected.")
                st.subheader("Detected resume sections")
                st.write(", ".join(review["headings"]) if review["headings"] else "No standard section headings detected.")
                st.warning("This is a simple keyword-based indicator, not a real commercial ATS score or a shortlisting prediction.")
        except Exception as exc:
            st.error(str(exc))

# ============================ SKILL GAP ============================
elif page == "🧠 Skill Gap Analysis":
    st.title("Skill Gap Analysis")
    profile = st.session_state.profile
    selected_domain = st.selectbox(
        "Target domain",
        DOMAINS,
        index=DOMAINS.index(profile["interest"]) if profile["interest"] in DOMAINS else 0,
    )
    current_skills = st.text_area(
        "Your current skills (comma separated)",
        value=profile["skills"],
    )

    if st.button("Analyze Skill Gap", type="primary"):
        current = {item.strip().lower() for item in current_skills.split(",") if item.strip()}
        required = ROADMAPS[selected_domain]
        matched = [skill for skill in required if skill.lower() in current]
        missing = [skill for skill in required if skill.lower() not in current]
        readiness = round((len(matched) / len(required)) * 100) if required else 0

        x, y, z = st.columns(3)
        x.metric("Skill readiness", f"{readiness}%")
        y.metric("Matched skills", len(matched))
        z.metric("Skills to develop", len(missing))
        st.progress(readiness / 100)
        st.subheader("Skills you already have")
        st.write(", ".join(matched) if matched else "No matching skills found yet.")
        st.subheader("Skills to develop")
        if missing:
            for skill in missing:
                st.write(f"• {skill}")
        else:
            st.success("You have listed all skills in this basic roadmap.")

# ============================== REPORT ============================
elif page == "📊 Career Report":
    st.title("Career Report")
    profile = st.session_state.profile
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader(profile["name"] or "Student Career Summary")
    st.write(f'**Degree:** {profile["degree"]} — {profile["branch"]}')
    st.write(f'**CGPA:** {profile["cgpa"]:.2f}')
    st.write(f'**Career interest:** {profile["interest"]}')
    st.write(f'**Projects:** {profile["projects"]} | **Internships:** {profile["internships"]} | **Certifications:** {profile["certifications"]}')
    st.write(f'**Skills:** {profile["skills"]}')
    st.write(f'**Latest model output:** {st.session_state.prediction_result or "Not generated"}')
    st.markdown("</div>", unsafe_allow_html=True)

    report = (
        "CareerSense AI - Career Report\n"
        "================================\n"
        f'Name: {profile["name"]}\n'
        f'Degree: {profile["degree"]}\n'
        f'Branch: {profile["branch"]}\n'
        f'CGPA: {profile["cgpa"]}\n'
        f'Career interest: {profile["interest"]}\n'
        f'Skills: {profile["skills"]}\n'
        f'Projects: {profile["projects"]}\n'
        f'Internships: {profile["internships"]}\n'
        f'Certifications: {profile["certifications"]}\n'
        f'Latest model output: {st.session_state.prediction_result or "Not generated"}\n'
    )
    st.download_button(
        "Download Career Report",
        data=report,
        file_name="CareerSense_Career_Report.txt",
        mime="text/plain",
    )

# ================================ ABOUT ============================
elif page == "ℹ️ About":
    st.title("About CareerSense AI")
    st.markdown(
        """
        <div class="glass">
          <h3>Intelligent Career Guidance Platform</h3>
          <p>CareerSense AI combines student profile management, machine-learning
          placement prediction, career-domain roadmaps, resume keyword review,
          and skill-gap guidance in one Streamlit application.</p>
          <p><b>Core technologies:</b> Python, Streamlit, Pandas, NumPy, and a
          trained scikit-learn-compatible model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader("Repository files")
    st.write(f"app.py: {'Available' if (ROOT / 'app.py').exists() else 'Missing'}")
    st.write(f"placement_model.pkl: {'Available' if MODEL_FILE.exists() else 'Missing'}")
    st.write(f"train.csv: {'Available' if DATA_FILE.exists() else 'Missing'}")
    if model_error:
        st.caption(f"Model loading information: {model_error}")

# ------------------------------- FOOTER ----------------------------
st.markdown(
    '<div class="footer">CareerSense AI · Intelligent Career Guidance System · Built with Python and Streamlit</div>',
    unsafe_allow_html=True,
)
