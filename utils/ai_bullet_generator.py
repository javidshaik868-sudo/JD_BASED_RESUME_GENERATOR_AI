# utils/ai_bullet_generator.py

# -------------------------------
# 📦 Imports
# -------------------------------
import random
from openai import OpenAI
from utils.openai_client import client

client = OpenAI()

# -------------------------------
# 🤖 AI Experience Bullet Generator
# -------------------------------
def generate_experience_bullets(resume_text, jd_skills, resume_skills=None, doc=None):
    """
    Generate 3–4 professional experience bullet points
    based on newly added JD skills.

    Args:
        resume_text (str): Existing resume content to provide context.
        jd_skills (list): List of newly extracted skills from JD.
        resume_skills (list, optional): Skills already in resume to avoid repetition.
        doc (Document, optional): python-docx Document object to update metadata.

    Returns:
        str: Generated bullet points (ATS optimized).
    """
    if not jd_skills:
        return ""

    # -------------------------------
    # Clean and pick skills
    # -------------------------------
    selected_skills = random.sample(jd_skills, min(len(jd_skills), 4))
    skills_text = ", ".join(selected_skills)

    # -------------------------------
    # Construct prompt for OpenAI
    # -------------------------------
    prompt = f"""
You are an expert ATS resume writer.

Task:
- Use the given skills to generate 3 to 4 professional experience bullet points.

STRICT RULES:
- Use action verbs (Developed, Implemented, Optimized, Designed)
- Make bullets realistic for a software developer
- Each bullet must include at least one of these skills: {skills_text}
- Keep each bullet 1–2 lines
- Do NOT repeat wording
- Do NOT mention "skills" explicitly
- Output ONLY bullet points

Resume Context:
{resume_text}
"""

    try:
        # -------------------------------
        # Call OpenAI Chat API
        # -------------------------------
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate strong ATS resume bullet points."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9  # 🔥 More randomness for creativity
        )

        bullets = response.choices[0].message.content.strip()

        # -------------------------------
        # Add bullets to DOCX if doc object is provided
        # -------------------------------
        if doc:
            for bullet in bullets.split("\n"):
                doc.add_paragraph(bullet, style='List Bullet')

        # -------------------------------
        # Identify new skills to add to resume keywords
        # -------------------------------
        if resume_skills:
            to_add = [s for s in jd_skills if s.lower() not in [x.lower() for x in resume_skills]]
            if doc:
                doc.core_properties.keywords = ", ".join(jd_skills)

        return bullets

    except Exception as e:
        print("OpenAI Error:", e)
        # Fallback bullet point
        return "• Improved system performance and implemented scalable solutions."