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
    :return: The generated image object or None in case of failure.
    """
    try:
        # Step 1: Send the image generation request
        request = requests.post(
            'https://api.bfl.ml/v1/flux-pro-1.1',
            headers={
                'accept': 'application/json',
                'x-key': os.environ.get("BFL_API_KEY"),
                'Content-Type': 'application/json',
            },
            json={
                'prompt': prompt,
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

                # Step 4: Display the image
                img.show()
                return img
            else:
                print(f"Status: {result['status']}")
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    # Test the function with a sample prompt
    test_prompt = "A mouse on its back legs running like a human is holding a big silver fish with its arms. The cat is running away from the shop owner and has a panicked look on his face. The scene is situated in a crowded market."

    generate_image_flux(test_prompt)
