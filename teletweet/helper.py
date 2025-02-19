#!/usr/bin/env python3
# coding: utf-8

# TeleTweet - helper.py
# 2023-05-20  22:32

import json
import logging
import os
import random

script_dir = os.path.dirname(__file__)

def ensure_file_exists(filename, default_content):
    """Ensure a file exists with default content if needed."""
    filepath = os.path.join(script_dir, filename)
    try:
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                if isinstance(default_content, dict):
                    json.dump(default_content, f)
                else:
                    f.write(default_content)
        return filepath
    except Exception as e:
        logging.error(f"Error ensuring file exists {filename}: {e}")
        return None

def generate_tags(mode: str = "allrandom") -> str:
    """Generate tags for messages."""
    try:
        tags_file = ensure_file_exists("tags.txt", "")
        if not tags_file:
            return ""

        with open(tags_file, "r", encoding="utf-8") as f:
            strings = f.read().splitlines()
            if not strings:
                return ""

            STRINGS = strings[:5]
            random.shuffle(STRINGS)
            
            if mode == "allrandom":
                STRINGS = STRINGS[:1]
                random.shuffle(strings)
                STRINGS.extend(strings[:2])
            else:
                STRINGS = STRINGS[:3]

            return "\n".join(STRINGS)
    except Exception as e:
        logging.error(f"Error generating tags: {e}")
        return ""
