import time
import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    MAX_RETRIES,
    RETRY_DELAY
)

genai.configure(api_key=GEMINI_API_KEY)

def build_model(name):

    return genai.GenerativeModel(
        model_name=name,
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 8192
        }
    )

primary = build_model(PRIMARY_MODEL)
fallback = build_model(FALLBACK_MODEL)

def generate(prompt):

    for attempt in range(MAX_RETRIES):

        try:

            response = primary.generate_content(prompt)

            if hasattr(response, "text"):
                return response.text.strip()

        except Exception as e:

            txt = str(e).lower()

            if "429" in txt or "quota" in txt:

                try:
                    response = fallback.generate_content(prompt)

                    if hasattr(response, "text"):
                        return response.text.strip()

                except Exception:
                    pass

                time.sleep(RETRY_DELAY)

            else:

                if attempt == MAX_RETRIES - 1:
                    return f"ERROR: {e}"

    return "فشل توليد المحتوى"