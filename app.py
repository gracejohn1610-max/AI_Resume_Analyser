import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_text
from text_cleaner import clean_text
from skill_extractor import extract_skills, analyze_skill_gap
from job_matcher import match_jobs
from roadmap_generator import generate_roadmap


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon="📄",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.metric-card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    text-align: center;
}

.skill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 15px;
    background-color: #e8f0fe;
    font-size: 14px;
}

.missing-skill {
    display: inline-block;
    padding: 7px 12px;
    margin: 4px;
    border-radius: 15px;
    background-color: #fff0f0;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📄 AI Resume Analyser</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered Resume Analysis • Job Matching • Skill Gap Detection • Career Roadmap'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Resume Analyzer")

    st.write(
        "Upload your resume to analyse skills, "
        "job compatibility and learning requirements."
    )

    st.divider()

    st.info(
        "Supported formats:\n\n"
        "• PDF\n"
        "• DOCX"
    )

    st.divider()

    st.caption("AI Resume Analyser")
    st.caption("Career Intelligence System")


# ---------------------------------------------------------
# RESUME UPLOAD
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your Resume",
    type=["pdf", "docx"],
    help="Upload a PDF or DOCX resume."
)


# ---------------------------------------------------------
# MAIN PROCESSING
# ---------------------------------------------------------

if uploaded_file is None:

    st.info(
        "👆 Upload a PDF or DOCX resume above to start the analysis."
    )

    # Feature overview
    st.subheader("✨ What this system does")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("### 📄")
        st.write("Resume Parsing")
        st.caption("Extract text from PDF/DOCX resumes.")

    with col2:
        st.markdown("### 🧠")
        st.write("Skill Detection")
        st.caption("Identify technical skills from your resume.")

    with col3:
        st.markdown("### 🎯")
        st.write("Job Matching")
        st.caption("Compare your profile with available roles.")

    with col4:
        st.markdown("### 🚀")
        st.write("Career Roadmap")
        st.caption("Identify missing skills and learning areas.")

    st.stop()


# ---------------------------------------------------------
# EXTRACT RESUME TEXT
# ---------------------------------------------------------

try:

    with st.spinner("📖 Reading your resume..."):

        raw_text = extract_text(uploaded_file)

        cleaned_text = clean_text(raw_text)

    if not cleaned_text:

        st.error(
            "❌ No readable text was found in this resume."
        )

        st.stop()

