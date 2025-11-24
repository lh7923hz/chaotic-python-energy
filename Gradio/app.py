import os
import openai
import gradio as gr
from io import BytesIO
from PIL import Image
import requests

# Import API key from config file
# Priority: config.py > environment variable
try:
    from config import OPENAI_API_KEY
except ImportError:
    # Fallback to environment variable if config.py doesn't exist
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Validate API key exists
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key not found! Please set it in config.py or OPENAI_API_KEY environment variable.\n"
        "Copy config.example.py to config.py and add your API key."
    )

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt):
    """
    Generates an image using OpenAI's DALL-E image generation API from the user's prompt.
    Returns a PIL Image object for Gradio to display.
    """
    if not prompt or not prompt.strip():
        return None
    
    try:
        # Call OpenAI Image API using DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",  # DALL-E 3 supports: "1024x1024", "1792x1024", "1024x1792"
            quality="standard",  # "standard" or "hd"
            n=1
        )

        # Get image URL from response
        image_url = response.data[0].url
        
        # Download the image
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        # Convert to PIL Image
        image = Image.open(BytesIO(img_response.content))
        
        return image
        
    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"
    except requests.RequestException as e:
        return f"Error downloading image: {str(e)}"
    except Exception as e:
        return f"Error generating image: {str(e)}"

# Gradio UI
iface = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(
        label="Enter a prompt for the image",
        placeholder="e.g., A futuristic city with flying cars at sunset",
        lines=3
    ),
    outputs=gr.Image(label="Generated Image", type="pil"),
    title="OpenAI DALL-E Image Generator",
    description="Type a detailed prompt and generate an image using OpenAI's DALL-E 3 API. Be creative and descriptive!"
)

# Launch the app
if __name__ == "__main__":
    iface.launch()
