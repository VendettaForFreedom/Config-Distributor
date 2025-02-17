import logging
import random
from typing import List, Optional, Tuple

def get_random_message_pair() -> Optional[List[int]]:
    """Get a random message pair from the repository."""
    try:
        # Open and read the text file
        with open('message_id_pairs.txt', 'r') as file:
            # Parse each line into a pair of message IDs
            message_id_pairs = [
                list(map(int, line.strip().split())) 
                for line in file.readlines()
            ]

        if not message_id_pairs:
            logging.warning("No message pairs found in repository")
            return None

        # Randomly select one pair of message IDs
        selected_pair = random.choice(message_id_pairs)
        logging.info("Selected message pair: %s", selected_pair)
        return selected_pair

    except Exception as e:
        logging.error(f"Error reading message pairs: {e}")
        return None

def add_message_pair(msg_ids: List[int]) -> bool:
    """Add a new message pair to the repository."""
    try:
        with open('message_id_pairs.txt', 'a') as file:
            file.write(f"{' '.join(map(str, msg_ids))}\n")
        return True
    except Exception as e:
        logging.error(f"Error adding message pair: {e}")
        return False

def remove_message_pair(msg_ids: List[int]) -> bool:
    """Remove a message pair from the repository."""
    try:
        # Read all pairs
        with open('message_id_pairs.txt', 'r') as file:
            pairs = file.readlines()

        # Convert the input ids to string format for comparison
        pair_str = f"{' '.join(map(str, msg_ids))}\n"

        # Remove the pair if it exists
        if pair_str in pairs:
            pairs.remove(pair_str)

            # Write back all remaining pairs
            with open('message_id_pairs.txt', 'w') as file:
                file.writelines(pairs)
            return True
        return False

    except Exception as e:
        logging.error(f"Error removing message pair: {e}")
        return False
