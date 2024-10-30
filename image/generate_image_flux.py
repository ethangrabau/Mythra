import os
import requests
import time
from PIL import Image
from io import BytesIO

def generate_image_flux(prompt, width=1024, height=768):
    """
    Generate an image using the Flux 1.1 Pro API.

    :param prompt: The text prompt to generate the image from.
    :param width: The width of the image (default is 1024).
    :param height: The height of the image (default is 768).
    :return: The path of the saved image file or None in case of failure.
    """
    try:
        # Prepend the prefix to the transcribed text
        prompt_prefix = "High-fantasy, photorealistic illustration for a DND campaign. The scene should evoke epic adventure, rich in detail, dramatic lighting, and set in a magical world. The story is about the following: "
        full_prompt = prompt_prefix + prompt

        # Step 1: Send the image generation request
        request = requests.post(
            'https://api.bfl.ml/v1/flux-pro-1.1',
            headers={
                'accept': 'application/json',
                'x-key': os.environ.get("BFL_API_KEY"),
                'Content-Type': 'application/json',
            },
            json={
                'prompt': full_prompt,
                'width': width,
                'height': height,
            },
        ).json()

        request_id = request["id"]

        # Step 2: Poll for the result
        while True:
            time.sleep(0.5)
            result = requests.get(
                'https://api.bfl.ml/v1/get_result',
                headers={
                    'accept': 'application/json',
                    'x-key': os.environ.get("BFL_API_KEY"),
                },
                params={
                    'id': request_id,
                },
            ).json()

            # Check if the result is ready
            if result["status"] == "Ready":
                image_url = result['result']['sample']
                print(f"Image URL: {image_url}")

                # Step 3: Fetch the image from the URL
                image_response = requests.get(image_url)
                img = Image.open(BytesIO(image_response.content))

                # Step 4: Save the image to a file
                image_path = "generated_image_flux.png"  # You can adjust the name as needed
                img.save(image_path)

                return image_path  # Return the path to the saved image

            else:
                print(f"Status: {result['status']}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Test the function with a sample prompt
    test_prompt = "Todd (Description: a male aasimar paladin, standing tall with a radiant halo behind his head. His long, silver-white hair cascades over his gleaming golden and silver armor, adorned with intricate celestial designs. His armor is marked by sharp angular plates, with a majestic chest piece emblazoned with holy symbols. His shoulders are protected by golden pauldrons shaped like angelic wings, and he wields a mighty sword at his side) walks up a mountain with Bruce (Description: a towering Goliath barbarian with a formidable muscular build and pale gray skin that looks like weathered stone. His bald head is adorned with intricate dark tribal tattoos, creating stark contrast against his rugged complexion. Bruce wears a combination of furs and leathers, decorated with bone and metal details that speak to his prowess as a warrior. His carries Gladrin (Description: a massive, double-headed axe etched with ancient runes))"

    image_path = generate_image_flux(test_prompt)
    if image_path:
        print(f"Image saved at: {image_path}")
