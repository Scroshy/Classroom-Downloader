# Google Classroom Downloader

A Python automation tool that connects to your Google Classroom, scans for files (Assignments, Materials, and Announcements), and downloads them locally. It automatically converts Google Docs/Slides/Sheets into PDFs for offline viewing.

## Features

* **Authentication:** Secure OAuth 2.0 login via Google.
* **Course Selection:** Lists all active courses and lets you choose which one to download from.
* **Smart Scanning:** Checks Assignments, Class Materials, and the Stream (Announcements) for files.
* **Auto-Conversion:** Automatically detects "native" Google files (Docs, Sheets, Slides) and exports them as PDFs.
* **Sanitization:** Cleans up filenames to ensure they save correctly on Windows.

## Project Structure

This project is modularized into four main components:

* `main.py`: The entry point. Controls the flow of the application.
* `auth.py`: Handles Google OAuth login and token management.
* `classroom_manager.py`: Interacts with the Google Classroom API to fetch courses and file links.
* `downloader.py`: Interacts with the Google Drive API to download files and handle PDF conversion.

## Prerequisites

Before running the script, you need to set up a Google Cloud Project.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Enable the **Google Classroom API** and **Google Drive API**.
4.  Go to "Credentials" -> "Create Credentials" -> "OAuth Client ID" (Desktop App).
5.  Download the JSON file, rename it to `credentials.json`, and place it in this project folder.
6.  Add your email to the **Test Users** list in the "OAuth Consent Screen" settings.

## Installation

1.  **Clone or Download** this repository.
2.  **Install Dependencies:**
    Open your terminal/command prompt in the project folder and run:
    ```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

## Usage

1.  Ensure `credentials.json` is in the same folder as the scripts.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  **First Run:** A browser window will open asking you to log in. Grant the necessary permissions.
4.  **Select a Course:** Enter the number corresponding to the course you want to download.
5.  **Wait:** The script will create a folder named after the course and download all found files into it.

## Troubleshooting

* **"Access Blocked" Error:** Make sure you added your email address to the "Test Users" section in the Google Cloud Console.
* **"Found 0 Files":** Ensure you are checking the "Stream" or "Classwork" tabs on the website to verify files actually exist. Some teachers use links (URLs) instead of files; this script currently only downloads files stored in Drive.
* **Token Errors:** If you change permissions or scopes, delete the `token.json` file and run the script again to re-authenticate.