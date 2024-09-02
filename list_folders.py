import os 
ACCESS_TOKEN = os.getenv("DROPBOX_API_KEY")
import dropbox

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)



# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def list_all_folders(path):
    """Recursively list all folders in the given Dropbox path."""
    try:
        response = dbx.files_list_folder(path)
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                print(f"Folder found: {entry.path_lower}")
                list_all_folders(entry.path_lower)
    except dropbox.exceptions.ApiError as e:
        print(f"Failed to list folders in {path}: {e}")

def main():
    # Starting path (can be adjusted)
    start_path = "/current"
    list_all_folders(start_path)
     # Open file to write folder paths
    with open("folders_list.txt", "w") as file_handle:
        list_all_folders(start_path)
    print("Folder list saved to folders_list.txt")
if __name__ == "__main__":
    main()