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

def get_quest_titles(quests, section):
    """Get list of quest titles from a quest section"""
    return [q.get('title', 'Unnamed Quest') if isinstance(q, dict) else str(q)
            for q in quests.get(section, [])]

def print_summary(data):
    """
    Print a comprehensive human-readable summary of the journal data.
    
    Args:
        data: Journal data as a dictionary
    """
    try:
        character = data.get("character", {})
        print("\n===== CHARACTER SUMMARY =====")
        print(f"Name: {character.get('name', 'Unknown')}")
        print(f"Level {character.get('level', '?')} {character.get('class', 'Unknown')}")
        print(f"HP: {character.get('hp', '?')}/{character.get('max_hp', '?')}")
        print(f"Hit Dice: {character.get('hit_dice', '?')}")
        print(f"Fighting Style: {character.get('fighting_style', 'None')}")
        
        currency = character.get("currency", {})
        print(f"\nCurrency: {currency.get('gp', 0)} GP, {currency.get('sp', 0)} SP, {currency.get('cp', 0)} CP")
        
        if features := character.get("features", []):
            print("\nFeatures:")
            for feature in features:
                print(f"- {feature}")
        
        quests = data.get("quests", {})
        
        print("\n===== QUESTS =====")
        print("Active Quests:")
        for i, quest in enumerate(quests.get("active", []), 1):
            print(f"{i}. {quest.get('title', 'Untitled')} - {quest.get('description', 'No description')[:60]}...")
        
        print("\nCompleted Quests:")
        for i, quest in enumerate(quests.get("completed", []), 1):
            print(f"{i}. {quest.get('title', 'Untitled')} - Completed: {quest.get('completed_date', 'Unknown')}")
            
        print("\nRumors:")
        for i, rumor in enumerate(quests.get("rumors", []), 1):
            print(f"{i}. {rumor.get('title', 'Untitled')} - Source: {rumor.get('source', 'Unknown')}")
        
        print("\n===== INVENTORY =====")
        for item in data.get("inventory", [])[:10]:  # Show first 10 items
            name = item.get("name", "Unnamed item")
            qty = item.get("quantity", 1)
            print(f"- {name} (x{qty})")
        if len(data.get("inventory", [])) > 10:
            print(f"... and {len(data.get('inventory', [])) - 10} more items")
        
        print("\n===== RECENT JOURNAL ENTRIES =====")
        entries = data.get("journal_log", [])
        for entry in entries[-3:]:  # Show the last 3 entries
            if isinstance(entry, dict):
                date = entry.get("date", entry.get("day", "Unknown date"))
                title = entry.get("title", "Untitled entry")
                content = entry.get("content", entry.get("entry", ""))
                print(f"\n[{date}] {title}")
                if content:
                    print(content if len(content) < 200 else f"{content[:200]}...")
            else:
                print(f"\n{str(entry)[:200]}{'...' if len(str(entry)) > 200 else ''}")
            
        if mental_notes := data.get("mental_state", {}).get("notes", []):
            print("\n===== MENTAL STATE NOTES =====")
            for note in mental_notes[-3:]:  # Show last 3 notes
                print(f"- {note}")
                
    except Exception as e:
        print(f"Error printing summary: {e}")
        print("Partial summary:")
        print(json.dumps(data, indent=2)[:1000])

def clean_journal_data(data):
    """
    Clean journal data by removing empty fields and null values.
    Preserves structure needed for AI processing.
    
    Args:
        data: Journal data dictionary
    
    Returns:
        dict: Cleaned journal data
    """
    def clean_dict(d):
        if not isinstance(d, dict):
            return d
        return {k: clean_dict(v) for k, v in d.items()
                if v not in (None, "", [], {}) and not str(v).isspace()}
    
    # Preserve these fields even if empty
    required_fields = {
        "character": {"name", "class", "level"},
        "quests": {"active", "completed", "rumors"},
        "_meta": {"version", "last_ai_sync", "milestones"}
    }
    
    cleaned = clean_dict(data)
    
    # Ensure required structure remains
    for section, fields in required_fields.items():
        if section not in cleaned:
            cleaned[section] = {}
        for field in fields:
            if field not in cleaned[section]:
                if section == "quests":
                    cleaned[section][field] = []
                else:
                    cleaned[section][field] = None
    
    return cleaned

def list_json_files(folder):
    """
    Returns a list of .json filenames in the given folder.
    
    Args:
        folder: Path to the folder to search in
    
    Returns:
        list: List of filenames ending with .json
    """
    try:
        if not os.path.exists(folder):
            print(f"Folder {folder} does not exist.")
            return []
            
        json_files = [f for f in os.listdir(folder) if f.endswith('.json')]
        return json_files
    except Exception as e:
        print(f"Error listing JSON files: {e}")
        return []
