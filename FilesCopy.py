import os
import shutil

def copy_files(src, dst):
    for root, dirs, files in os.walk(src):
        # Create corresponding destination subfolder path
        relative_path = os.path.relpath(root, src)
        dst_folder = os.path.join(dst, relative_path)
        
        # Create subfolder if it doesn't exist
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        # Copy files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_folder, file)
            shutil.copy2(src_file, dst_file)  # copy2 preserves metadata

src_folder = r'C:\PlayrixHS\temp\Expedition_Script\Exp19Circus'
dst_folder = r'C:\PlayrixHS\homescapes\base_mm\textures\Gamefield\static\Exp19Circus'

copy_files(src_folder, dst_folder)

print("Files copied successfully.")





    #first_directory = 'C:\PlayrixHS\temp\Expedition_Script\Exp19Circus'
    #second_directory = 'C:\PlayrixHS\homescapes\base_mm\textures\Gamefield\static\Exp19Circus'

