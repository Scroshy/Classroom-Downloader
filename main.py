import os
from tkinter import filedialog
import tkinter as tk
import auth
import classroom_manager
import downloader

def main():
    print("--- Google Classroom Downloader ---")
    
    # 1. Authenticate
    print("Authenticating...")
    cl_service, dr_service = auth.get_services()
    
    # 2. Get Courses
    print("Fetching courses...")
    courses = classroom_manager.list_courses(cl_service)
    
    if not courses:
        print("No courses found.")
        return

    # 3. User Selection
    print("\nAvailable Courses:")
    for i, course in enumerate(courses):
        print(f"{i + 1}. {course['name']}")

    try:
        choice = int(input("\nEnter course number: ")) - 1
        selected_course = courses[choice]
        print(f"\nSelected: {selected_course['name']}")
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # 4. Scan for Files
    files = classroom_manager.get_files_from_course(cl_service, selected_course['id'])
    print(f"\nFound {len(files)} files.")

    if len(files) == 0:
        return

    # 5. Download
    folder_name = downloader.sanitize_filename(selected_course['name'])
# --- FIX STARTS HERE ---
    print("Opening folder dialog...")
    root = tk.Tk()
    root.withdraw()  # Hide the main blank window
    root.attributes('-topmost', True)  # Force the dialog to appear on top of other windows
    
    folder_destination = filedialog.askdirectory(title="Select destination directory")
    
    root.destroy()   # Clean up the window instance
    # --- FIX ENDS HERE ---

    # Check if user cancelled
    if not folder_destination:
        print("Download cancelled by user.")
        return

    folder_path = os.path.join(folder_destination, folder_name)
    print("download")
    downloader.download_files(dr_service, files, folder_path)

    print("\nAll operations completed successfully!")

if __name__ == "__main__":
    main()