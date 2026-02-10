import os

USE_LLM_CLEANUP = False

class LLMCleaner:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = USE_LLM_CLEANUP and self.api_key is not None

        if self.enabled:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)

    def clean_text(self, text):
        if not self.enabled:
            return text

        prompt = f"""
            You are cleaning OCR text from an exam paper.

            STRICT RULES:
            - DO NOT rewrite, paraphrase, or summarize.
            - DO NOT change wording.
            - ONLY fix OCR errors:
            * broken words (govern- ment → government)
            * incorrect line breaks
            * spacing issues
            - Preserve numbering, options, punctuation.
            - Output must be lexically identical except OCR fixes.

            TEXT:
            {text}
            """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return text
