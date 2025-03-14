import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import datetime


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        self.base_folder = None
        self.log_entries = []

        # Create a style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TLabel", font=("Arial", 11), background="#f0f0f0")

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

        # Content frame
        content_frame = ttk.Frame(main_frame)
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
        self.status_frame = ttk.Frame(main_frame)
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
        except Exception as e:
            error_msg = f"Error creating folder structure: {str(e)}"
            self.add_log_entry(error_msg)
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def move_files(self):
        file_mappings = {
            "00_Jokian": ["joki", "order"],
            "01_Tugas_Transformasi_Digital": ["tugastransformasi", "tugasdigital"],
            "02_Tugas_Kecakapan_Antarpersonal": [
                "tugaskecakapan",
                "tugasantarpersonal",
            ],
            "03_Tugas_Pemrograman": ["tugaspemrograman", "tugascoding"],
            "04_Tugas_Manajemen_Proyek": ["tugasmanajemen", "tugasproyek"],
            "05_Tugas_Design_Interface_User": [
                "tugasdesign",
                "tugasinterface",
                "tugasui",
                "tugasux",
            ],
            "06_Tugas_Analisa_Dan_Perancangan_Sistem": [
                "tugasanalisa",
                "tugasperancangan",
            ],
            "07_Tugas_Sistem_Basis_Data": ["tugasbasisdata", "tugasdatabase"],
            "08_Tugas_Praktikum_Basis_Data": ["tugaspraktikum", "tugasbasisdata"],
            "01_Transformasi_Digital": ["transformasi", "digital"],
            "02_Kecakapan_Antarpersonal": ["kecakapan", "antarpersonal"],
            "03_Pemrograman": ["pemrograman", "coding"],
            "04_Manajemen_Proyek": ["manajemen", "proyek"],
            "05_Design_Interface_User": ["design", "interface", "ui", "ux"],
            "06_Analisa_Dan_Perancangan_Sistem": ["analisa", "perancangan"],
            "07_Sistem_Basis_Data": ["basis", "data"],
            "08_Praktikum_Basis_Data": ["praktikum", "basis data"],
        }

        # Source folder is now the "02_File_Berantakan" folder
        source_folder = os.path.join(self.base_folder, "02_File_Berantakan")
        if not os.path.exists(source_folder):
            error_msg = "02_File_Berantakan folder not found."
            self.add_log_entry(error_msg)
            messagebox.showwarning("Warning", error_msg)
            return

        files = os.listdir(source_folder)
        total_files = len(files)

        if total_files == 0:
            msg = "No files found in 02_File_Berantakan folder."
            self.add_log_entry(msg)
            messagebox.showinfo("Info", msg)
            return

        moved_files = 0
        file_moves = []  # Track individual file moves

        for i, file in enumerate(files):
            file_path = os.path.join(source_folder, file)
            if os.path.isfile(file_path):
                matched = False
                for folder, keywords in file_mappings.items():
                    if any(keyword.lower() in file.lower() for keyword in keywords):
                        destination_parent = (
                            "00_Tugas_dan_Joki" if "Tugas" in folder else "01_Materi"
                        )
                        destination = os.path.join(
                            self.base_folder,
                            destination_parent,
                            folder,
                        )
                        destination_path = os.path.join(destination, file)
                        shutil.move(file_path, destination_path)
                        file_moves.append(
                            f"Moved '{file}' to {destination_parent}/{folder}"
                        )
                        matched = True
                        break

                # If no match found, file stays in 02_File_Berantakan
                if matched:
                    moved_files += 1
                else:
                    file_moves.append(
                        f"No match for '{file}' - remained in 02_File_Berantakan"
                    )

                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing... {i+1}/{total_files} files")
                self.root.update()

        summary = f"Completed organization: {moved_files}/{total_files} files moved"
        self.add_log_entry(summary)

        # Add detailed file move information
        for move in file_moves:
            self.add_log_entry(move, indent=True)

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
            self.add_log_entry(error_msg)
            self.root.after(
                0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}")
            )
        finally:
            self.root.after(0, lambda: self.progress_bar.pack_forget())
            self.root.after(0, lambda: self.organize_button.config(state=tk.NORMAL))
            self.root.after(
                0, lambda: self.create_structure_button.config(state=tk.NORMAL)
            )

    def add_log_entry(self, message, indent=False):
        """Add an entry to the activity log with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = "    " if indent else ""
        self.log_entries.append(f"{timestamp}: {prefix}{message}")

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

                for entry in self.log_entries:
                    log_file.write(f"{entry}\n")

            self.add_log_entry(f"Log file saved to {log_path}")
            messagebox.showinfo("Success", f"Log saved to:\n{log_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save log: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
