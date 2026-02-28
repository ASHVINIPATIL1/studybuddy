from groq import Groq
from django.conf import settings
import json
import re

client = Groq(api_key=settings.GROQ_API_KEY)

def extract_text_from_pdf(file_path):
    import fitz
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def generate_mcq_questions(text, num_questions=10):
    prompt = f"""
    You are Study-Buddy, an expert exam-focused AI teacher.

    Your task:
    Generate {num_questions} high-quality multiple choice questions strictly based on the provided study material.

    Rules:
    1. Questions must test understanding, not just definition recall.
    2. Include a mix of:
    - Conceptual questions
    - Application-based questions
    - Analytical reasoning questions
    3. Avoid vague or trivial questions.
    4. All options must be realistic and plausible.
    5. Only ONE correct answer.
    6. Distribute difficulty as:
    - 30% easy
    - 50% medium
    - 20% hard
    7. If material is insufficient, generate fewer but high-quality questions.

    Output format:
    Return ONLY valid JSON.
    No markdown.
    No explanations outside JSON.

    [
    {{
        "question": "Clear and specific question?",
        "option_a": "Option A",
        "option_b": "Option B",
        "option_c": "Option C",
        "option_d": "Option D",
        "correct_answer": "a",
        "explanation": "Why the correct answer is correct and why others are wrong.",
        "difficulty": "easy | medium | hard",
        "topic": "Main topic from material",
        "cognitive_level": "recall | understanding | application | analysis"
    }}
    ]

    Important:
    - Keep questions concise.
    - Avoid repeating similar questions.
    - Use only information present in the study material.

    Study Material:
    {text[:8000]}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    response_text = response.choices[0].message.content.strip()
    response_text = re.sub(r'```json|```', '', response_text).strip()
    return json.loads(response_text)

def generate_flashcards(text, num_cards=10):
    prompt = f"""
    You are Study-Buddy, an intelligent academic learning assistant.

    Your task:
    Generate {num_cards} high-quality flashcards strictly based on the study material provided.

    Flashcard Rules:
    1. Cover the most important concepts, definitions, formulas, processes, and key facts.
    2. Do NOT create information that is not present in the material.
    3. Avoid repeating similar flashcards.
    4. Keep the "front" short and clear (one concept per card).
    5. Keep the "back" concise but informative (2–4 lines max).
    6. If the material is insufficient, generate fewer but high-quality flashcards.
    7. Mix difficulty levels naturally (easy, medium, hard).

    Return ONLY a valid JSON array.
    Do NOT include markdown.
    Do NOT include explanations outside JSON.

    Format:
    [
    {{
        "front": "Clear question or key term",
        "back": "Clear explanation in simple language",
        "topic": "Main topic name",
        "difficulty": "easy | medium | hard"
    }}
    ]

    Study Material:
    {text[:8000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    response_text = response.choices[0].message.content.strip()
    response_text = re.sub(r'```json|```', '', response_text).strip()
    return json.loads(response_text)

def chat_with_material(text, user_message, chat_history=[]):
    messages = [
        {"role": "system", "content": f"""You are a helpful study assistant. Answer questions strictly based on the study material below (do not answer the question if the topic of question is too unrelated to the material provided "eg -: Material = DSA , Question = HTML , How to cook". Though you can answer the questions which are closely related to the topic). Be concise, clear and helpful.

Study Material:
{text[:6000]}"""}
    ]
    for msg in chat_history[-6:]:
        messages.append({"role": msg['role'], "content": msg['content']})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()