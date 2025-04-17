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
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("No journal loaded")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Import button
        import_btn = ttk.Button(self.root, text="Import Updated Log", command=self.import_updated_log)
        import_btn.pack(side=tk.TOP, padx=5, pady=5)
        
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
        self.create_settings_tab()
        
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
        
        # Completed quests list
        completed_list_frame = ttk.Frame(completed_frame)
        completed_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.completed_quests = tk.Listbox(completed_list_frame)
        self.completed_quests.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # View Full Log button
        view_log_btn = ttk.Button(completed_list_frame, text="View Full Log",
                                command=self.view_full_quest_log)
        view_log_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
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

    def view_full_quest_log(self):
        """Show the full detailed log for a completed quest"""
        selection = self.completed_quests.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a quest first")
            return
            
        idx = selection[0]
        quests = self.journal_data.get("quests", {}).get("completed", [])
        if idx >= len(quests):
            return
            
        quest = quests[idx]
        if "detailed_log" not in quest:
            messagebox.showwarning("Warning",
                                 "This quest has no detailed log. Please update the journal data to include structured quest notes.")
            return
            
        log = quest["detailed_log"]
        
        # Create detail window
        detail_win = tk.Toplevel(self.root)
        detail_win.title(f"Quest Log: {quest.get('title', 'Untitled Quest')}")
        detail_win.geometry("700x800")
        
        # Main container with scrollbar
        container = ttk.Frame(detail_win)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Helper function to add sections
        def add_section(parent, title, content, is_list=False):
            frame = ttk.LabelFrame(parent, text=title)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            if is_list and isinstance(content, list):
                for item in content:
                    ttk.Label(frame, text=f"• {item}", wraplength=650).pack(anchor="w", padx=5, pady=2)
            elif content:
                text = tk.Text(frame, wrap=tk.WORD, height=4, width=80)
                text.insert("1.0", content)
                text.config(state="disabled")
                text.pack(fill=tk.X, padx=5, pady=5)
            else:
                ttk.Label(frame, text="No information available", foreground="gray").pack()
        
        # Add all sections in order
        add_section(scrollable_frame, "📍 Setting", log.get("setting"))
        add_section(scrollable_frame, "❗ Trigger", log.get("trigger"))
        add_section(scrollable_frame, "🧠 Player Choices", log.get("player_choices"), is_list=True)
        add_section(scrollable_frame, "☠️ Enemy", log.get("enemy"))
        add_section(scrollable_frame, "⚔️ Combat Notes", log.get("combat_notes"), is_list=True)
        add_section(scrollable_frame, "🧍 Aftermath", log.get("aftermath"))
        add_section(scrollable_frame, "💭 Character Notes", log.get("character_notes"), is_list=True)
        add_section(scrollable_frame, "⭐ Why It Matters", log.get("why_it_matters"))
        
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
        
    def create_settings_tab(self):
        """Create the settings tab with import/export and QoL features"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")
        
        # Backup Section
        backup_frame = ttk.LabelFrame(tab, text="Backup & Restore", padding=10)
        backup_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(backup_frame, text="Create Backup",
                 command=self.create_backup).pack(fill=tk.X, pady=2)
        ttk.Button(backup_frame, text="Restore Backup",
                 command=self.restore_backup).pack(fill=tk.X, pady=2)
        
        # Import/Export Section
        transfer_frame = ttk.LabelFrame(tab, text="Data Transfer", padding=10)
        transfer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(transfer_frame, text="Import Journal",
                 command=self.import_journal).pack(fill=tk.X, pady=2)
        ttk.Button(transfer_frame, text="Export Current Journal",
                 command=self.export_journal).pack(fill=tk.X, pady=2)
        
        # QoL Features Section
        qol_frame = ttk.LabelFrame(tab, text="Quality of Life", padding=10)
        qol_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Auto-save toggle
        self.auto_save_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(qol_frame, text="Enable Auto-Save",
                       variable=self.auto_save_var).pack(anchor=tk.W, pady=2)
        
        # Quick summary button
        ttk.Button(qol_frame, text="Show Current Summary",
                 command=self.show_current_summary).pack(fill=tk.X, pady=2)
        
        # Theme selector
        theme_frame = ttk.Frame(qol_frame)
        theme_frame.pack(fill=tk.X, pady=5)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value="default")
        ttk.Combobox(theme_frame, textvariable=self.theme_var,
                    values=["default", "light", "dark"]).pack(side=tk.LEFT, padx=5)

    def create_backup(self):
        """Create a timestamped backup of current journal"""
        if not self.current_journal_path:
            messagebox.showwarning("Warning", "No journal loaded to backup")
            return
            
        backup_dir = os.path.join(os.path.dirname(self.current_journal_path), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{os.path.basename(self.current_journal_path)}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        try:
            shutil.copy2(self.current_journal_path, backup_path)
            messagebox.showinfo("Success", f"Backup created at:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {e}")

    def restore_backup(self):
        """Restore from a backup file"""
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = filedialog.askopenfilename(
            initialdir=backup_dir,
            title="Select Backup to Restore",
            filetypes=[("JSON files", "*.json")]
        )
        
        if not backup_file:
            return
            
        try:
            # Load the backup to verify it's valid
            test_load = load_journal(backup_file)
            
            # Get original filename from backup name
            original_name = "_".join(backup_file.split("_")[2:])
            restore_path = os.path.join(os.path.dirname(backup_file), "..", original_name)
            
            if messagebox.askyesno("Confirm", f"Restore {original_name} from backup?"):
                shutil.copy2(backup_file, restore_path)
                
                # Reload if it was the current journal
                if self.current_journal_path == restore_path:
                    self.journal_data = test_load
                    self.update_all_tabs()
                
                messagebox.showinfo("Success", "Journal restored successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore backup: {e}")

    def show_current_summary(self):
        """Display a summary of the current journal"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "No journal loaded")
            return
            
        summary_win = tk.Toplevel(self.root)
        summary_win.title("Journal Summary")
        
        text = scrolledtext.ScrolledText(summary_win, width=80, height=25)
        text.pack(padx=10, pady=10)
        
        # Redirect print output to the text widget
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        print_summary(self.journal_data)
        
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        text.insert(tk.END, output)
        text.config(state=tk.DISABLED)
        
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
            self.status_var.set(f"Loaded: {journal_name}")
            self.update_all_tabs()
            self.notebook.select(1)  # Switch to journal tab
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load journal: {e}")
    
    def import_updated_log(self):
        """Import an updated journal file and overwrite an existing one"""
        if not self.journal_data:
            messagebox.showwarning("Warning", "Please load a journal first")
            return
            
        # Step 1: Select the updated file
        updated_file = filedialog.askopenfilename(
            title="Select Updated Journal File",
            filetypes=[("JSON files", "*.json")]
        )
        
        if not updated_file:
            return  # User cancelled
            
        try:
            updated_data = load_journal(updated_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load updated file: {e}")
            return
            
        # Step 2: Select target file to overwrite
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        target_file = filedialog.askopenfilename(
            title="Select Target Journal to Overwrite",
            initialdir=logs_dir,
            filetypes=[("JSON files", "*.json")]
        )
        
        if not target_file:
            return  # User cancelled
            
        # Confirm overwrite
        if not messagebox.askyesno("Confirm Overwrite",
                                 f"Overwrite {os.path.basename(target_file)} with {os.path.basename(updated_file)}?"):
            return
            
        # Perform the overwrite
        try:
            if save_journal(updated_data, target_file):
                messagebox.showinfo("Success", "Journal updated successfully")
                
                # If we overwrote the currently loaded file, reload it
                if target_file == self.current_journal_path:
                    self.journal_data = updated_data
                    self.update_all_tabs()
            else:
                messagebox.showerror("Error", "Failed to save updated journal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update journal: {e}")
    
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
    
    def show_quest_details(self, quest_type, index):
        """Show detailed view of a quest"""
        quest = self.journal_data.get("quests", {}).get(quest_type, [])[index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Quest Details - {quest.get('title', 'Untitled')}")
        
        details = scrolledtext.ScrolledText(dialog, width=60, height=15)
        details.pack(padx=10, pady=10)
        
        text = f"Title: {quest.get('title', 'Untitled')}\n\n"
        text += f"Description:\n{quest.get('description', '')}\n\n"
        
        if quest_type in ["active", "completed"]:
            text += f"Giver: {quest.get('giver', 'Unknown')}\n"
            text += f"Started: {quest.get('started', 'Unknown')}\n"
            if quest_type == "completed":
                text += f"Completed: {quest.get('completed_date', 'Unknown')}\n"
        elif quest_type == "rumors":
            text += f"Source: {quest.get('source', 'Unknown')}\n"
            text += f"Heard: {quest.get('heard_date', 'Unknown')}\n"
            
        details.insert(tk.END, text)
        details.config(state=tk.DISABLED)
        
    def update_quests_lists(self):
        """Update the quests lists display"""
        self.active_quests.delete(0, tk.END)
        self.completed_quests.delete(0, tk.END)
        self.rumors.delete(0, tk.END)
        
        quests = self.journal_data.get("quests", {})
        
        # Active quests
        for quest in quests.get("active", []):
            title = quest.get("title", "Unnamed quest") if isinstance(quest, dict) else str(quest)
            self.active_quests.insert(tk.END, title)
        
        # Completed quests
        for quest in quests.get("completed", []):
            title = quest.get("title", "Unnamed quest") if isinstance(quest, dict) else str(quest)
            self.completed_quests.insert(tk.END, title)
        
        # Rumors
        for rumor in quests.get("rumors", []):
            title = rumor.get("title", "Unnamed rumor") if isinstance(rumor, dict) else str(rumor)
            self.rumors.insert(tk.END, title)
        
        # Bind double-click to show details
        self.active_quests.bind("<Double-1>", lambda e: self.show_quest_details("active", self.active_quests.curselection()[0]))
        self.completed_quests.bind("<Double-1>", lambda e: self.show_quest_details("completed", self.completed_quests.curselection()[0]))
        self.rumors.bind("<Double-1>", lambda e: self.show_quest_details("rumors", self.rumors.curselection()[0]))

def main():
    root = tk.Tk()
    app = DnDJournalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()