
# DnD Solo Journal

A lightweight journaling system for solo Dungeons & Dragons players, designed to track character stats, inventory, quests, and narrative progression. Built specifically to support text-based roleplay campaigns and AI-assisted storytelling.

## 🎯 Purpose

This project was created to support a long-term solo D&D campaign. It focuses on clear, persistent tracking of:

- Character stats and progression
- Inventory and quest items
- Quest logs and ongoing leads
- Known NPCs
- Mental/emotional development of the character
- Journal entries per in-game day

## 📦 Features

- JSON-based save files for persistence and AI-friendly data loading
- Modular structure for easy editing and future expansions
- Clear separation of character data, quest state, and RP flavor
- Future-proof design for importing/exporting logs between sessions

## 📁 Project Structure

```
dnd_solo_journal/
├── main.py                # Entry point for running the journal tool
├── journal_template.json  # Default structure for new characters
├── utils.py               # Helper functions (e.g., read/write/save JSON)
├── logs/                  # Stores your saved game states
└── README.md              # This file
```

## 🔧 Planned Features

- Command-line tool for creating and updating journal files
- Optional CLI prompts for character creation and quest logging
- Auto-updating quest and inventory logs after AI-assisted sessions
- Markdown or plaintext exports for reading summaries

## 💾 JSON Format Overview

Each journal file contains the following sections:

- `character` – core stats and features
- `inventory` – all current gear, rations, gold, and key items
- `quests` – completed, active, and rumored
- `npcs` – known characters
- `mental_state` – emotional summaries or ongoing thoughts
- `journal_log` – daily narrative entries

## 📚 How to Use

1. Start with `journal_template.json` and rename it for your character.
2. Run `main.py` to update logs or begin a new entry.
3. Upload the log to your AI assistant for a character check-in.
4. Receive updates, save the new file, and repeat.

## 🧙 Solo Campaign Tested

Originally created for the adventures of Lawrence Holding, an aging soldier-turned-adventurer wandering through a grounded, gritty D&D world. Supports all storytelling styles, from survivalist campaigns to epic magical quests.

---

Feel free to fork, adapt, and expand for your own campaigns!

