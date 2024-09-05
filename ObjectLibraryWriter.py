import os
from lxml import etree
from lxml.etree import Element, SubElement, tostring, parse
import tkinter as tk
from tkinter import messagebox

def add_items_to_xml(existing_xml_file, root_dir, z_order):
    # Parse the existing XML file
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(existing_xml_file, parser)
    root = tree.getroot()

    # Find all existing <item> ids in the XML
    existing_item_ids = set()
    for item_elem in root.findall(".//item"):
        existing_item_ids.add(item_elem.get('id'))

    # Find the correct <Objects> element based on user's choice of z_order
    objects_elem = root.find(f'.//Objects[@defaultZOrder="{z_order}"]')
    if objects_elem is None:
        messagebox.showerror("Error", f"No <Objects> element found with defaultZOrder='{z_order}'")
        return

    # Traverse directories and files
    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            # Skip files without an image extension
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                continue

            # Check if an <item> with this filename already exists
            if filename in existing_item_ids:
                print(f"Item with id '{filename}' already exists. Skipping...")
                continue

            # Create <item> element
            item_elem = Element('item', id=filename)

            # Create <layer> element with the specified attributes
            layer_elem = SubElement(item_elem, 'layer', 
                                    type="texture", 
                                    name="texture", 
                                    texture="cl_" + filename, 
                                    xOffset="-130", 
                                    yOffset="-50", 
                                    xMin="-60", 
                                    yMin="-70", 
                                    zMin="0", 
                                    xMax="60", 
                                    yMax="15", 
                                    zMax="300")

            # Add the new <item> element to the selected <Objects> element
            objects_elem.append(item_elem)

    # Write the updated XML to the file with preserved formatting
    with open(existing_xml_file, 'wb') as f:
        f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

def choose_z_order():
    # Function to handle the z-order selection and trigger the XML update
    def on_submit():
        selected_z_order = z_order_var.get()
        if selected_z_order:
            # Close the window
            window.destroy()
            # Run the XML update with the selected z-order
            add_items_to_xml(existing_xml_file, root_directory, selected_z_order)
        else:
            messagebox.showwarning("Selection Required", "Please choose where to add new elements.")

    # Tkinter setup
    window = tk.Tk()
    window.title("Choose Parent Objects")

    tk.Label(window, text="Where would you like to add new elements?").pack(pady=10)

    z_order_var = tk.StringVar()

    # Radio buttons for user selection
    tk.Radiobutton(window, text="Parent <Objects> with defaultZOrder='0'", variable=z_order_var, value="0").pack(anchor=tk.W)
    tk.Radiobutton(window, text="Parent <Objects> with defaultZOrder='-1000'", variable=z_order_var, value="-1000").pack(anchor=tk.W)

    # Submit button
    submit_button = tk.Button(window, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    window.mainloop()

# Set paths
existing_xml_file = 'ObjectLibrary.xml'
root_directory = 'C:/PlayrixHS/temp/Expedition_Script/Exp19Circus'

# Launch the popup window for z-order selection
choose_z_order()
