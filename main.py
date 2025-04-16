#!/usr/bin/env python3
# main.py – Entry point for the Solo D&D Journal app
# Your job is to:
# 1. Load an existing journal file from the /logs folder or create one from journal_template.json.
# 2. Offer CLI prompts or arguments for:
#    - Adding a new journal entry
#    - Updating inventory, quests, NPCs, or mental state
#    - Leveling up or changing stats
#    - Exporting a summary (optional)
# 3. Save the updated journal file back to /logs with the same filename.
# Use functions from utils.py for all read/write operations.
# Avoid hardcoding filenames — use input() or argparse to select files.

import os
import sys
import json  # Added missing import for json module
import argparse
from pathlib import Path
from utils import load_journal, save_journal, update_section, add_journal_entry, print_summary

def get_logs_dir():
    """Get the absolute path to the logs directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "logs")
    
def get_template_path():
    """Get the absolute path to the journal template."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "journal_template.json")

def list_journals():
    """List all available journal files in the logs directory."""
    logs_dir = get_logs_dir()
    try:
        if not os.path.exists(logs_dir):
            print("Logs directory doesn't exist yet. No journals available.")
            return []
            
        journals = [f for f in os.listdir(logs_dir) if f.endswith('.json')]
        
        if not journals:
            print("No journal files found in logs directory.")
            return []
            
        print("Available journals:")
        for i, journal in enumerate(journals, 1):
            print(f"{i}. {journal}")
        return journals
    except Exception as e:
        print(f"Error listing journals: {e}")
        return []

def create_new_journal():
    """Create a new journal from the template."""
    template_path = get_template_path()
    logs_dir = get_logs_dir()
    
    try:
        journal_data = load_journal(template_path)
        
        # Get basic character info
        journal_data["character"]["name"] = input("Character name: ")
        journal_data["character"]["class"] = input("Character class: ")
        journal_data["character"]["hp"] = int(input("Starting HP: "))
        journal_data["character"]["hit_dice"] = input("Hit dice (e.g., 1d10): ")
        
        # Create a filename based on character name
        safe_name = journal_data["character"]["name"].lower().replace(" ", "_")
        filename = f"{safe_name}.json"
        filepath = os.path.join(logs_dir, filename)
        
        # Save the new journal
        os.makedirs(logs_dir, exist_ok=True)
        if save_journal(journal_data, filepath):
            print(f"Created new journal at {filepath}")
            return filepath
        else:
            print("Failed to create journal.")
            return None
    except Exception as e:
        print(f"Error creating journal: {e}")
        return None

def add_new_entry(journal_data):
    """Add a new entry to the journal log."""
    print("\n=== Adding New Journal Entry ===")
    date = input("Date (YYYY-MM-DD) [leave blank for today]: ")
    title = input("Entry title: ")
    print("Entry content (type END on a new line when finished):")
    
    # Collect multiline input
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    
    content = "\n".join(lines)
    
    entry = {
        "date": date,
        "title": title,
        "content": content
    }
    
    return add_journal_entry(journal_data, entry)

def update_inventory(journal_data):
    """Update the character's inventory."""
    print("\n=== Updating Inventory ===")
    print("Current inventory items:")
    for i, item in enumerate(journal_data.get("inventory", []), 1):
        print(f"{i}. {item.get('name', 'Unknown item')}")
    
    action = input("Do you want to [a]dd an item, [r]emove an item, or [c]ancel? ").lower()
    
    if action == 'a':
        name = input("Item name: ")
        quantity = input("Quantity (default 1): ")
        description = input("Description: ")
        
        item = {
            "name": name,
            "quantity": int(quantity) if quantity.isdigit() else 1,
            "description": description
        }
        
        journal_data["inventory"] = journal_data.get("inventory", []) + [item]
        print(f"Added {name} to inventory.")
    
    elif action == 'r':
        try:
            idx = int(input("Enter the number of the item to remove: ")) - 1
            if 0 <= idx < len(journal_data.get("inventory", [])):
                removed = journal_data["inventory"].pop(idx)
                print(f"Removed {removed.get('name', 'item')} from inventory.")
            else:
                print("Invalid item number.")
        except ValueError:
            print("Please enter a valid number.")
    
    return journal_data

