import os

def rename_png_files_in_subfolders(root_folder):
    # Get the name of the root folder
    root_folder_name = os.path.basename(root_folder.rstrip(os.sep))

    # Traverse all directories and subdirectories
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.png'):
                # Get the relative folder structure
                relative_path = os.path.relpath(dirpath, root_folder)
                path_parts = relative_path.split(os.sep)

                if len(path_parts) > 1:
                    # Combine root folder and next folder without separator
                    first_part = root_folder_name + path_parts[0]
                    # Use the last folder name as the last part of the new name
                    last_part = path_parts[-1]
                else:
                    # If there's no subfolder, just use the root folder name as first part
                    first_part = root_folder_name
                    last_part = root_folder_name  # In case the file is in the root folder

                # Build the new file name with the specified structure
                new_filename = f"{first_part}_{last_part}_{filename}"

                # Full original and new file paths
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_filename)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")

# Example usage:
root_folder = r"C:/PlayrixHS/temp/Expedition_Script/Exp19Circus"  # Set your root folder here
rename_png_files_in_subfolders(root_folder)
