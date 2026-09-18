def generate_roadmap(missing_skills):

    roadmap = []

    learning_order = [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Deep Learning",
        "NLP",
        "Transformers",
        "Hugging Face",
        "OpenCV",
        "Computer Vision",
        "CNN",
        "YOLO",
        "FastAPI",
        "APIs",
        "Docker",
        "Git",
        "GitHub",
        "Power BI",
        "Tableau",
        "MongoDB",
        "MySQL",
        "AWS",
        "Azure",
        "LLM",
        "RAG"
    ]

    # Put skills in a sensible learning order
    ordered_missing = []

    for skill in learning_order:
        for missing in missing_skills:

            if skill.lower() == missing.lower():
                ordered_missing.append(missing)

    # Add any skills not included in our predefined order
    for missing in missing_skills:

        if missing not in ordered_missing:
            ordered_missing.append(missing)

    # Generate roadmap
    for i, skill in enumerate(ordered_missing):

        week = i + 1

        roadmap.append({
            "week": f"Week {week}",
            "skill": skill,
            "task": f"Learn {skill} fundamentals and complete a small practical project."
        })

    return roadmap