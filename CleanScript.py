import os

def clean_folder(folder_path):
    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    # Specify the folder path here
    folder_to_clean = r"C:\PlayrixHS\temp\Expedition_Script\Exp19Circus"

    if os.path.exists(folder_to_clean):
        clean_folder(folder_to_clean)
        print("Folder cleaned successfully.")
    else:
        print("The specified folder does not exist.")