except Exception as e:

    st.error(
        f"❌ Error reading resume: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# EXTRACT SKILLS
# ---------------------------------------------------------

try:

    with st.spinner("🧠 Detecting skills..."):

        resume_skills = extract_skills(cleaned_text)

except Exception as e:

    st.error(
        f"❌ Error extracting skills: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# CONVERT SKILLS INTO SIMPLE LIST
# ---------------------------------------------------------

skill_names = []

for item in resume_skills:

    if isinstance(item, dict):

        skill = item.get("skill")

        if skill:
            skill_names.append(skill)

    elif isinstance(item, str):

        skill_names.append(item)


# Remove duplicates
skill_names = list(dict.fromkeys(skill_names))


# ---------------------------------------------------------
# JOB MATCHING
# ---------------------------------------------------------

try:

    with st.spinner("🎯 Matching your resume with job roles..."):

        job_results = match_jobs(
            cleaned_text,
            skill_names
        )

except Exception as e:

    st.error(
        f"❌ Error matching jobs: {e}"
    )

    st.stop()


# ---------------------------------------------------------
# TOP RESULT
# ---------------------------------------------------------

if job_results:

    top_match = job_results[0]

else:

    top_match = {
        "role": "No match",
        "match_score": 0,
        "similarity": 0,
        "skill_score": 0,
        "required_skills": []
    }


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

st.divider()

st.header("📊 Resume Analysis Dashboard")


# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🎯 Top Role",
        top_match["role"]
    )

with col2:

    st.metric(
        "📈 Match Score",
        f'{top_match["match_score"]}%'
    )

with col3:

    st.metric(
        "🧠 Skills Found",
        len(skill_names)
    )

with col4:

    st.metric(
        "💼 Roles Analysed",
        len(job_results)
    )


# ---------------------------------------------------------
# TOP MATCH
# ---------------------------------------------------------

st.subheader("🏆 Recommended Career Role")

st.success(
    f'Your highest matching role is **{top_match["role"]}** '
    f'with a **{top_match["match_score"]}% match score**.'
)


# ---------------------------------------------------------
# SKILLS FOUND
# ---------------------------------------------------------

st.subheader("🧠 Skills Detected in Your Resume")

if skill_names:

    skills_html = ""

    for skill in skill_names:

        skills_html += (
            f'<span class="skill">{skill}</span>'
        )

    st.markdown(
        skills_html,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "No skills were detected. Try uploading a resume with a skills section."
    )


# ---------------------------------------------------------
# JOB MATCHING TABLE
# ---------------------------------------------------------

st.divider()

st.subheader("🎯 Job Role Matching")

if job_results:

    table_data = []

    for result in job_results:

        table_data.append({
            "Job Role": result["role"],
            "Match Score": result["match_score"],
            "Skill Coverage": result["skill_score"],
            "Text Similarity": result["similarity"]
        })

    df_results = pd.DataFrame(table_data)

    st.dataframe(
        df_results,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# JOB MATCHING CHART
# ---------------------------------------------------------

st.subheader("📊 Career Match Visualization")

if job_results:

    chart_df = pd.DataFrame([
        {
            "Role": result["role"],
            "Match Score": result["match_score"]
        }
        for result in job_results
    ])

    fig = px.bar(
        chart_df,
        x="Role",
        y="Match Score",
        title="Resume Compatibility by Job Role",
        text="Match Score"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Match Score (%)",
        xaxis_title="Job Role",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------------
# ROLE SELECTION FOR SKILL GAP
# ---------------------------------------------------------

st.divider()

st.subheader("🔍 Skill Gap Analysis")

role_names = [
    result["role"]
    for result in job_results
]

selected_role = st.selectbox(
    "Select a job role to analyse your skill gap:",
    role_names
)


# Find selected role
selected_result = None

for result in job_results:

    if result["role"] == selected_role:

        selected_result = result
        break


# ---------------------------------------------------------
# SKILL GAP
# ---------------------------------------------------------

if selected_result:

    required_skills = selected_result[
        "required_skills"
    ]

    matched_skills, missing_skills = analyze_skill_gap(
        resume_skills,
        required_skills
    )


    col1, col2 = st.columns(2)


    # Matched
    with col1:

        st.markdown("### ✅ Skills You Have")

        if matched_skills:

            for skill in matched_skills:

                st.success(skill)

        else:

            st.write("No matching skills found.")


    # Missing
    with col2:

        st.markdown("### ⚠️ Skills to Develop")

        if missing_skills:

            for skill in missing_skills:

                st.warning(skill)

        else:

            st.success(
                "🎉 You have all the required skills for this role!"
            )


# ---------------------------------------------------------
# LEARNING ROADMAP
# ---------------------------------------------------------

st.divider()

st.subheader("🚀 Personalized Learning Roadmap")


if selected_result:

    missing_skills = analyze_skill_gap(
        resume_skills,
        selected_result["required_skills"]
    )[1]

    if missing_skills:

        roadmap = generate_roadmap(
            missing_skills
        )

        for item in roadmap:

            with st.expander(
                f'📚 {item["week"]} — {item["skill"]}'
            ):

                st.write(
                    item["task"]
                )

    else:

        st.success(
            "No major skill gaps detected for this role."
        )


# ---------------------------------------------------------
# RESUME TEXT PREVIEW
# ---------------------------------------------------------

st.divider()

with st.expander("📄 View Extracted Resume Text"):

    st.write(raw_text)


# ---------------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------------

st.divider()

st.subheader("📥 Download Analysis Report")


report_lines = []

report_lines.append(
    "AI RESUME ANALYSER"
)

report_lines.append(
    "=================="
)

report_lines.append("")

report_lines.append(
    f"Resume: {uploaded_file.name}"
)

report_lines.append("")

report_lines.append(
    f"Top Matching Role: {top_match['role']}"
)

report_lines.append(
    f"Match Score: {top_match['match_score']}%"
)

report_lines.append("")

report_lines.append(
    "SKILLS DETECTED"
)

report_lines.append(
    "---------------"
)

report_lines.extend(
    skill_names
)

report_lines.append("")

report_lines.append(
    "JOB ROLE MATCHES"
)

report_lines.append(
    "----------------"
)

for result in job_results:

    report_lines.append(
        f"{result['role']} - "
        f"{result['match_score']}%"
    )

report_lines.append("")

if selected_result:

    matched_skills, missing_skills = analyze_skill_gap(
        resume_skills,
        selected_result["required_skills"]
    )

    report_lines.append(
        f"SKILL GAP FOR {selected_role}"
    )

    report_lines.append(
        "---------------------------"
    )

    report_lines.append(
        "Matched Skills:"
    )

    report_lines.extend(
        matched_skills
    )

    report_lines.append("")

    report_lines.append(
        "Missing Skills:"
    )

    report_lines.extend(
        missing_skills
    )


report = "\n".join(report_lines)


st.download_button(
    label="📥 Download Resume Analysis Report",
    data=report,
    file_name="resume_analysis_report.txt",
    mime="text/plain"
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI Resume Analyser • Resume Intelligence & Career Guidance System"
)