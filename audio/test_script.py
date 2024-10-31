import logging
import time
from memory_manager import MemoryManager  # Correct import for memory management
from analyze_text_for_image import analyze_text_for_image  # Importing the function

# Set up detailed logging, clear the log at the start of a new run
with open("dnd_app_log.txt", "w") as log_file:
    log_file.write("")

logging.basicConfig(
    filename="dnd_app_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize memory manager
memory_manager = MemoryManager()

# Load character descriptions into long-term memory
characters = {
    "Bruce": (
        "Bruce is a towering Goliath barbarian with a formidable muscular build and pale gray skin "
        "that looks like weathered stone. His bald head is adorned with intricate dark tribal tattoos, "
        "creating stark contrast against his rugged complexion. Bruce wears a combination of furs and leathers, "
        "decorated with bone and metal details that speak to his prowess as a warrior. His most prized possession "
        "is Gladrin, a massive, double-headed axe etched with ancient runes. Bruce's presence is imposing, and in battle, "
        "he becomes a force of nature, driven by rage and the need to protect his tribe."
    ),
    "Todd": (
        "Todd is a male aasimar paladin, standing tall with a radiant halo behind his head. His long, silver-white hair cascades "
        "over his gleaming golden and silver armor, adorned with intricate celestial designs. He carries an air of divine authority, "
        "with piercing eyes that convey both compassion and unwavering resolve. His armor is marked by sharp angular plates, "
        "with a majestic chest piece emblazoned with holy symbols. His shoulders are protected by golden pauldrons shaped like angelic wings, "
        "and he wields a mighty sword at his side. Todd radiates a soft glow, symbolizing his celestial heritage, and stands as a guardian "
        "of the light, ready to defend against the forces of darkness."
    )
}

# Pre-load character descriptions into long-term memory
for name, description in characters.items():
    memory_manager.set_long_term_memory(f"Character: {name}. {description}")
    logging.info(f"Loaded character: {name} into long-term memory.")

# Example transcriptions for testing
transcriptions = [
    "Bruce is hiking up a mountain and sees a large temple at the top. The sun is starting to set.",
    "Inside the temple, Bruce meets Todd who is praying to the gods.",
    "Bruce draws his mighty axe, Gladrin, as he prepares to defend Todd from an ambush."
]

# Simulate processing each transcription
for transcription in transcriptions:
    logging.info(f"\nProcessing transcription: {transcription}")

    # Simulate processing transcription and updating memories
    analyze_text_for_image(transcription, memory_manager)

    # Wait 2 seconds between each processing step to simulate delay
    time.sleep(2)

logging.info("Test script complete.")
