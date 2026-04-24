import os

import openai

OPENAI_MODEL = "gpt-3.5-turbo"


def generate_resume_feedback(resume_text: str, top_matches: list) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        return "OpenAI API key is not configured. Set OPENAI_API_KEY in your environment to enable AI feedback."

    prompt = (
        "You are an AI career coach. Analyze the resume text and provide actionable feedback on strengths, weaknesses, and improvements. "
        "Also suggest how to align the resume more closely with the following top job matches:\n\n"
        + "\n\n".join([f"- {job['title']} at {job['company']}: {job['description']}" for job in top_matches[:2]])
        + "\n\nResume text:\n" + resume_text
    )

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You provide concise, friendly resume feedback for job seekers."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=450,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        return f"AI feedback generation failed: {exc}"
