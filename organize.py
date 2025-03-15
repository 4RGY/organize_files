import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import datetime


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f0f0")
        self.base_folder = None
        self.log_entries = []

        # Define default keywords mapping
        self.file_mappings = {
            "00_Jokian": ["0000", "jokian", "orderan"],
            "01_Tugas_Transformasi_Digital": ["0001", "tugasTransformasi"],
            "02_Tugas_Kecakapan_Antarpersonal": ["0002", "tugasKecakapan"],
            "03_Tugas_Pemrograman": ["0003", "tugasPemrograman"],
            "04_Tugas_Manajemen_Proyek": ["0004", "tugasManajemen"],
            "05_Tugas_Design_Interface_User": ["0005", "tugasDesign", "tugasui", "tugasux"],
            "06_Tugas_Analisa_Dan_Perancangan_Sistem": ["0006", "tugasPerancangan"],
            "07_Tugas_Sistem_Basis_Data": ["00007", "tugasDatabase"],
            "08_Tugas_Praktikum_Basis_Data": ["0008", "praktikumBasis"],
            "01_Transformasi_Digital": ["0009", "Transformasi_Digital"],
            "02_Kecakapan_Antarpersonal": ["0010", "Kecapakan_Antarpersonal"],
            "03_Pemrograman": ["0011", "Pemrograman"],
            "04_Manajemen_Proyek": ["0012", "Manajemen_Proyek"],
            "05_Design_Interface_User": ["0013", "Design_Interface_User", "ui", "ux"],
            "06_Analisa_Dan_Perancangan_Sistem": ["0014", "Analisa_Dan_Perancangan_Sistem"],
            "07_Sistem_Basis_Data": ["0015", "Sistem_Basis_Data"],
            "08_Praktikum_Basis_Data": ["0016", "Praktikum_Basis_Data"],
        }

        # Create a style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", font=("Arial", 11), background="#f0f0f0")
        self.style.configure("Tab.TNotebook", background="#f0f0f0")

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)

        header_label = ttk.Label(
            header_frame, text="File Organizer", font=("Arial", 18, "bold")
        )
        header_label.pack()

        description = ttk.Label(
            header_frame,
            text="Organize your files into structured folders",
            font=("Arial", 10),
        )
        description.pack(pady=5)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill=tk.X, pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Main tab
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Main")

        # Keywords tab
        keywords_tab = ttk.Frame(notebook)
        notebook.add(keywords_tab, text="Keywords")

        # Logs tab
        logs_tab = ttk.Frame(notebook)
        notebook.add(logs_tab, text="Activity Logs")

        # Setup main tab content
        self.setup_main_tab(main_tab)

        # Setup keywords tab content
        self.setup_keywords_tab(keywords_tab)

        # Setup logs tab content
        self.setup_logs_tab(logs_tab)

    def setup_main_tab(self, parent):
        # Content frame
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Base folder selection
        base_folder_frame = ttk.Frame(content_frame)
        base_folder_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            base_folder_frame,
            text="Step 1: Select base folder for organization",
            font=("Arial", 11, "bold"),
        ).pack(anchor=tk.W)

        base_folder_entry_frame = ttk.Frame(base_folder_frame)
        base_folder_entry_frame.pack(fill=tk.X, pady=5)

        self.base_folder_var = tk.StringVar()
        base_folder_entry = ttk.Entry(
            base_folder_entry_frame, textvariable=self.base_folder_var, width=40
        )
        base_folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        base_folder_button = ttk.Button(
            base_folder_entry_frame, text="Browse", command=self.select_base_folder
        )
        base_folder_button.pack(side=tk.RIGHT, padx=5)

        # Action buttons
        action_frame = ttk.Frame(content_frame)
        action_frame.pack(fill=tk.X, pady=20)

        self.create_structure_button = ttk.Button(
            action_frame, text="Create Folder Structure", command=self.create_folders
        )
        self.create_structure_button.pack(pady=5, padx=50, fill=tk.X)

        self.organize_button = ttk.Button(
            action_frame,
            text="Organize Files From 02_File_Berantakan",
            command=self.organize_files,
        )
        self.organize_button.pack(pady=5, padx=50, fill=tk.X)

        # New button for saving logs
        self.save_log_button = ttk.Button(
            action_frame,
            text="Save Activity Log",
            command=self.save_log,
            state=tk.DISABLED,
        )
        self.save_log_button.pack(pady=5, padx=50, fill=tk.X)

        # Status frame
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill=tk.X, pady=10)

        self.status_var = tk.StringVar(value="Ready to organize")
        self.status_label = ttk.Label(
            self.status_frame,
            textvariable=self.status_var,
            font=("Arial", 10, "italic"),
        )
        self.status_label.pack()

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=10)
        self.progress_bar.pack_forget()  # Hidden by default

    def setup_keywords_tab(self, parent):
        # Create a frame for the keywords tab
        keywords_frame = ttk.Frame(parent, padding="10")
        keywords_frame.pack(fill=tk.BOTH, expand=True)

        # Title and instructions
        ttk.Label(
            keywords_frame,
            text="Keywords Configuration",
            font=("Arial", 14, "bold"),
        ).pack(anchor=tk.W, pady=(0, 10))

        ttk.Label(
            keywords_frame,
            text="Each folder has associated keywords. Files containing these keywords will be moved to the corresponding folder.",
            wraplength=700,
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create a scrollable frame for keyword entries
        self.keyword_entries = {}

        # Create a canvas with scrollbar
        canvas_frame = ttk.Frame(keywords_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        inner_frame = ttk.Frame(canvas, padding="5")

        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Add keyword entries for each folder
        row = 0
        for folder, keywords in self.file_mappings.items():
            # Get parent folder
            parent_folder = "00_Tugas_dan_Joki" if "Tugas" in folder or "Jokian" in folder else "01_Materi"

            # Create entry for each folder
            folder_frame = ttk.Frame(inner_frame)
            folder_frame.grid(row=row, column=0, sticky='ew', pady=5)

            # Folder label with parent info
            folder_label = ttk.Label(
                folder_frame,
                text=f"{parent_folder} / {folder}:",
                width=40,
                font=("Arial", 10, "bold"),
            )
            folder_label.grid(row=0, column=0, sticky='w')

            # Keywords entry
            keywords_var = tk.StringVar(value=", ".join(keywords))
            keywords_entry = ttk.Entry(folder_frame, textvariable=keywords_var, width=50)
            keywords_entry.grid(row=0, column=1, padx=5)

            # Store entry reference
            self.keyword_entries[folder] = keywords_var

            row += 1

        # Button to save keywords
        save_keywords_button = ttk.Button(
            keywords_frame,
            text="Save Keywords",
            command=self.save_keywords,
        )
        save_keywords_button.pack(pady=10)

        # Update canvas scrollregion when inner_frame changes size
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind('<Configure>', configure_canvas)

        # Update canvas width when the window is resized
        def on_frame_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind('<Configure>', on_frame_configure)

    def setup_logs_tab(self, parent):
        # Create a frame for the logs tab
        logs_frame = ttk.Frame(parent, padding="10")
        logs_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            logs_frame,
            text="Activity Log Monitor",
            font=("Arial", 14, "bold"),
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create text area for logs
        self.log_text = scrolledtext.ScrolledText(
            logs_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Courier", 10),
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.log_text.config(state=tk.DISABLED)

        # Buttons frame
        log_buttons_frame = ttk.Frame(logs_frame)
        log_buttons_frame.pack(fill=tk.X, pady=10)

        # Clear log button
        clear_log_button = ttk.Button(
            log_buttons_frame,
            text="Clear Log Display",
            command=self.clear_log_display,
        )
        clear_log_button.pack(side=tk.LEFT, padx=5)

        # Save log button (duplicate of the one on main tab)
        save_log_button_copy = ttk.Button(
            log_buttons_frame,
            text="Save Log to File",
            command=self.save_log,
        )
        save_log_button_copy.pack(side=tk.LEFT, padx=5)

        # Refresh log button
        refresh_log_button = ttk.Button(
            log_buttons_frame,
            text="Refresh Log Display",
            command=self.refresh_log_display,
        )
        refresh_log_button.pack(side=tk.LEFT, padx=5)

        # Summary frame
        summary_frame = ttk.LabelFrame(logs_frame, text="Log Summary")
        summary_frame.pack(fill=tk.X, pady=10)

        # Summary labels
        self.log_stats_var = tk.StringVar(value="Total entries: 0 | Files moved: 0 | Errors: 0")
        ttk.Label(
            summary_frame,
            textvariable=self.log_stats_var,
            font=("Arial", 10),
        ).pack(pady=5)

        # Latest activity label
        self.latest_activity_var = tk.StringVar(value="No activity recorded yet")
        ttk.Label(
            summary_frame,
            text="Latest activity:",
            font=("Arial", 10, "bold"),
        ).pack(anchor=tk.W, padx=5)
        ttk.Label(
            summary_frame,
            textvariable=self.latest_activity_var,
            font=("Arial", 10),
            wraplength=700,
        ).pack(pady=5, padx=5, anchor=tk.W)

    def select_base_folder(self):
        folder = filedialog.askdirectory(title="Select Base Folder")
        if folder:
            self.base_folder = folder
            self.base_folder_var.set(folder)
            self.add_log_entry(f"Base folder selected: {folder}")

    def create_folders(self):
        if not self.base_folder:
            messagebox.showwarning("Warning", "Please select a base folder first.")
            return

        structure = {
            "00_Tugas_dan_Joki": [
                "00_Jokian",
                "01_Tugas_Transformasi_Digital",
                "02_Tugas_Kecakapan_Antarpersonal",
                "03_Tugas_Pemrograman",
                "04_Tugas_Manajemen_Proyek",
                "05_Tugas_Design_Interface_User",
                "06_Tugas_Analisa_Dan_Perancangan_Sistem",
                "07_Tugas_Sistem_Basis_Data",
                "08_Tugas_Praktikum_Basis_Data",
            ],
            "01_Materi": [
                "01_Transformasi_Digital",
                "02_Kecakapan_Antarpersonal",
                "01_Transformasi_Digital",
                "02_Kecakapan_Antarpersonal",
                "03_Pemrograman",
                "04_Manajemen_Proyek",
                "05_Design_Interface_User",
                "06_Analisa_Dan_Perancangan_Sistem",
                "07_Sistem_Basis_Data",
                "08_Praktikum_Basis_Data",
            ],
            "02_File_Berantakan": [],  # This is where disorganized files will be placed initially
        }

        try:
            created_folders = []
            for folder, subfolders in structure.items():
                folder_path = os.path.join(self.base_folder, folder)
                os.makedirs(folder_path, exist_ok=True)
                created_folders.append(folder_path)

                for subfolder in subfolders:
                    subfolder_path = os.path.join(folder_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
                    created_folders.append(subfolder_path)

            self.add_log_entry(
                f"Created folder structure with {len(created_folders)} folders"
            )
            messagebox.showinfo("Success", "Folder structure created successfully!")
            self.status_var.set("Folder structure created. Ready to organize files.")
            self.update_log_stats()
        except Exception as e:
            error_msg = f"Error creating folder structure: {str(e)}"
            self.add_log_entry(error_msg, error=True)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_log_stats()

    def save_keywords(self):
        """Save the updated keywords from the GUI to the file_mappings dictionary"""
        try:
            # Update the file_mappings dictionary with values from the GUI
            for folder, keywords_var in self.keyword_entries.items():
                # Get the keywords string from the entry field
                keywords_str = keywords_var.get()
                # Split by comma and strip whitespace
                keywords_list = [
                    k.strip() for k in keywords_str.split(",") if k.strip()
                ]
                # Update the file_mappings dictionary
                self.file_mappings[folder] = keywords_list

            self.add_log_entry("Keywords updated successfully")
            messagebox.showinfo("Success", "Keywords saved successfully!")
            self.update_log_stats()
        except Exception as e:
            error_msg = f"Error saving keywords: {str(e)}"
            self.add_log_entry(error_msg, error=True)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_log_stats()

    def move_files(self):
        """Move files based on the keywords in file_mappings"""
        # Source folder is the "02_File_Berantakan" folder
        source_folder = os.path.join(self.base_folder, "02_File_Berantakan")
        if not os.path.exists(source_folder):
            error_msg = "02_File_Berantakan folder not found."
            self.add_log_entry(error_msg, error=True)
            messagebox.showwarning("Warning", error_msg)
            self.update_log_stats()
            return

        files = os.listdir(source_folder)
        total_files = len(files)

        if total_files == 0:
            msg = "No files found in 02_File_Berantakan folder."
            self.add_log_entry(msg)
            messagebox.showinfo("Info", msg)
            self.update_log_stats()
            return

        moved_files = 0
        file_moves = []  # Track individual file moves

        for i, file in enumerate(files):
            file_path = os.path.join(source_folder, file)
            if os.path.isfile(file_path):
                matched = False
                for folder, keywords in self.file_mappings.items():
                    if any(keyword.lower() in file.lower() for keyword in keywords):
                        destination_parent = (
                            "00_Tugas_dan_Joki"
                            if "Tugas" in folder or "Jokian" in folder
                            else "01_Materi"
                        )
                        destination = os.path.join(
                            self.base_folder,
                            destination_parent,
                            folder,
                        )
                        destination_path = os.path.join(destination, file)

                        try:
                            shutil.move(file_path, destination_path)
                            move_msg = (
                                f"Moved '{file}' to {destination_parent}/{folder}"
                            )
                            file_moves.append(move_msg)
                            self.add_log_entry(move_msg, indent=True)
                            matched = True
                            moved_files += 1
                            self.update_stats("files_moved", 1)
                            break
                        except Exception as e:
                            error_msg = f"Error moving '{file}': {str(e)}"
                            self.add_log_entry(error_msg, error=True, indent=True)
                            file_moves.append(error_msg)
                            break

                # If no match found, file stays in 02_File_Berantakan
                if not matched:
                    no_match_msg = (
                        f"No match for '{file}' - remained in 02_File_Berantakan"
                    )
                    file_moves.append(no_match_msg)
                    self.add_log_entry(no_match_msg, indent=True)

                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing... {i+1}/{total_files} files")
                self.root.update()

        summary = f"Completed organization: {moved_files}/{total_files} files moved"
        self.add_log_entry(summary)
        self.update_log_stats()

        self.status_var.set(
            f"Complete! {moved_files}/{total_files} files organized successfully."
        )
        self.save_log_button.config(
            state=tk.NORMAL
        )  # Enable log saving after organization

    def organize_files(self):
        if not self.base_folder:
            messagebox.showwarning("Warning", "Please select a base folder first.")
            return

        # Show progress bar
        self.progress_bar.pack(fill=tk.X, pady=10)
        self.status_var.set("Starting file organization...")
        self.organize_button.config(state=tk.DISABLED)
        self.create_structure_button.config(state=tk.DISABLED)
        self.save_log_button.config(state=tk.DISABLED)

        # Log the start of organization
        self.add_log_entry("Starting file organization")

        # Run the organization in a separate thread to keep GUI responsive
        threading.Thread(target=self.organize_thread, daemon=True).start()

    def organize_thread(self):
        try:
            self.move_files()
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Success", "Files have been organized successfully!"
                ),
            )
        except Exception as e:
            error_msg = f"Error during file organization: {str(e)}"
            self.add_log_entry(error_msg, error=True)
            self.root.after(
                0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}")
            )
        finally:
            self.root.after(0, lambda: self.progress_bar.pack_forget())
            self.root.after(0, lambda: self.organize_button.config(state=tk.NORMAL))
            self.root.after(
                0, lambda: self.create_structure_button.config(state=tk.NORMAL)
            )
            self.update_log_stats()

    def add_log_entry(self, message, indent=False, error=False):
        """Add an entry to the activity log with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = "    " if indent else ""
        error_prefix = "[ERROR] " if error else ""
        entry = f"{timestamp}: {prefix}{error_prefix}{message}"
        self.log_entries.append(entry)

        # Update log display
        self.update_log_display(entry)

        # Update latest activity
        self.latest_activity_var.set(message)

        # Update stats
        self.update_stats("total_entries", 1)
        if error:
            self.update_stats("errors", 1)

    def update_stats(self, stat_name, value):
        """Update the statistics dictionary"""
        if not hasattr(self, "stats"):
            self.stats = {"total_entries": 0, "files_moved": 0, "errors": 0}

        self.stats[stat_name] = self.stats.get(stat_name, 0) + value
        self.update_log_stats()

    def update_log_stats(self):
        """Update the log statistics display"""
        if not hasattr(self, "stats"):
            self.stats = {"total_entries": 0, "files_moved": 0, "errors": 0}

        # Update the stats display
        if hasattr(self, "log_stats_var"):
            stats_text = f"Total entries: {self.stats.get('total_entries', 0)} | Files moved: {self.stats.get('files_moved', 0)} | Errors: {self.stats.get('errors', 0)}"
            self.log_stats_var.set(stats_text)

    def update_log_display(self, entry=None):
        """Update the log text widget with new entries"""
        if hasattr(self, "log_text"):
            self.log_text.config(state=tk.NORMAL)

            if entry:
                # Add just the new entry
                self.log_text.insert(tk.END, entry + "\n")
            else:
                # Add all entries (for refresh)
                self.log_text.delete(1.0, tk.END)
                for log_entry in self.log_entries:
                    self.log_text.insert(tk.END, log_entry + "\n")

            # Auto-scroll to the end
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

    def refresh_log_display(self):
        """Refresh the entire log display"""
        self.update_log_display()
        self.update_log_stats()

    def clear_log_display(self):
        """Clear only the log display, but keep the entries"""
        if hasattr(self, "log_text"):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state=tk.DISABLED)

    def save_log(self):
        """Save the activity log to a file"""
        if not self.log_entries:
            messagebox.showinfo("Info", "No log entries to save.")
            return

        try:
            log_filename = f"file_organizer_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            log_path = os.path.join(self.base_folder, log_filename)

            with open(log_path, "w") as log_file:
                log_file.write("=== FILE ORGANIZER ACTIVITY LOG ===\n")
                log_file.write(
                    f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                log_file.write(f"Base folder: {self.base_folder}\n")
                log_file.write("=" * 40 + "\n\n")

                # Write statistics
                log_file.write("=== STATISTICS ===\n")
                log_file.write(
                    f"Total log entries: {self.stats.get('total_entries', 0)}\n"
                )
                log_file.write(f"Files moved: {self.stats.get('files_moved', 0)}\n")
                log_file.write(f"Errors: {self.stats.get('errors', 0)}\n")
                log_file.write("=" * 40 + "\n\n")

                # Write keyword mappings
                log_file.write("=== KEYWORD MAPPINGS ===\n")
                for folder, keywords in self.file_mappings.items():
                    log_file.write(f"{folder}: {', '.join(keywords)}\n")
                log_file.write("=" * 40 + "\n\n")

                # Write log entries
                log_file.write("=== ACTIVITY LOG ===\n")
                for entry in self.log_entries:
                    log_file.write(f"{entry}\n")

            self.add_log_entry(f"Log file saved to {log_path}")
            messagebox.showinfo("Success", f"Log saved to:\n{log_path}")
        except Exception as e:
            error_msg = f"Failed to save log: {str(e)}"
            self.add_log_entry(error_msg, error=True)
            messagebox.showerror("Error", error_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
