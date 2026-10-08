import io
from PIL import Image
from google import genai
import config

def generate_panel_image(visual_description: str, art_style: str) -> Image.Image:
    """Generates an image for a comic panel given a visual prompt and art style."""
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    prompt = f"Comic book panel artwork in {art_style} style. {visual_description}, high quality, crisp line art, detailed illustration."

    result = client.models.generate_images(
        model=config.IMAGE_MODEL,
        prompt=prompt,
        config=dict(
            number_of_images=1,
            aspect_ratio="1:1",
            output_mime_type="image/jpeg"
        )
    )

    image_bytes = result.generated_images[0].image.image_bytes
    return Image.open(io.BytesIO(image_bytes))