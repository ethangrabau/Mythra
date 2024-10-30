import os
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate_image(prompt, size="1024x1024"):
    """
    Generate an image based on the provided prompt.

    :param prompt: The text prompt to generate the image from.
    :param size: The desired size of the generated image (default is 1024x1024).
    :return: The path of the generated image file.
    """
    try:
        # Create the image generation request using the correct method
        response = client.images.generate(
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response.data[0].url
        print("Generated Image URL:", image_url)

        # Fetch the image from the URL
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        # Save the image to a file
        image_path = "generated_image.png"
        image.save(image_path)

        return image_path  # Return the path to the saved image
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Test the function with a sample prompt
    test_prompt = "A scenic landscape with mountains and a river during sunset."
    image_path = generate_image(test_prompt)
    if image_path:
        print(f"Image saved at: {image_path}")
