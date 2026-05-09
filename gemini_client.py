import time
import google.generativeai as genai

from config import (
    GEMINI_API_KEY,
    PRIMARY_MODEL,
    FALLBACK_MODEL
)

genai.configure(api_key=GEMINI_API_KEY)

PRIMARY = genai.GenerativeModel(PRIMARY_MODEL)
FALLBACK = genai.GenerativeModel(FALLBACK_MODEL)


def is_bad_response(text):

    bad = [
        "429",
        "quota",
        "rate limit",
        "exceeded",
        "resource exhausted",
        "api key expired",
        "permission denied"
    ]

    text_lower = text.lower()

    return any(x in text_lower for x in bad)


def generate(prompt, retries=5):

    for attempt in range(retries):

        try:

            response = PRIMARY.generate_content(prompt)

            if hasattr(response, "text"):

                text = response.text.strip()

                if not is_bad_response(text):
                    return text

        except Exception as e:

            err = str(e)

            print(f"PRIMARY ERROR: {err}")

        # fallback model
        try:

            response = FALLBACK.generate_content(prompt)

            if hasattr(response, "text"):

                text = response.text.strip()

                if not is_bad_response(text):
                    return text

        except Exception as e:

            print(f"FALLBACK ERROR: {e}")

        wait_time = (attempt + 1) * 15

        print(f"WAITING {wait_time}s")

        time.sleep(wait_time)

    return """
تعذر إنشاء هذا القسم بسبب تجاوز حدود Gemini API.

يرجى إعادة المحاولة لاحقاً أو تغيير API KEY.
"""
