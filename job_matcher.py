import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


JOB_FILE = "data/job_roles.csv"


def load_jobs():
    """Load job role dataset."""
    return pd.read_csv(JOB_FILE)


def calculate_similarity(resume_text, job_text):
    """Calculate TF-IDF cosine similarity."""

    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity


def calculate_skill_score(resume_skills, required_skills):
    """Calculate percentage of required skills found."""

    if not required_skills:
        return 0

    resume_skills_lower = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_skills_lower = {
        skill.lower().strip()
        for skill in required_skills
    }

    matched = resume_skills_lower.intersection(
        required_skills_lower
    )

    return len(matched) / len(required_skills_lower)


def match_jobs(resume_text, resume_skills):
    """Match resume against all available job roles."""

    jobs = load_jobs()

    results = []

    for _, job in jobs.iterrows():

        required_skills = [
            skill.strip()
            for skill in job["skills"].split(",")
        ]

        # TF-IDF similarity
        similarity = calculate_similarity(
            resume_text,
            job["description"] + " " + job["skills"]
        )

        # Skill coverage
        skill_score = calculate_skill_score(
            resume_skills,
            required_skills
        )

        # Combined score
        final_score = (
            similarity * 0.4 +
            skill_score * 0.6
        )

        results.append({
            "role": job["role"],
            "similarity": round(similarity * 100, 2),
            "skill_score": round(skill_score * 100, 2),
            "match_score": round(final_score * 100, 2),
            "required_skills": required_skills
        })

    # Highest score first
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results