import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Models
TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "imagen-3.0-generate-002"

# Available comic styles
ART_STYLES = [
    "American Superhero Comic",
    "Japanese Manga (Black & White)",
    "Japanese Anime (Vibrant Color)",
    "Retro 1950s Pulp Comic",
    "Cyberpunk Graphic Novel",
    "Watercolor Storybook"
]