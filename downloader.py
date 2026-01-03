import os
import io
from googleapiclient.http import MediaIoBaseDownload

# Map Google types to the format we want to convert them to (PDF)
EXPORT_MIMES = {
    'application/vnd.google-apps.document': 'application/pdf',
    'application/vnd.google-apps.spreadsheet': 'application/pdf',
    'application/vnd.google-apps.presentation': 'application/pdf'
}

def sanitize_filename(name):
    """Removes characters that are illegal in Windows filenames."""
    return "".join([c for c in name if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '-')]).rstrip()

def download_files(drive_service, files_list, folder_name):
    """Iterates through file list and downloads them."""
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    print(f"\nStarting download to folder: {folder_name}/")

    for file_info in files_list:
        file_id = file_info['id']
        original_title = file_info['title']
        safe_name = sanitize_filename(original_title)
        
        try:
            # Check file type
            meta = drive_service.files().get(fileId=file_id, fields='mimeType').execute()
            mime_type = meta.get('mimeType')
            
            request = None
            final_filename = safe_name

            # LOGIC: Convert Google Docs to PDF, download others directly
            if mime_type in EXPORT_MIMES:
                request = drive_service.files().export_media(
                    fileId=file_id, 
                    mimeType=EXPORT_MIMES[mime_type]
                )
                if not final_filename.lower().endswith('.pdf'):
                    final_filename += '.pdf'
                print(f" [PDF Convert] {safe_name}")
            else:
                request = drive_service.files().get_media(fileId=file_id)
                print(f" [Download]    {safe_name}")

            # Check if exists
            file_path = os.path.join(folder_name, final_filename)
            if os.path.exists(file_path):
                continue

            # Execute Download
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            with open(file_path, "wb") as f:
                f.write(fh.getbuffer())

        except Exception as e:
            print(f"   [Error] Skipped '{safe_name}': {e}")