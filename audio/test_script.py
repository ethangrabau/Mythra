import logging
import time
from memory_manager import MemoryManager
from analyze_text_for_image import analyze_text_for_image
from difflib import get_close_matches

# Initialize memory manager
memory_manager = MemoryManager()

# Clear memory at the start of each run
memory_manager.clear_memory()  # Make sure this method is defined in MemoryManager

# Clear the log file at the beginning of each run
open("dnd_text_log.txt", "w").close()

# Set up logging with file and stream handlers
file_handler = logging.FileHandler("dnd_text_log.txt", mode="a")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)

# Ensure logs are written to file immediately
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(stream_handler)

# Define characters and pre-load them into long-term memory
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
    memory_manager.update_memory("characters", name, description)
    logging.info(f"Loaded character: {name} into long-term memory.")

# Vocabulary for close matching to improve transcription recognition
dnd_vocabulary = {
    "Bruce": ["bruce", "bruise"],
    "Todd": ["todd", "tad", "toad"],
    "Gladrin": ["gladrin", "gladron", "glad"],
    "Amulet": ["amulet", "ambulance", "amlet"],
    "Wyvern": ["wyvern", "dragon", "wiverin"],
    "Castle": ["castle", "casal", "cassel"],
}

# Helper function to correct terms in transcription based on vocabulary
def correct_spelling(term, vocab):
    matches = get_close_matches(term.lower(), vocab, n=1, cutoff=0.8)
    return matches[0] if matches else term

# Example transcriptions for testing
transcriptions = [
    "Bruce and Todd are trekking through a dense, misty forest. The fog is thick, and visibility is low.",
    "They stumble upon an old, abandoned cabin with a faint glow coming from inside.",
    "Inside the cabin, they find an ancient map spread across a dusty table, showing a hidden path to a nearby castle.",
    "As they study the map, an elderly sage appears from the shadows, warning them of dangers ahead.",
    "The sage hands Todd a magical amulet, which begins to glow faintly in his hand.",
    "Following the map, they cross a rickety wooden bridge over a deep chasm, with Bruce leading the way.",
    "Upon reaching the castle gate, they find it locked. Bruce raises Gladrin, his mighty axe, and shatters the gate with a single blow.",
    "Inside the castle, the walls are lined with ancient tapestries depicting battles between humans and dragons.",
    "A loud roar echoes through the hall as a fierce wyvern emerges, blocking their path.",
    "Todd draws his sword, the amulet glowing brightly now, as he and Bruce prepare for the fight."
]

# Process each transcription
for transcription in transcriptions:
    # Correct spelling in transcription based on vocabulary
    words = transcription.split()
    corrected_transcription = ' '.join(
        correct_spelling(word, [item for sublist in dnd_vocabulary.values() for item in sublist])
        for word in words
    )

    # Log the corrected transcription
    logging.info(f"Processing corrected transcription: {corrected_transcription}")
    
    # Analyze the transcription for image generation
    image_prompt = analyze_text_for_image(corrected_transcription, memory_manager)

    # Log the memory and the final prompt for image generation
    logging.info(f"Current memory for this transcription: {memory_manager.get_memory()}")
    if image_prompt != "none":
        logging.info(f"Image generation prompt sent to Flux: {image_prompt}")
    else:
        logging.info("No image generation needed for this transcription.")
    
    # Flush logs after each transcription analysis
    file_handler.flush()
    time.sleep(2)  # Simulate delay for testing

logging.info("Test script complete.")
file_handler.flush()  # Final flush to ensure complete log output
