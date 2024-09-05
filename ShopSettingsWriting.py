import os
import tkinter as tk
from tkinter import ttk
from lxml import etree

def is_folder_empty(folder_path):
    """Check if the given folder is empty (does not contain files or subfolders)."""
    with os.scandir(folder_path) as entries:
        return not any(entries)

def check_folder_and_subfolders(folder_path):
    """Check if a folder and all its subfolders are non-empty."""
    if is_folder_empty(folder_path):
        return False
    
    for entry in os.scandir(folder_path):
        if entry.is_dir():
            if not check_folder_and_subfolders(entry.path):
                return False
                
    return True

def list_non_empty_folders(directory_path, base_folder):
    """List non-empty folders and their subfolders."""
    non_empty_folders = []

    for root, dirs, files in os.walk(directory_path):
        if files or dirs:
            full_path = os.path.join(root)
            relative_path = os.path.relpath(full_path, start=directory_path)
            shortened_path = relative_path.split(base_folder, 1)[-1].lstrip(os.path.sep)

            if check_folder_and_subfolders(full_path):
                non_empty_folders.append(shortened_path)

    return non_empty_folders

def generate_ids_from_folder(folder_path):
    ids = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):  # Adjust the file extension as needed
            file_id = os.path.splitext(file_name)[0]  # Example: file_id is the file name without extension
            ids.append(file_id)
    print(f"Generated IDs for {folder_path}: {ids}")  # Debugging line
    return ids



def create_checklist_from_xml(file_path, prefix):
    """Parse XML file and return a list of item IDs with the specified prefix."""
    tree = etree.parse(file_path)
    root = tree.getroot()

    checklist = []

    for item in root.xpath('//item'):
        item_id = item.get('id')
        if item_id.startswith(prefix):
            checklist.append(item_id)

    return checklist

def add_builds_to_xml(file_path, ids, selected_items):
    """Add <build> elements to selected <item> elements in the XML file while preserving formatting and avoiding duplicates."""
    # Parse the existing XML file
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()
    
    # Define a custom pretty printer to preserve formatting
    def pretty_print(xml_element):
        xml_str = etree.tostring(xml_element, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
        return xml_str
    
    # Loop through the selected item IDs
    for item_id in selected_items:
        # Find the <item> element with the specified ID
        item_element = root.find(f".//item[@id='{item_id}']")
        
        if item_element is not None:
            # Collect existing build names in this <item>
            existing_build_names = set()
            for build_element in item_element.findall('build'):
                existing_build_names.add(build_element.get('name'))
            
            # Add <build> elements to the <item> element
            for build_id in ids:
                if build_id not in existing_build_names:
                    # Create a new <build> element with the name attribute set to the build_id
                    build_element = etree.Element("build", name=build_id)
                    item_element.append(build_element)
                    existing_build_names.add(build_id)  # Update the set with the new build name
    
    # Write the updated XML file with pretty printing to preserve formatting
    xml_str = pretty_print(root)
    with open(file_path, 'w', encoding='UTF-8') as f:
        f.write(xml_str)

def show_checklists_gui(folders, folder_paths, xml_checklist, xml_file_path):
    """Display a GUI with two separate sections for checklists and a run button."""
    root = tk.Tk()
    root.title("Checklists")

    # Frame for Folder Checkboxes
    frame_folders = ttk.Frame(root, padding="10")
    frame_folders.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    tk.Label(frame_folders, text="Folder Checklist").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    # Add folder checkboxes
    folder_vars = {}
    for i, folder in enumerate(folders):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(frame_folders, text=folder, variable=var)
        cb.grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
        folder_vars[folder] = var

    # Frame for XML Checkboxes
    frame_xml = ttk.Frame(root, padding="10")
    frame_xml.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
    tk.Label(frame_xml, text="XML Checklist").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

    # Add XML checkboxes
    xml_vars = {}
    for i, item in enumerate(xml_checklist):
        var = tk.BooleanVar()
        cb = tk.Checkbutton(frame_xml, text=item, variable=var)
        cb.grid(row=i+1, column=0, sticky=tk.W, padx=5, pady=2)
        xml_vars[item] = var

    # Run button
    btn_run = ttk.Button(root, text="Run", command=lambda: run_updates(folder_vars, xml_vars, folder_paths, xml_file_path))
    btn_run.grid(row=1, column=0, columnspan=2, pady=10)

    # Close button
    btn_close = ttk.Button(root, text="Close", command=root.destroy)
    btn_close.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

def update_ids_in_xml(file_path, ids, selected_items):
    """Update the XML file with new IDs, based on selected XML items."""
    # Parse the existing XML file
    tree = etree.parse(file_path)
    root = tree.getroot()
    
    # Remove existing <build> elements that match the selected items
    for item in selected_items:
        for build_element in root.xpath(f'//build[@name="{item}"]'):
            root.remove(build_element)
    
    # Add new <build> elements for the new IDs
    for id in ids:
        if not root.xpath('//item'):
            build_element = etree.Element("build", name=id)
            root.append(build_element)
    
    # Save the updated XML file
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

def run_updates(folder_vars, xml_vars, folder_paths, xml_file_path):
    """Run updates based on selected items in the GUI."""
    selected_folders = [folder for folder, var in folder_vars.items() if var.get()]
    selected_xml_items = [item for item, var in xml_vars.items() if var.get()]

    # Generate IDs from selected folders
    all_ids = []
    for folder in selected_folders:
        folder_path = folder_paths.get(folder)
        if folder_path:
            ids = generate_ids_from_folder(folder_path)
            all_ids.extend(ids)
    
    # Add <build> elements to selected <item> elements in the XML file
    add_builds_to_xml(xml_file_path, all_ids, selected_xml_items)


# Example usage:
if __name__ == "__main__":
    # Define folder path and base folder name
    folder_path = 'C:/PlayrixHS/temp/Expedition_Script/Exp19Circus'
    base_folder = 'Exp19Circus'
    
    # List non-empty folders
    folders = list_non_empty_folders(folder_path, base_folder)

    # Generate full paths for each folder and store in a dictionary
    folder_paths = {folder: os.path.join(folder_path, folder) for folder in folders}

    # Path to your XML file and prefix
    xml_file_path = 'ShopSettings.xml'
    prefix = 'Exp19Circus'


    # Generate checklist from XML
    xml_checklist = create_checklist_from_xml(xml_file_path, prefix)

    # Show GUI with both checklists
    show_checklists_gui(folders, folder_paths, xml_checklist, xml_file_path)