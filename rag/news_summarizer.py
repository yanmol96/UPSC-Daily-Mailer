import os
from google import genai


USE_LLM = True

# --- API key handling ---
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not set. Run: export GOOGLE_API_KEY=your_key"
    )

client = genai.Client(api_key=API_KEY)

# ✅ Use a model that is guaranteed to work
MODEL_NAME = "models/gemini-2.5-flash-lite"

SYSTEM_PROMPT = """
You are a UPSC current affairs assistant.

IMPORTANT OUTPUT RULES (STRICT):
- Output ONLY valid HTML
- Do NOT use markdown (*, **, -, #)
- Do NOT insert empty lines
- Do NOT indent text
- Use <p>, <ul>, <li>, <b>, <h4>, <br> only
- Each section must be continuous (no blank gaps)

STRUCTURE (FOLLOW EXACTLY):

<h4>30-Second Summary</h4>
<ul>
<li>Point 1</li>
<li>Point 2</li>
<li>Point 3</li>
<li>Point 4</li>
</ul>

<h4>Prelims Facts</h4>
<ul>
<li>Fact 1</li>
<li>Fact 2</li>
</ul>

<h4>Mains Material</h4>

<b>Introduction:</b>
<p>2–3 lines, GS-style, issue-based introduction.</p>

<b>Body:</b>
<p>~60-second mains answer covering causes, implications, constitutional aspects, governance angle, and examples.</p>

<b>Conclusion & Way Forward:</b>
<p>1–2 line conclusion followed by 2–3 actionable, forward-looking points.</p>

STYLE RULES:
- No journalism tone
- No syllabus listing
- Write like topper notes
- No generic phrases
"""



# def summarize_news(news_text: str) -> str:
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=SYSTEM_PROMPT + "\n\nNEWS:\n" + news_text
#     )
#     return response.text.strip()


def summarize_news(news_text: str) -> str:
    if not USE_LLM:
        return (
            "LLM DISABLED (TEST MODE)\n\n"
            "This is a dummy summary to verify:\n"
            "- daily scraping\n"
            "- ranking\n"
            "- email delivery\n\n"
            "No Gemini API call was made."
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=SYSTEM_PROMPT + "\n\nNEWS:\n" + news_text
    )
    return response.text.strip()
