# Folder Organizer

This project is a simple Python GUI application designed to help organize files in a folder based on their extensions. The application allows users to scan a folder (and optionally its subfolders) and move files into destination folders based on the file type.

## Features

- **Folder Selection**: Easily select a folder to organize.
- **Include Subfolders**: Optionally include files from subdirectories during the scan.
- **Automatic Detection**: Detects file extensions present in the selected folder.
- **Custom Folder Assignments**: Assign destination folders for each file type.
- **File Moving**: Moves files into the specified folders based on their extension.
- **Logging**: A log file (`log.txt`) is generated to document file moves and any errors.

## Installation Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KMopsy/FolderOrganizer.git
   cd FolderOrganizer
2. **Set up a Python virtual environment (optional but recommended):**
	```bash
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install the dependencies:**
	```bash
	pip install customtkinter
	```

## How to Run the Project
**Run the application:**
```bash
python main.py
```

**Select a folder:**
Click on "Select Folder" to choose a folder.
(Optional) Check "Include subfolders" to include files from subdirectories.

**Scan the folder:**
Click "Start" to scan the selected folder for files based on their extensions.

**Move files:**
A new window will display all detected file extensions. Assign destination folders for each extension.
Click "Move Files" to move the files to the respective folders.

**Check logs:**
A log.txt file will be created in the selected folder, documenting file movements and any errors encountered during the process.

## Example Usage
You select a folder that contains .txt, .jpg, and .pdf files.
The application scans the folder and lists these file types.
You specify that .txt files should be moved to a "TextFiles" folder, .jpg files to an "Images" folder, and so on.
Once you click "Move Files," the files are organized into their designated folders.

## Purpose
This project was developed as a personal project. I’m happy to share it with others who may find it useful or inspiring. Feel free to explore and adapt the code for your own projects.

## License
This project is shared for inspiration and educational purposes. You are welcome to use and modify the code, but please note that it comes with no warranties or guarantees. I am not responsible for any issues or damages that may arise from its use.
