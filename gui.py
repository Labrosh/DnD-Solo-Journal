import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from utils import load_journal, save_journal, add_journal_entry, update_section, print_summary, list_json_files
import os
import json
from pathlib import Path

class DnDJournalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Solo Journal")
        self.root.geometry("800x600")
        
        # Journal data and path
        self.journal_data = None
        self.current_journal_path = None
        
        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_welcome_tab()
        self.create_journal_tab()
        self.create_inventory_tab()
        self.create_quests_tab()
        self.create_character_tab()
        self.create_import_tab()
        
        # Start with welcome tab
        self.notebook.select(0)
        
    def create_welcome_tab(self):
        """Create the welcome/selection tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Welcome")
        
        # Journal selection frame
        selection_frame = ttk.LabelFrame(tab, text="Select Journal", padding=10)
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # List existing journals
        self.journal_listbox = tk.Listbox(selection_frame)
        self.journal_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(selection_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Load Selected", command=self.load_selected_journal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create New", command=self.create_new_journal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh List", command=self.refresh_journal_list).pack(side=tk.LEFT, padx=5)
        
        # Initial refresh
        self.refresh_journal_list()
        
    def create_journal_tab(self):
        """Create the journal entries tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Journal")
        
        # Entry form
        form_frame = ttk.LabelFrame(tab, text="New Entry", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Date
        ttk.Label(form_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_date = ttk.Entry(form_frame)
        self.entry_date.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Title
        ttk.Label(form_frame, text="Title:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_title = ttk.Entry(form_frame)
        self.entry_title.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Content
        ttk.Label(form_frame, text="Content:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.entry_content = scrolledtext.ScrolledText(form_frame, width=40, height=10)
        self.entry_content.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)
        
        # Submit button
        ttk.Button(form_frame, text="Add Entry", command=self.add_journal_entry).grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
        
        # Recent entries display
        entries_frame = ttk.LabelFrame(tab, text="Recent Entries", padding=10)
        entries_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.recent_entries = scrolledtext.ScrolledText(entries_frame, state=tk.DISABLED)
        self.recent_entries.pack(fill=tk.BOTH, expand=True)
        
    def create_inventory_tab(self):
        """Create the inventory management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Inventory")
        
        # Inventory list
        list_frame = ttk.LabelFrame(tab, text="Inventory Items", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.inventory_listbox = tk.Listbox(list_frame)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_inventory_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Item", command=self.remove_inventory_item).pack(side=tk.LEFT, padx=5)
        
    def create_quests_tab(self):
        """Create the quests management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Quests")
        
        # Notebook for quest types
        quest_notebook = ttk.Notebook(tab)
        quest_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Active quests
        active_frame = ttk.Frame(quest_notebook)
        quest_notebook.add(active_frame, text="Active")
        
        self.active_quests = tk.Listbox(active_frame)
        self.active_quests.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Completed quests
        completed_frame = ttk.Frame(quest_notebook)
        quest_notebook.add(completed_frame, text="Completed")
        
        self.completed_quests = tk.Listbox(completed_frame)
        self.completed_quests.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Rumors
        rumors_frame = ttk.Frame(quest_notebook)
        quest_notebook.add(rumors_frame, text="Rumors")
        
        self.rumors = tk.Listbox(rumors_frame)
        self.rumors.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add Quest", command=self.add_quest).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Complete Quest", command=self.complete_quest).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Rumor", command=self.add_rumor).pack(side=tk.LEFT, padx=5)
        
    def create_character_tab(self):
        """Create the character stats tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Character")
        
        # Character info
        info_frame = ttk.LabelFrame(tab, text="Character Info", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Name
        ttk.Label(info_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.char_name = ttk.Entry(info_frame)
        self.char_name.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Class
        ttk.Label(info_frame, text="Class:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.char_class = ttk.Entry(info_frame)
        self.char_class.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # Level
        ttk.Label(info_frame, text="Level:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.char_level = ttk.Spinbox(info_frame, from_=1, to=20)
        self.char_level.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # HP
        ttk.Label(info_frame, text="HP:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.char_hp = ttk.Spinbox(info_frame, from_=1, to=999)
        self.char_hp.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Hit Dice
        ttk.Label(info_frame, text="Hit Dice:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.char_hit_dice = ttk.Entry(info_frame)
        self.char_hit_dice.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Save button
        ttk.Button(info_frame, text="Save Changes", command=self.save_character).grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)
        
    def create_import_tab(self):
        """Create the import/export tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Import/Export")
        
        # Import frame
        import_frame = ttk.LabelFrame(tab, text="Import Journal", padding=10)
        import_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(import_frame, text="Import Journal", command=self.import_journal).pack(pady=5)
        
        # Export frame
        export_frame = ttk.LabelFrame(tab, text="Export Journal", padding=10)
        export_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(export_frame, text="Export Current Journal", command=self.export_journal).pack(pady=5)
        
    # TODO: Implement all the command methods for the GUI
    
    def refresh_journal_list(self):
        """Refresh the list of available journals"""
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        self.journal_listbox.delete(0, tk.END)
        
        try:
            journals = list_json_files(logs_dir)
            for journal in journals:
                self.journal_listbox.insert(tk.END, journal)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list journals: {e}")
    
    def load_selected_journal(self):
        """Load the selected journal from the list"""
        selection = self.journal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a journal first")
            return
            
        journal_name = self.journal_listbox.get(selection[0])
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        journal_path = os.path.join(logs_dir, journal_name)
        
        try:
            self.journal_data = load_journal(journal_path)
            self.current_journal_path = journal_path
            self.update_all_tabs()
            self.notebook.select(1)  # Switch to journal tab
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load journal: {e}")
    
    def create_new_journal(self):
        """Create a new journal from template"""
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "journal_template.json")
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        
        try:
            # Create a dialog to get character info
            dialog = tk.Toplevel(self.root)
            dialog.title("Create New Journal")
            
            # Character name
            ttk.Label(dialog, text="Character name:").grid(row=0, column=0, padx=5, pady=5)
            name_entry = ttk.Entry(dialog)
            name_entry.grid(row=0, column=1, padx=5, pady=5)
            
            # Character class
            ttk.Label(dialog, text="Character class:").grid(row=1, column=0, padx=5, pady=5)
            class_entry = ttk.Entry(dialog)
            class_entry.grid(row=1, column=1, padx=5, pady=5)
            
            # Starting HP
            ttk.Label(dialog, text="Starting HP:").grid(row=2, column=0, padx=5, pady=5)
            hp_entry = ttk.Spinbox(dialog, from_=1, to=999)
            hp_entry.grid(row=2, column=1, padx=5, pady=5)
            
            # Hit dice
            ttk.Label(dialog, text="Hit dice:").grid(row=3, column=0, padx=5, pady=5)
            hit_dice_entry = ttk.Entry(dialog)
            hit_dice_entry.grid(row=3, column=1, padx=5, pady=5)
            
            def on_submit():
                try:
                    journal_data = load_journal(template_path)
                    journal_data["character"]["name"] = name_entry.get()
                    journal_data["character"]["class"] = class_entry.get()
                    journal_data["character"]["hp"] = int(hp_entry.get())
                    journal_data["character"]["hit_dice"] = hit_dice_entry.get()
                    
                    # Create filename
                    safe_name = journal_data["character"]["name"].lower().replace(" ", "_")
                    filename = f"{safe_name}.json"
                    filepath = os.path.join(logs_dir, filename)
                    
                    # Save the new journal
                    os.makedirs(logs_dir, exist_ok=True)
                    if save_journal(journal_data, filepath):
                        messagebox.showinfo("Success", f"Created new journal at {filepath}")
                        self.journal_data = journal_data
                        self.current_journal_path = filepath
                        self.update_all_tabs()
                        self.notebook.select(1)  # Switch to journal tab
                        dialog.destroy()
                        self.refresh_journal_list()
                    else:
                        messagebox.showerror("Error", "Failed to create journal")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create journal: {e}")
            
            ttk.Button(dialog, text="Create", command=on_submit).grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create journal: {e}")
    
    def add_journal_entry(self):
        """Add a new journal entry"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        date = self.entry_date.get()
        title = self.entry_title.get()
        content = self.entry_content.get("1.0", tk.END).strip()
        
        if not title or not content:
            messagebox.showwarning("Warning", "Title and content are required")
            return
            
        entry = {
            "date": date if date else None,
            "title": title,
            "content": content
        }
        
        try:
            self.journal_data = add_journal_entry(self.journal_data, entry)
            if save_journal(self.journal_data, self.current_journal_path):
                messagebox.showinfo("Success", "Journal entry added")
                self.entry_date.delete(0, tk.END)
                self.entry_title.delete(0, tk.END)
                self.entry_content.delete("1.0", tk.END)
                self.update_journal_entries()
            else:
                messagebox.showerror("Error", "Failed to save journal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {e}")
    
    def add_inventory_item(self):
        """Add a new inventory item"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Inventory Item")
        
        # Item name
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Quantity
        ttk.Label(dialog, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = ttk.Spinbox(dialog, from_=1, to=999)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=2, column=0, padx=5, pady=5)
        desc_entry = ttk.Entry(dialog)
        desc_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def on_submit():
            try:
                item = {
                    "name": name_entry.get(),
                    "quantity": int(quantity_entry.get()),
                    "description": desc_entry.get()
                }
                
                inventory = self.journal_data.get("inventory", [])
                inventory.append(item)
                self.journal_data["inventory"] = inventory
                
                if save_journal(self.journal_data, self.current_journal_path):
                    messagebox.showinfo("Success", "Item added to inventory")
                    self.update_inventory_list()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save inventory")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add item: {e}")
        
        ttk.Button(dialog, text="Add", command=on_submit).grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
    
    def remove_inventory_item(self):
        """Remove selected inventory item"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        selection = self.inventory_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
            
        idx = selection[0]
        inventory = self.journal_data.get("inventory", [])
        
        if 0 <= idx < len(inventory):
            item_name = inventory[idx].get("name", "item")
            if messagebox.askyesno("Confirm", f"Remove {item_name} from inventory?"):
                inventory.pop(idx)
                self.journal_data["inventory"] = inventory
                
                if save_journal(self.journal_data, self.current_journal_path):
                    messagebox.showinfo("Success", "Item removed from inventory")
                    self.update_inventory_list()
                else:
                    messagebox.showerror("Error", "Failed to save inventory")
    
    def add_quest(self):
        """Add a new quest"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Quest")
        
        # Quest title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        desc_entry = scrolledtext.ScrolledText(dialog, width=40, height=5)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Giver
        ttk.Label(dialog, text="Quest Giver:").grid(row=2, column=0, padx=5, pady=5)
        giver_entry = ttk.Entry(dialog)
        giver_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Start date
        ttk.Label(dialog, text="Start Date:").grid(row=3, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(dialog)
        date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def on_submit():
            try:
                quest = {
                    "title": title_entry.get(),
                    "description": desc_entry.get("1.0", tk.END).strip(),
                    "giver": giver_entry.get(),
                    "started": date_entry.get() if date_entry.get() else None
                }
                
                quests = self.journal_data.get("quests", {"active": [], "completed": [], "rumors": []})
                quests["active"].append(quest)
                self.journal_data["quests"] = quests
                
                if save_journal(self.journal_data, self.current_journal_path):
                    messagebox.showinfo("Success", "Quest added")
                    self.update_quests_lists()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save quest")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add quest: {e}")
        
        ttk.Button(dialog, text="Add Quest", command=on_submit).grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
    
    def complete_quest(self):
        """Mark selected quest as completed"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        selection = self.active_quests.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a quest to complete")
            return
            
        idx = selection[0]
        quests = self.journal_data.get("quests", {"active": [], "completed": [], "rumors": []})
        
        if 0 <= idx < len(quests["active"]):
            quest = quests["active"][idx]
            quest_title = quest.get("title", "Unnamed quest")
            
            dialog = tk.Toplevel(self.root)
            dialog.title("Complete Quest")
            
            ttk.Label(dialog, text=f"Complete '{quest_title}'?").pack(padx=10, pady=5)
            ttk.Label(dialog, text="Completion Date:").pack(padx=10, pady=5)
            date_entry = ttk.Entry(dialog)
            date_entry.pack(padx=10, pady=5)
            
            def on_submit():
                try:
                    completed_quest = quests["active"].pop(idx)
                    completed_quest["completed_date"] = date_entry.get() if date_entry.get() else None
                    quests["completed"].append(completed_quest)
                    self.journal_data["quests"] = quests
                    
                    if save_journal(self.journal_data, self.current_journal_path):
                        messagebox.showinfo("Success", "Quest marked as completed")
                        self.update_quests_lists()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Failed to save quest")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to complete quest: {e}")
            
            ttk.Button(dialog, text="Complete", command=on_submit).pack(padx=10, pady=10)
    
    def add_rumor(self):
        """Add a new rumor"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Rumor")
        
        # Rumor title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        desc_entry = scrolledtext.ScrolledText(dialog, width=40, height=5)
        desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Source
        ttk.Label(dialog, text="Source:").grid(row=2, column=0, padx=5, pady=5)
        source_entry = ttk.Entry(dialog)
        source_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Date heard
        ttk.Label(dialog, text="Date Heard:").grid(row=3, column=0, padx=5, pady=5)
        date_entry = ttk.Entry(dialog)
        date_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def on_submit():
            try:
                rumor = {
                    "title": title_entry.get(),
                    "description": desc_entry.get("1.0", tk.END).strip(),
                    "source": source_entry.get(),
                    "heard_date": date_entry.get() if date_entry.get() else None
                }
                
                quests = self.journal_data.get("quests", {"active": [], "completed": [], "rumors": []})
                quests["rumors"].append(rumor)
                self.journal_data["quests"] = quests
                
                if save_journal(self.journal_data, self.current_journal_path):
                    messagebox.showinfo("Success", "Rumor added")
                    self.update_quests_lists()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save rumor")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add rumor: {e}")
        
        ttk.Button(dialog, text="Add Rumor", command=on_submit).grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
    
    def save_character(self):
        """Save character changes"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load or create a journal first")
            return
            
        try:
            character = {
                "name": self.char_name.get(),
                "class": self.char_class.get(),
                "level": int(self.char_level.get()),
                "hp": int(self.char_hp.get()),
                "hit_dice": self.char_hit_dice.get()
            }
            
            self.journal_data["character"] = character
            
            if save_journal(self.journal_data, self.current_journal_path):
                messagebox.showinfo("Success", "Character saved")
            else:
                messagebox.showerror("Error", "Failed to save character")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save character: {e}")
    
    def import_journal(self):
        """Import a journal file"""
        # TODO: Implement journal import
        pass
    
    def export_journal(self):
        """Export current journal"""
        # TODO: Implement journal export
        pass
    
    def update_all_tabs(self):
        """Update all tabs with current journal data"""
        if not self.journal_data:
            return
            
        # Update character tab
        character = self.journal_data.get("character", {})
        self.char_name.delete(0, tk.END)
        self.char_name.insert(0, character.get("name", ""))
        self.char_class.delete(0, tk.END)
        self.char_class.insert(0, character.get("class", ""))
        self.char_level.delete(0, tk.END)
        self.char_level.insert(0, character.get("level", 1))
        self.char_hp.delete(0, tk.END)
        self.char_hp.insert(0, character.get("hp", 0))
        self.char_hit_dice.delete(0, tk.END)
        self.char_hit_dice.insert(0, character.get("hit_dice", ""))
        
        # Update journal entries
        self.update_journal_entries()
        
        # Update inventory
        self.update_inventory_list()
        
        # Update quests
        self.update_quests_lists()
    
    def update_journal_entries(self):
        """Update the recent journal entries display"""
        self.recent_entries.config(state=tk.NORMAL)
        self.recent_entries.delete(1.0, tk.END)
        
        entries = self.journal_data.get("journal_log", [])
        for entry in entries[-5:]:  # Show last 5 entries
            if isinstance(entry, dict):
                date = entry.get("date", "Unknown date")
                title = entry.get("title", "Untitled entry")
                content = entry.get("content", "")
                
                self.recent_entries.insert(tk.END, f"[{date}] {title}\n")
                if content:
                    self.recent_entries.insert(tk.END, f"{content[:100]}...\n\n" if len(content) > 100 else f"{content}\n\n")
        
        self.recent_entries.config(state=tk.DISABLED)
    
    def update_inventory_list(self):
        """Update the inventory list display"""
        self.inventory_listbox.delete(0, tk.END)
        
        inventory = self.journal_data.get("inventory", [])
        for item in inventory:
            if isinstance(item, dict):
                name = item.get("name", "Unknown item")
                quantity = item.get("quantity", 1)
                self.inventory_listbox.insert(tk.END, f"{name} (x{quantity})")
            else:
                self.inventory_listbox.insert(tk.END, str(item))
    
    def update_quests_lists(self):
        """Update the quests lists display"""
        self.active_quests.delete(0, tk.END)
        self.completed_quests.delete(0, tk.END)
        self.rumors.delete(0, tk.END)
        
        quests = self.journal_data.get("quests", {})
        
        # Active quests
        for quest in quests.get("active", []):
            if isinstance(quest, dict):
                self.active_quests.insert(tk.END, quest.get("title", "Unnamed quest"))
            else:
                self.active_quests.insert(tk.END, str(quest))
        
        # Completed quests
        for quest in quests.get("completed", []):
            if isinstance(quest, dict):
                self.completed_quests.insert(tk.END, quest.get("title", "Unnamed quest"))
            else:
                self.completed_quests.insert(tk.END, str(quest))
        
        # Rumors
        for rumor in quests.get("rumors", []):
            if isinstance(rumor, dict):
                self.rumors.insert(tk.END, rumor.get("title", "Unnamed rumor"))
            else:
                self.rumors.insert(tk.END, str(rumor))

def main():
    root = tk.Tk()
    app = DnDJournalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()