# D&D Solo Journal - AI Adventure Integration Tool

## Overview
This tool maintains continuity for AI-run D&D adventures by:
- Tracking game state in structured JSON format
- Providing backup UI for reviewing/editing AI-generated content
- Managing milestone updates between AI sessions

## Core Workflow
1. **AI Session**: ChatGPT runs the adventure
2. **Milestone Reached**: AI prompts to update the journal
3. **Export**: Save current state from this tool
4. **AI Processing**: ChatGPT reads, updates, and returns journal
5. **Import**: Load updated journal back into this tool
6. **Repeat**: Continue the adventure

## Key Features
- **AI Sync Tracking**: Timestamps and version control
- **Milestone Markers**: Quest completions, level ups, etc.
- **Data Validation**: Clean JSON structure for reliable AI parsing
- **Dual Display**: Summary views + full narrative logs
- **Manual Overrides**: Edit capability for rare corrections

## Installation
```bash
git clone [repo-url]
cd DnD-Solo-Journal
python3 gui.py
```

## Usage
1. Start new journal from template or load existing
2. Play adventure with AI (ChatGPT)
3. At milestones:
   - Export current journal (`Settings > Export Journal`)
   - Provide JSON to AI for updates
   - Import AI-updated journal (`Settings > Import Journal`)
4. Review changes and continue adventure

## Data Structure
Journals contain:
- Character stats and inventory
- Active/completed quests
- NPC relationships 
- Mental state notes
- Metadata for AI sync tracking

Example structure:
```json
{
  "_meta": {
    "version": 2,
    "last_ai_sync": "2025-04-16T19:30:00",
    "milestones": [
      {
        "type": "quest_completed",
        "quest": "The Ghoul in the Mine",
        "timestamp": "2025-04-16T19:25:00"
      }
    ]
  },
  "character": {
    "name": "Lawrence Holding",
    "class": "Fighter",
    "level": 2
  },
  "quests": {
    "active": [],
    "completed": [...],
    "rumors": [...]
  }
}
```

## Best Practices
- Always export/import via the GUI (don't edit JSON directly)
- Verify AI changes after import
- Use milestones to maintain narrative continuity
- Keep manual edits minimal
