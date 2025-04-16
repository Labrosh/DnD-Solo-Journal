# utils.py – Helper functions for reading, saving, and updating journal data
# Implement:
# - load_journal(filepath): loads a JSON file from logs/ or root
# - save_journal(data, filepath): saves the updated data as JSON
# - update_section(data, section_name, updates): safely update a journal section
# - print_summary(data): optional, outputs a human-readable summary of key info
# All functions should handle exceptions gracefully (e.g., file not found, bad data)

import json
import os
import datetime
from pathlib import Path

def load_journal(filepath):
    """
    Load a journal file from the specified path.
    If the file doesn't exist, raises FileNotFoundError.
    
    Args:
        filepath: Path to the journal file
    
    Returns:
        dict: Journal data as a dictionary
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: File {filepath} contains invalid JSON.")
        raise

def save_journal(data, filepath):
    """
    Save journal data to the specified path.
    Creates parent directories if they don't exist.
    
    Args:
        data: Journal data as a dictionary
        filepath: Path where the journal should be saved
    
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)
        return True
    except Exception as e:
        print(f"Error saving journal: {e}")
        return False

def update_section(data, section_name, updates):
    """
    Safely update a section of the journal.
    
    Args:
        data: Journal data as a dictionary
        section_name: Name of the section to update (e.g., 'inventory')
        updates: New data to update the section with
    
    Returns:
        dict: Updated journal data
    """
    try:
        # Handle nested sections like quests.active
        if '.' in section_name:
            parent, child = section_name.split('.', 1)
            if parent in data and child in data[parent]:
                data[parent][child] = updates
            else:
                print(f"Warning: Section {section_name} not found in journal.")
        else:
            if section_name in data:
                data[section_name] = updates
            else:
                print(f"Warning: Section {section_name} not found in journal.")
        return data
    except Exception as e:
        print(f"Error updating section: {e}")
        return data

def add_journal_entry(data, entry):
    """
    Add a new entry to the journal_log section.
    
    Args:
        data: Journal data as a dictionary
        entry: Dictionary containing entry details
    
    Returns:
        dict: Updated journal data
    """
    if "journal_log" in data:
        if not entry.get("date"):
            entry["date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        data["journal_log"].append(entry)
    return data

def print_summary(data):
    """
    Print a human-readable summary of the journal data.
    
    Args:
        data: Journal data as a dictionary
    """
    try:
        character = data.get("character", {})
        print("\n===== CHARACTER SUMMARY =====")
        print(f"Name: {character.get('name', 'Unknown')}")
        print(f"Level {character.get('level', '?')} {character.get('class', 'Unknown')}")
        print(f"HP: {character.get('hp', '?')}")
        
        print("\n===== ACTIVE QUESTS =====")
        for quest in data.get("quests", {}).get("active", []):
            print(f"- {quest.get('title', 'Unnamed Quest')}")
        
        print("\n===== RECENT JOURNAL ENTRIES =====")
        entries = data.get("journal_log", [])
        for entry in entries[-3:]:  # Show the last 3 entries
            print(f"\n[{entry.get('date', 'Unknown date')}] {entry.get('title', 'Untitled entry')}")
            print(f"{entry.get('content', '')[:100]}...")  # Show first 100 chars
            
    except Exception as e:
        print(f"Error printing summary: {e}")
