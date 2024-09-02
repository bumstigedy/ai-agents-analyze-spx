import os 
ACCESS_TOKEN = os.getenv("DROPBOX_API_KEY")
import dropbox

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def download_files_from_folder(folder_path):
    """Download all files from the specified Dropbox folder."""
    try:
        # List all files in the folder
        response = dbx.files_list_folder(folder_path)
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_path = entry.path_lower
                file_name = entry.name
                print(file_path,file_name)
                # Download the file
                download_path = f"./{file_name}"  # Download to current directory
                with open(download_path, "wb") as f:
                    metadata, res = dbx.files_download(file_path)
                    f.write(res.content)
                print(f"Downloaded {file_name} to {download_path}")
    except dropbox.exceptions.ApiError as e:
        print(f"Failed to download files from {folder_path}: {e}")

def main():
    # Set the folder path as a variable
    folder_path = "/current/2024/august/aug 12/goldman/s&t"
    
    download_files_from_folder(folder_path)

if __name__ == "__main__":
    main()
