import pandas as pd
import re
from pathlib import Path


# Get project directory safely
BASE_DIR = Path(__file__).resolve().parent
SKILL_FILE = BASE_DIR / "data" / "skill_dictionary.csv"


def load_skills():
    """Load the controlled skill dictionary."""

    df = pd.read_csv(SKILL_FILE)

    # Make sure column names are clean
    df.columns = df.columns.str.strip()

    return df


def normalize_skill(skill):
    """Normalize skill names for comparison."""

    skill = str(skill).strip().lower()

    aliases = {
        "c++": "cpp",
        "c#": "csharp",
        ".net": "dotnet",
        "powerbi": "power bi",
        "power bi": "power bi",
        "machine-learning": "machine learning",
        "deep-learning": "deep learning"
    }

    return aliases.get(skill, skill)


def extract_skills(text):
    """Find skills present in the resume."""

    if not text:
        return []

    df = load_skills()

    text_lower = text.lower()

    found_skills = []
    already_found = set()

    for _, row in df.iterrows():

        original_skill = str(row["skill"]).strip()

        normalized_skill = normalize_skill(original_skill)

        # Search version
        search_skill = normalized_skill

        # Special cases
        if normalized_skill == "cpp":
            pattern = r"(?<!\w)c\+\+(?!\w)|(?<!\w)cpp(?!\w)"

        elif normalized_skill == "csharp":
            pattern = r"(?<!\w)c#(?!\w)|(?<!\w)csharp(?!\w)"

        elif normalized_skill == "dotnet":
            pattern = r"(?<!\w)\.net(?!\w)|(?<!\w)dotnet(?!\w)"

        elif normalized_skill == "power bi":
            pattern = r"(?<!\w)power\s*bi(?!\w)"

        else:
            # Escape special characters
            escaped = re.escape(search_skill)

            pattern = rf"(?<!\w){escaped}(?!\w)"

        if re.search(pattern, text_lower):

            skill_key = normalize_skill(original_skill)

            if skill_key not in already_found:

                found_skills.append({
                    "skill": original_skill,
                    "category": row["category"]
                })

                already_found.add(skill_key)

    return found_skills


def analyze_skill_gap(resume_skills, required_skills):
    """Compare resume skills with required job skills."""

    resume_skill_names = {
        normalize_skill(item["skill"])
        for item in resume_skills
    }

    matched = []
    missing = []

    for skill in required_skills:

        normalized_required = normalize_skill(skill)

        if normalized_required in resume_skill_names:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing