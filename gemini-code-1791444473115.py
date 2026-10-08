import json
from google import genai
from google.genai import types
import config

def generate_comic_script(prompt: str, style: str, num_panels: int = 4) -> dict:
    """Generates a structured comic story with panel descriptions, captions, and dialogues."""
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    system_instruction = """
    You are a professional comic book writer. Your task is to output a JSON object containing a comic script.
    Ensure consistent character traits and visual style prompts across all panels.
    The response MUST be raw JSON adhering strictly to this schema:
    {
      "title": "Comic Title",
      "characters": ["Name and brief visual description"],
      "panels": [
        {
          "panel_number": 1,
          "visual_description": "Detailed image generation prompt capturing action, lighting, and art style",
          "caption": "Narrator voiceover text",
          "dialogue": "Character Name: 'Speech bubble text'"
        }
      ]
    }
    """

    user_prompt = f"""
    Create a {num_panels}-panel comic story based on this idea: '{prompt}'.
    Art Style: {style}.
    Make sure each panel visual description is self-contained and descriptive enough to generate a coherent panel image.
    """

    response = client.models.generate_content(
        model=config.TEXT_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.7
        )
    )
    
    return json.loads(response.text)