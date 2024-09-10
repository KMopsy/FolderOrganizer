"""
    FolderOrganizer to organize and move files by their extensions
    Libraries used: python, tkinter, customtkinter, os, pathlib, threading
"""

import threading
from tkinter import filedialog
import customtkinter as ctk
import os
import pathlib

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")


class App:
    # Initialize the application and set up variables
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x350")
        self.master.title("Folder Organizer")
        self.folder_path = None
        self.ExtWin = None
        self.ext = []
        self.files = []
        self.dest = []

        self.scansub_checkbox = ctk.BooleanVar(value=False)

        self.create_widgets()

    # Set up the basic GUI layout and widgets
    def create_widgets(self):
        self.info_label = ctk.CTkLabel(self.master, text="Select a folder to proceed", font=("Arial", 14))
        self.info_label.pack(pady=20)

        self.folder_label = ctk.CTkLabel(self.master, text="No folder selected", font=("Arial", 12))
        self.folder_label.pack(pady=10)

        self.subfolder_checkbox = ctk.CTkCheckBox(self.master, text="Include subfolders",
                                                  variable=self.scansub_checkbox)
        self.subfolder_checkbox.pack(pady=10)

        self.select_folder_button = ctk.CTkButton(self.master, text="Select Folder", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.master, text="Status: Waiting for folder selection", font=("Arial", 12))
        self.status_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self.master, text="Start", command=self.start_scan, state=ctk.DISABLED)
        self.start_button.pack(pady=10)

    # Function triggered by the "Select Folder" button to open a folder dialog
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if not self.folder_path:
            self.status_label.configure(text="Status: No folder selected")
        else:
            self.folder_label.configure(text=f"Selected folder: {self.folder_path}")
            self.status_label.configure(text="Status: Folder selected successfully")
            self.start_button.configure(state=ctk.NORMAL)
            self.log_status("INFO", "Folder selected successfully")

    # Function to scan the selected folder and read its contents
    def start_scan(self):
        if self.folder_path:
            self.select_folder_button.configure(state=ctk.DISABLED)
            files = os.listdir(self.folder_path)
            if self.scansub_checkbox.get():
                for path, subdirs, files in os.walk(self.folder_path):
                    for name in files:
                        if pathlib.Path(name).suffix not in self.ext:
                            self.ext.append(pathlib.Path(name).suffix)
                            self.files.append(os.path.join(path, name))
            else:
                for file in files:
                    path = os.path.join(self.folder_path, file)
                    if os.path.isfile(path):
                        if pathlib.Path(file).suffix not in self.ext:
                            self.ext.append(pathlib.Path(file).suffix)
                            self.files.append(path)

            self.status_label.configure(text="Status: Scan completed.\nAwaiting user input.")
            self.log_status("INFO", "Scan completed. Awaiting user input.")
            self.showExt()

    # Function to display file extensions and input fields for destination folders
    def showExt(self):
        self.ExtWin = ctk.CTkToplevel()
        self.ExtWin.title("Move Files")

        if self.ExtWin is not None and self.ExtWin.winfo_exists():
            self.ExtWin.lift()

        self.ExtWin.geometry(f"+{self.master.winfo_x() + self.master.winfo_width() + 10}+{self.master.winfo_y()}")

        for i, ext in enumerate(self.ext):
            label = ctk.CTkLabel(self.ExtWin, text=ext, height=30)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            textbox = ctk.CTkTextbox(self.ExtWin, height=30, width=200)
            textbox.grid(row=i, column=1, padx=10, pady=5, sticky="w")

            self.dest.append(textbox)

        start_button = ctk.CTkButton(self.ExtWin, command=self.prepare_move_files, text="Move Files")
        start_button.grid(row=len(self.ext), column=0, columnspan=2, pady=10)

        self.ExtWin.focus()

    # Prepare to move the files by creating a new thread
    def prepare_move_files(self):
        threading.Thread(target=self.move_files).start()

    # Move files to the selected destination folders
    def move_files(self):
        if self.dest:
            self.status_label.configure(text="Status: User input completed.\nMoving files...")
            self.log_status("INFO", "User input completed. Moving files.")
            for dest in self.dest:
                destg = dest.get("1.0", "end-1c").strip()
                if not destg:
                    self.log_status("ERROR", f"Destination {destg} is empty.")
                    continue
                path = os.path.join(self.folder_path, destg)
                if not os.path.exists(path):
                    try:
                        os.mkdir(path)
                        self.log_status("SUCCESS", f"Folder {path} created.")
                    except Exception as e:
                        self.log_status("ERROR", f"Error creating folder {path}")
            for file in self.files:
                if pathlib.Path(file).suffix in self.ext:
                    try:
                        os.rename(file, os.path.join(self.folder_path,
                                                     self.dest[self.ext.index(pathlib.Path(file).suffix)].get("1.0",
                                                                                                              "end-1c").strip(),
                                                     pathlib.Path(file).name))
                        self.log_status("SUCCESS", f"File {file} moved successfully.")
                    except FileNotFoundError:
                        self.log_status("ERROR", f"File {file} not found.")
                    except PermissionError:
                        self.log_status("ERROR", f"Access denied to {file}.")
                    except Exception as e:
                        self.log_status("ERROR", f"Unknown error occurred while moving {file}: {e}")

        self.start_button.configure(state=ctk.DISABLED)
        self.select_folder_button.configure(state=ctk.NORMAL)
        self.status_label.configure(text="Status: Files moved successfully!")
        self.log_status("SUCCESS", "Files moved successfully!")
        if self.ExtWin is not None and self.ExtWin.winfo_exists():
            self.ExtWin.destroy()
            self.ExtWin = None

    # Create a thread for the logging function
    def log_status(self, errorcode, text):
        threading.Thread(target=self.write_log, args=(errorcode, text)).start()

    # Write log entries to the log file
    def write_log(self, errorcode, text):
        if self.folder_path:
            log_path = os.path.join(self.folder_path, "log.txt")
            try:
                with open(log_path, "a") as log:
                    log.write(f"{errorcode} | {text}\n")
            except Exception as e:
                print(f"Error writing log: {e}")
        else:
            print("No valid folder path found.")


# Run the application
if __name__ == "__main__":
    app = ctk.CTk()
    fo_app = App(app)
    app.mainloop()