def update_quest_log(journal_data):
    """Update the character's quest log."""
    print("\n=== Updating Quest Log ===")
    quests = journal_data.get("quests", {"completed": [], "active": [], "rumors": []})
    
    print("1. View active quests")
    print("2. Add new quest")
    print("3. Complete a quest")
    print("4. Add rumor")
    print("5. Cancel")
    
    choice = input("Choose an option (1-5): ")
    
    if choice == '1':
        print("\nActive quests:")
        for i, quest in enumerate(quests.get("active", []), 1):
            print(f"{i}. {quest.get('title', 'Unnamed quest')}")
    
    elif choice == '2':
        title = input("Quest title: ")
        description = input("Quest description: ")
        giver = input("Quest giver: ")
        
        new_quest = {
            "title": title,
            "description": description,
            "giver": giver,
            "started": input("Start date (YYYY-MM-DD): ")
        }
        
        quests["active"] = quests.get("active", []) + [new_quest]
        journal_data["quests"] = quests
        print(f"Added '{title}' to active quests.")
    
    elif choice == '3':
        try:
            print("\nActive quests:")
            for i, quest in enumerate(quests.get("active", []), 1):
                print(f"{i}. {quest.get('title', 'Unnamed quest')}")
            
            idx = int(input("Enter the number of the quest to complete: ")) - 1
            if 0 <= idx < len(quests.get("active", [])):
                completed_quest = quests["active"].pop(idx)
                completed_quest["completed_date"] = input("Completion date (YYYY-MM-DD): ")
                quests["completed"] = quests.get("completed", []) + [completed_quest]
                journal_data["quests"] = quests
                print(f"Moved '{completed_quest.get('title', 'quest')}' to completed quests.")
            else:
                print("Invalid quest number.")
        except ValueError:
            print("Please enter a valid number.")
    
    elif choice == '4':
        title = input("Rumor title: ")
        description = input("Rumor description: ")
        source = input("Rumor source: ")
        
        new_rumor = {
            "title": title,
            "description": description,
            "source": source,
            "heard_date": input("Date heard (YYYY-MM-DD): ")
        }
        
        quests["rumors"] = quests.get("rumors", []) + [new_rumor]
        journal_data["quests"] = quests
        print(f"Added '{title}' to rumors.")
    
    return journal_data

def update_character(journal_data):
    """Update character stats."""
    print("\n=== Updating Character Stats ===")
    character = journal_data.get("character", {})
    
    print(f"Current stats for {character.get('name', 'Unknown')}:")
    print(f"Level: {character.get('level', 1)}")
    print(f"Class: {character.get('class', 'Unknown')}")
    print(f"HP: {character.get('hp', 0)}")
    
    field = input("What would you like to update? (level, hp, features, or name): ").lower()
    
    if field == 'level':
        try:
            new_level = int(input(f"New level (current: {character.get('level', 1)}): "))
            character["level"] = new_level
            print(f"Updated level to {new_level}.")
        except ValueError:
            print("Please enter a valid number.")
    
    elif field == 'hp':
        try:
            new_hp = int(input(f"New HP (current: {character.get('hp', 0)}): "))
            character["hp"] = new_hp
            print(f"Updated HP to {new_hp}.")
        except ValueError:
            print("Please enter a valid number.")
    
    elif field == 'features':
        print("Current features:")
        for i, feature in enumerate(character.get("features", []), 1):
            print(f"{i}. {feature}")
        
        action = input("Do you want to [a]dd a feature or [r]emove one? ").lower()
        
        if action == 'a':
            new_feature = input("New feature: ")
            character["features"] = character.get("features", []) + [new_feature]
            print(f"Added '{new_feature}' to features.")
        elif action == 'r':
            try:
                idx = int(input("Enter the number of the feature to remove: ")) - 1
                if 0 <= idx < len(character.get("features", [])):
                    removed = character["features"].pop(idx)
                    print(f"Removed '{removed}' from features.")
                else:
                    print("Invalid feature number.")
            except ValueError:
                print("Please enter a valid number.")
    
    elif field == 'name':
        new_name = input(f"New name (current: {character.get('name', 'Unknown')}): ")
        character["name"] = new_name
        print(f"Updated name to {new_name}.")
    
    else:
        print(f"Field '{field}' not recognized or cannot be updated.")
    
    journal_data["character"] = character
    return journal_data

def main():
    """Main function to run the Solo D&D Journal application."""
    print("===== D&D Solo Journal =====")
    
    # Check if logs directory exists, create if needed
    logs_dir = get_logs_dir()
    os.makedirs(logs_dir, exist_ok=True)
    
    # List existing journals or create a new one
    journals = list_journals()
    
    if journals:
        choice = input("\nEnter journal number to load, or 'n' to create a new one: ")
        if choice.lower() == 'n':
            journal_path = create_new_journal()
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(journals):
                    journal_path = os.path.join(logs_dir, journals[idx])
                else:
                    print("Invalid journal number.")
                    return
            except ValueError:
                print("Invalid choice. Please enter a number or 'n'.")
                return
    else:
        print("No existing journals found.")
        create_choice = input("Would you like to create a new journal? (y/n): ")
        if create_choice.lower() == 'y':
            journal_path = create_new_journal()
        else:
            print("Exiting.")
            return
    
    if not journal_path:
        return
    
    # Load the selected journal
    try:
        journal_data = load_journal(journal_path)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error loading journal from {journal_path}")
        return
    
    # Show journal summary
    print_summary(journal_data)
    
    # Main interaction loop
    while True:
        print("\n===== JOURNAL OPTIONS =====")
        print("1. Add journal entry")
        print("2. Update inventory")
        print("3. Update quest log")
        print("4. Update character stats")
        print("5. View summary")
        print("6. Save and exit")
        
        choice = input("\nChoose an option (1-6): ")
        
        if choice == '1':
            journal_data = add_new_entry(journal_data)
        elif choice == '2':
            journal_data = update_inventory(journal_data)
        elif choice == '3':
            journal_data = update_quest_log(journal_data)
        elif choice == '4':
            journal_data = update_character(journal_data)
        elif choice == '5':
            print_summary(journal_data)
        elif choice == '6':
            if save_journal(journal_data, journal_path):
                print(f"Journal saved to {journal_path}")
            else:
                print("Error saving journal")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
