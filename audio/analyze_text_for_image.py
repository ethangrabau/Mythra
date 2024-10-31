import os
import re
import logging
from openai import OpenAI

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set up logging for both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dnd_app_log.txt", mode="w"),
        logging.StreamHandler()
    ]
)

def sanitize_text(text):
    """Clean and prepare text for LLM processing."""
    text = text.replace("’", "'")
    text = re.sub(r'[“”]', '"', text)
    return text

def update_recent_memory(transcription, recent_memory):
    """Update recent memory with LLM based on new transcription."""
    prompt = (
        "You are tracking a Dungeons and Dragons game. Update recent memory based on transcription, "
        "while retaining only the latest scene's relevant details. Remove outdated information from previous scenes.\n\n"
        f"Transcription: {transcription}\n"
        f"Current Recent Memory: {recent_memory}\n\n"
        "Update recent memory only if the transcription provides new information."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        updated_recent_memory = response.choices[0].message.content.strip()
        return updated_recent_memory
    except Exception as e:
        logging.error(f"Error updating recent memory: {e}")
        return recent_memory

def update_long_term_memory(transcription, recent_memory, long_term_memory):
    """Update long-term memory by integrating new key details about characters or settings."""
    prompt = (
        "You are managing long-term story memory for a Dungeons and Dragons game. Integrate only persistent details "
        "into long-term memory based on transcription and recent memory.\n\n"
        f"Transcription: {transcription}\n"
        f"Recent Memory: {recent_memory}\n"
        f"Current Long-Term Memory: {long_term_memory}\n\n"
        "Update only if new long-term character or setting details are provided."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        updated_long_term_memory = response.choices[0].message.content.strip()
        return updated_long_term_memory
    except Exception as e:
        logging.error(f"Error updating long-term memory: {e}")
        return long_term_memory

def analyze_text_for_image(text, memory_manager):
    """Analyze text and decide if a new image is needed, ensuring detailed logging."""
    logging.info(f"Analyzing text: {text[:100]}...")
    sanitized_text = sanitize_text(text)

    # Fetch current memory states
    current_recent_memory = memory_manager.get_recent_memory()
    current_long_term_memory = memory_manager.get_long_term_memory()

    # Log current memory states before updates
    logging.info(f"Long-term memory before updates: {current_long_term_memory}")

    # Update recent memory
    updated_recent_memory = update_recent_memory(sanitized_text, current_recent_memory)
    memory_manager.set_recent_memory(updated_recent_memory)
    logging.info(f"Updated recent memory: {updated_recent_memory}")

    # Update long-term memory if new details are present
    updated_long_term_memory = update_long_term_memory(sanitized_text, updated_recent_memory, current_long_term_memory)
    memory_manager.set_long_term_memory(updated_long_term_memory)
    logging.info(f"Updated long-term memory: {updated_long_term_memory}")

    # Determine if an image update is necessary
    if updated_recent_memory == current_recent_memory and updated_long_term_memory == current_long_term_memory:
        logging.info("No significant memory change detected; skipping image generation.")
        return "none"

    try:
        # Generate image prompt incorporating long-term details
        prompt = (
            "You are an AI art companion for a D&D game. Given the transcription, recent memory, and long-term character details, "
            "generate an image prompt that includes all relevant character details from long-term memory.\n\n"
            f"Transcription: {sanitized_text}\n\n"
            f"Recent Memory: {updated_recent_memory}\n\n"
            f"Long-Term Memory: {updated_long_term_memory}\n\n"
            "Respond with 'generate image: [describe the scene]' or 'no image' if no image is needed."
        )

        logging.info(f"Sending prompt to OpenAI: {prompt[:200]}...")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_response = response.choices[0].message.content.strip().lower()
        logging.info(f"Received AI response: {ai_response}")

        if "generate image" in ai_response:
            prompt_text = ai_response.split("generate image:")[-1].strip()
            logging.info(f"AI decided to generate a new image with prompt: {prompt_text}")
            return prompt_text
        elif "no image" in ai_response:
            logging.info("AI decided not to generate a new image.")
            return "none"
        else:
            logging.warning(f"Unexpected response format: {ai_response}")
            return "none"
    except Exception as e:
        logging.error(f"Error analyzing text for image: {e}")
        return "none"
