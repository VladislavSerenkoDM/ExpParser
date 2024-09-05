import os
from lxml import etree

def update_xml_with_sprite(xml_file, basePath, sprite_id, sprite_path):
    # Parse the XML file
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_file, parser)
    root = tree.getroot()

    # Flags to determine if the sprite was added and if basePaths were found
    sprite_added = False
    basePath_found = False
    basePath_one_folder_up_found = False

    # Check if the sprite already exists in the XML
    for sprites in root.findall('Sprites'):
        if sprites.get('basePath') == basePath:
            basePath_found = True
            
            # Check for existing sprite with the same id and path
            existing_sprites = sprites.findall('sprite')
            for sprite in existing_sprites:
                if sprite.get('id') == sprite_id and sprite.get('path') == sprite_path:
                    print(f"Sprite with id '{sprite_id}' and path '{sprite_path}' already exists. Skipping.")
                    return  # Exit if duplicate is found

            # Create the new <sprite> element
            new_sprite = etree.Element('sprite', id=sprite_id, path=sprite_path)
            # Append the new sprite to the <Sprites> element
            sprites.append(new_sprite)
            sprite_added = True
            break

    if not basePath_found:
        # Look for the basePath one folder level up
        basePath_one_folder_up = os.path.dirname(basePath)
        print(f"Checking for basePath one folder up: '{basePath_one_folder_up}'")
        for sprites in root.findall('Sprites'):
            if sprites.get('basePath') == basePath_one_folder_up:
                basePath_one_folder_up_found = True
                
                # Check for existing sprite with the same id and path
                existing_sprites = sprites.findall('sprite')
                for sprite in existing_sprites:
                    if sprite.get('id') == sprite_id and sprite.get('path') == sprite_path:
                        print(f"Sprite with id '{sprite_id}' and path '{sprite_path}' already exists. Skipping.")
                        return  # Exit if duplicate is found

                # Create the new <sprite> element
                new_sprite = etree.Element('sprite', id=sprite_id, path=sprite_path)
                # Append the new sprite to the <Sprites> element
                sprites.append(new_sprite)
                sprite_added = True
                break

    if not basePath_found and not basePath_one_folder_up_found:
        print(f"No <Sprites> element with basePath '{basePath}' or one folder up found in XML file.")

    # Write the updated XML back to the file with pretty formatting if any sprite was added
    if sprite_added:
        with open(xml_file, 'wb') as f:
            tree.write(f, pretty_print=True, encoding='utf-8', xml_declaration=True)

def process_png_files(root_folder, xml_file):
    root_folder_name = os.path.basename(root_folder)
    root_folder_parts = root_folder.split(os.sep)
    root_folder_name_with_subfolder = root_folder_parts[-2] if len(root_folder_parts) > 1 else root_folder_name
    prepend_path = "textures/Gamefield/static"
    
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.png'):
                # Compute relative path and exclude the PNG filename
                relative_path = os.path.relpath(subdir, root_folder)
                basePath = os.path.join(prepend_path, root_folder_name_with_subfolder, relative_path)
                basePath = basePath.replace(os.sep, '/')
                print(basePath)
                # Create the id and path variables
                file_name_without_ext = os.path.splitext(file)[0]
                sprite_id = f"cl_{root_folder_name}_{file_name_without_ext}"
                sprite_path = f"{root_folder_name}_{file_name_without_ext}"
                
                # Call the function to update the XML
                update_xml_with_sprite(xml_file, basePath, sprite_id, sprite_path)

# Set the root folder and XML file
root_folder = 'C:/PlayrixHS/temp/Expedition_Script/Exp19Circus'
xml_file = 'Resources.xml'  # Replace with the path to your XML file
process_png_files(root_folder, xml_file)
