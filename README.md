# File Organizer

A desktop application built with Python and Tkinter to help users organize their files into a structured folder system.

## Project Overview

File Organizer is a simple yet powerful tool designed to help students and professionals manage their academic and work files. The application creates a predefined folder structure and automatically sorts files based on keywords in their filenames. It's particularly useful for organizing course materials, assignments, and project files.

Key features:
- Create a structured folder hierarchy with a single click
- Automatically organize files based on filename keywords
- Track file movement with detailed activity logs
- User-friendly graphical interface
- Progress tracking for organization tasks

## Prerequisites

To run this application, you need:
- Python 3.6 or higher
- Tkinter (usually included with Python installations)
- Standard Python libraries: os, shutil, threading, datetime

## Installation

1. Clone this repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/file-organizer.git
   cd file-organizer
   ```

2. Ensure you have Python installed:
   ```bash
   python --version
   ```

3. Run the application:
   ```bash
   python organize.py
   ```

## Usage

### Step 1: Select a Base Folder
Click the "Browse" button to select the directory where you want to create your organized folder structure.

### Step 2: Create Folder Structure
Click "Create Folder Structure" to generate the following hierarchy:
```
Base Folder/
├── 00_Tugas_dan_Joki/
│   ├── 00_Jokian/
│   ├── 01_Tugas_Transformasi_Digital/
│   ├── 02_Tugas_Kecakapan_Antarpersonal/
│   ├── 03_Tugas_Pemrograman/
│   ├── 04_Tugas_Manajemen_Proyek/
│   ├── 05_Tugas_Design_Interface_User/
│   ├── 06_Tugas_Analisa_Dan_Perancangan_Sistem/
│   ├── 07_Tugas_Sistem_Basis_Data/
│   └── 08_Tugas_Praktikum_Basis_Data/
├── 01_Materi/
│   ├── 01_Transformasi_Digital/
│   ├── 02_Kecakapan_Antarpersonal/
│   ├── 03_Pemrograman/
│   ├── 04_Manajemen_Proyek/
│   ├── 05_Design_Interface_User/
│   ├── 06_Analisa_Dan_Perancangan_Sistem/
│   ├── 07_Sistem_Basis_Data/
│   └── 08_Praktikum_Basis_Data/
└── 02_File_Berantakan/
```

### Step 3: Organize Files
1. Place your disorganized files in the "02_File_Berantakan" folder
2. Click "Organize Files From 02_File_Berantakan"
3. The application will automatically sort files based on keywords in their filenames
4. View the progress bar for real-time status updates

### Step 4: Save Activity Log
After organization is complete, click "Save Activity Log" to generate a detailed report of all file movements.

## How File Organization Works

Files are automatically sorted based on keywords in their filenames:

| Destination Folder | Keywords |
|--------------------|----------|
| 00_Jokian | joki, order |
| 01_Tugas_Transformasi_Digital | tugastransformasi, tugasdigital |
| 02_Tugas_Kecakapan_Antarpersonal | tugaskecakapan, tugasantarpersonal |
| ... | ... |
| 03_Pemrograman | pemrograman, coding |
| ... | ... |

Files that don't match any keywords remain in the "02_File_Berantakan" folder.

## Contributing

Contributions to improve File Organizer are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Ideas
- Add support for custom folder structures
- Implement file organization by date or type
- Create a dark mode for the interface
- Add support for multiple languages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created to help students organize their academic files
- Inspiration from various file management systems

---

Created with ❤️ by [Argy Anggara / Kodein.dulu]
