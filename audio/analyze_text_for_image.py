import os
import re
import logging
from openai import OpenAI
from difflib import get_close_matches
import json  # Ensure json is imported

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Define `build_vocab_from_memory` here
def build_vocab_from_memory(memory):
    """Builds a vocabulary from characters, items, and locations in memory."""
    vocab = {}
    for entity_type in ["characters", "items", "locations"]:
        if entity_type in memory:
            for name in memory[entity_type]:
                vocab[name] = [name.lower()]
    return vocab

# Function to sanitize text
def sanitize_text(text):
    text = text.replace("’", "'")
    text = re.sub(r'[“”]', '"', text)
    return text

# Unified memory function for managing characters, items, and locations
def update_memory(transcription, memory_manager):
    prompt = (
        "You are managing a dynamic memory table for a Dungeons and Dragons game (DND). "
        "The memory table includes characters, items, locations, and recent activity. "
        "You will be given a transcription of the current scene and the memory table. "
        "Update the memory table with any new details from the transcription strictly as presented. "
        "Do not assume or infer information beyond the transcription, and only update details relevant to named characters, items, or locations. "
        "Update the recent activity with a short summary of the latest events. "
        "Use the examples below to guide your updates and formatting:\n\n"
        
        "### Examples ###\n\n"
        
        # Example 1: Detailed character description with physical traits
        "Example 1:\n"
        "Transcription: A tall, muscular man named Gus, with dark hair tied back and a jagged scar across his cheek, "
        "stands on the deck of a pirate ship holding a silver sword. The waves crash around the ship.\n"
        "Memory table before update:\n"
        "Characters: {}\nItems: {}\nLocations: {}\nRecent activity: []\n\n"
        "Expected memory update:\n"
        "Characters: {'Gus': 'Tall, muscular man with dark hair tied back and a jagged scar across his cheek. Currently standing on a pirate ship deck holding a silver sword.'}\n"
        "Locations: {'Pirate Ship': 'A large ship with sails flapping in the wind, waves crashing around it.'}\n"
        "Recent activity: ['Gus stands on the pirate ship deck holding a silver sword as waves crash around.']\n\n"

        # Example 2: Item description and interaction with character
        "Example 2:\n"
        "Transcription: Gus picks up an amulet that glows with a faint blue light, adorned with an intricate design of a snake.\n"
        "Memory table before update:\n"
        "Characters: {'Gus': 'Tall, muscular man with dark hair tied back and a jagged scar.'}\n"
        "Items: {}\nLocations: {}\nRecent activity: []\n\n"
        "Expected memory update:\n"
        "Items: {'Amulet': 'A faintly glowing amulet with a blue light, adorned with a snake design.'}\n"
        "Characters: {'Gus': 'Tall, muscular man with dark hair tied back and a jagged scar, holding a glowing amulet.'}\n"
        "Recent activity: ['Gus picks up a glowing amulet with a snake design.']\n\n"
        
        # Example 3: Location description with environmental details
        "Example 3:\n"
        "Transcription: The party enters a dark cave with walls covered in glowing moss. The air feels damp and cool.\n"
        "Memory table before update:\n"
        "Locations: {}\nRecent activity: []\n\n"
        "Expected memory update:\n"
        "Locations: {'Cave': 'A dark cave with walls covered in glowing moss. The air is damp and cool.'}\n"
        "Recent activity: ['The party enters a dark cave with glowing moss on the walls.']\n\n"

        # Example 4: Character description with physical and mystical attributes
        "Example 4:\n"
        "Transcription: Standing at six feet, Elena has piercing green eyes, wavy auburn hair, and a golden cloak. "
        "She clutches a worn spellbook covered in ancient symbols.\n"
        "Memory table before update:\n"
        "Characters: {}\nItems: {}\nRecent activity: []\n\n"
        "Expected memory update:\n"
        "Characters: {'Elena': 'Six feet tall with piercing green eyes and wavy auburn hair. Wearing a golden cloak and holding a worn spellbook with ancient symbols.'}\n"
        "Items: {'Spellbook': 'A worn spellbook covered in ancient symbols, held by Elena.'}\n"
        "Recent activity: ['Elena stands holding her worn spellbook covered in ancient symbols.']\n\n"
        
        # Example 5: Recent activity update with action and summary
        "Example 5:\n"
        "Transcription: Elena chants an incantation as she raises her spellbook, casting a light spell that illuminates the cave.\n"
        "Memory table before update:\n"
        "Characters: {'Elena': 'Six feet tall with piercing green eyes, wavy auburn hair, wearing a golden cloak, holding a spellbook.'}\n"
        "Locations: {'Cave': 'A dark cave with glowing moss and damp, cool air.'}\n"
        "Recent activity: []\n\n"
        "Expected memory update:\n"
        "Recent activity: ['Elena casts a light spell, illuminating the dark cave.']\n\n"
        
        "### End of Examples ###\n\n"
        
        "Here is the transcription: " + transcription + "\n\n"
        "Here is the current memory table: " + str(memory_manager.get_memory()) + "\n\n"
        "Based on this transcription, update the memory table accordingly."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        
         # Retrieve and log the raw AI response
        ai_response = response.choices[0].message.content.strip()
        logging.info(f"Raw AI response for memory update: {ai_response}")

        # Manual parsing of the response, assuming the format remains consistent
        updated_memory = {'characters': {}, 'items': {}, 'locations': {}, 'recent_activity_summary': []}

        # Parse characters
        characters_match = re.search(r"Characters:\s*({.*?})", ai_response, re.DOTALL)
        if characters_match:
            characters_str = characters_match.group(1)
            updated_memory['characters'] = eval(characters_str)  # Convert string to dictionary

        # Parse items
        items_match = re.search(r"Items:\s*({.*?})", ai_response, re.DOTALL)
        if items_match:
            items_str = items_match.group(1)
            updated_memory['items'] = eval(items_str)

        # Parse locations
        locations_match = re.search(r"Locations:\s*({.*?})", ai_response, re.DOTALL)
        if locations_match:
            locations_str = locations_match.group(1)
            updated_memory['locations'] = eval(locations_str)

        # Parse recent activity
        recent_activity_match = re.search(r"Recent activity:\s*\[(.*?)\]", ai_response, re.DOTALL)
        if recent_activity_match:
            recent_activity_str = recent_activity_match.group(1)
            updated_memory['recent_activity_summary'] = [entry.strip() for entry in recent_activity_str.split(',')]

        # Return the parsed memory table
        return updated_memory

    except Exception as e:
        logging.error(f"Error in update_memory: {e}")
        return memory_manager.get_memory()  # Return original memory in case of an error

def correct_spelling(term, vocab):
    matches = get_close_matches(term.lower(), [key for key in vocab.keys()], n=1, cutoff=0.8)
    return matches[0] if matches else term

# Spell-check function using dynamic vocabulary
def context_aware_spell_check(transcription, vocab):
    words = transcription.split()
    corrected_words = []
    
    for word in words:
        if word in vocab:
            corrected_words.append(word)
        else:
            close_matches = get_close_matches(word, vocab.keys(), n=1, cutoff=0.8)
            if close_matches:
                best_match = close_matches[0]
                corrected_words.append(best_match)
                logging.info(f"Corrected '{word}' to '{best_match}'")
            else:
                corrected_words.append(word)
    
    return " ".join(corrected_words)

def analyze_text_for_image(text, memory_manager):
    # Step 1: Sanitize and correct spelling in the transcription
    sanitized_text = sanitize_text(text)
    logging.info(f"Analyzing text: {sanitized_text[:100]}...")

    # Build the vocabulary from the memory for spelling correction
    dnd_vocab = build_vocab_from_memory(memory_manager.get_memory())

    # Correct transcription
    corrected_words = [correct_spelling(word, dnd_vocab) for word in sanitized_text.split()]
    corrected_text = ' '.join(corrected_words)
    corrected_transcription = context_aware_spell_check(corrected_text, dnd_vocab)
    logging.info(f"Final Corrected Transcription: {corrected_transcription}")

    # Get current memory
    current_memory_table = memory_manager.get_memory()
    logging.info(f"Current memory before update: {current_memory_table}")

    try:
        # Update memory
        updated_memory_table = update_memory(corrected_transcription, memory_manager)
        if not isinstance(updated_memory_table, dict):
            logging.error("Expected updated_memory_table to be a dictionary.")
            return "none"
        
        # Log comparison to check for differences
        if updated_memory_table == current_memory_table:
            logging.info("No changes detected, skipping image generation.")
            return "none"
        else:
            logging.info("Memory updated, preparing to generate image.")

        # Image generation prompt
        image_prompt = (
            "You are an AI art companion for a Dungeons and Dragons game. "
            "Please generate a detailed scene based on recent transcription and memory details:\n\n"
            f"Recent Transcription: {corrected_transcription}\n\n"
            f"Characters:\n{str(updated_memory_table.get('characters', {}))}\n\n"
            f"Items:\n{str(updated_memory_table.get('items', {}))}\n\n"
            f"Locations:\n{str(updated_memory_table.get('locations', {}))}\n"
        )
        
        # Log the prompt being sent
        logging.info(f"Sending prompt to OpenAI: {image_prompt[:200]}...")

        # Request from OpenAI, expecting a plain-text response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": image_prompt}],
        )

        # Treat response as plain text
        ai_response = response.choices[0].message.content.strip()
        logging.info(f"Raw AI response: {ai_response}")

        # Check for response content
        if "generate image" in ai_response.lower():
            prompt_start = ai_response.lower().find("generate image:") + len("generate image:")
            initial_prompt = ai_response[prompt_start:].strip()
            logging.info(f"Initial AI-generated prompt: {initial_prompt}")

            # Enhance prompt with character descriptions
            for name, description in updated_memory_table.get("characters", {}).items():
                initial_prompt = initial_prompt.replace(name, f"{name} ({description})")
            for name, description in updated_memory_table.get("items", {}).items():
                initial_prompt = initial_prompt.replace(name, f"{name} ({description})")
            for name, description in updated_memory_table.get("locations", {}).items():
                initial_prompt = initial_prompt.replace(name, f"{name} ({description})")

            logging.info(f"Final enhanced prompt for image generation: {initial_prompt}")
            return initial_prompt

        elif "no image" in ai_response.lower():
            logging.info("AI decided not to generate a new image.")
            return "none"
        else:
            logging.warning(f"Unexpected response format: {ai_response}")
            return "none"

    except Exception as e:
        logging.error(f"Error occurred while analyzing text: {e}")
        return "none"
