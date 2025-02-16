import random
import os
from typing import Optional

def load_tags() -> list:
    """Load tags from the tags file."""
    try:
        with open('teletweet/tags.txt', 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

def generate_tags(mode: Optional[str] = None) -> str:
    """Generate tags based on the specified mode."""
    tags = load_tags()
    if not tags:
        return ""
        
    if mode == "first5random":
        # Randomly select 5 tags
        selected_tags = random.sample(tags, min(5, len(tags)))
    else:
        # Use all tags
        selected_tags = tags
        
    return "\n" + "\n".join(selected_tags)

def add_tag(tag: str) -> bool:
    """Add a new tag to the tags file."""
    if not tag.startswith("#"):
        tag = f"#{tag}"
    
    try:
        with open('teletweet/tags.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{tag}")
        return True
    except Exception:
        return False

def remove_tag(tag: str) -> bool:
    """Remove a tag from the tags file."""
    if not tag.startswith("#"):
        tag = f"#{tag}"
        
    try:
        tags = load_tags()
        tags = [t for t in tags if t != tag]
        
        with open('teletweet/tags.txt', 'w', encoding='utf-8') as file:
            file.write("\n".join(tags))
        return True
    except Exception:
        return False
