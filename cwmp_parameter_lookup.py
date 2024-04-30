import xml.etree.ElementTree as ET
from tkinter import BooleanVar, IntVar
from tkinter import Button, Checkbutton, Entry, Frame, Label, Listbox, Menu, Scrollbar, Radiobutton
from tkinter import Tk, Text, Toplevel
from tkinter import LEFT, RIGHT, RAISED, MULTIPLE, INSERT
from tkinter import filedialog, messagebox
from typing import List, Tuple


def read_tr181_file(file_name: str) -> List[Tuple[str, str]]:
    """Retrieve all "parameter" elements under each "object" element within the "model" element
    Generate a List of "object-name"."parameter-name" strings in the model"""
    try:
        # Load and parse the XML file
        tree = ET.parse(file_name)
        xml_root = tree.getroot()

        # debug_access = []

        # Get all parameters
        parameters: List[Tuple[str, str]] = []
        for obj in xml_root.findall('.//object'):
            object_name: str = obj.get('name')
            if object_name is None:
                continue  # Skip objects without a name attribute

            for param in obj.findall('.//parameter'):
                parameter_name: str = param.get('name')
                if parameter_name is None:
                    continue  # Skip parameters without a name attribute

                access_type: str = param.get('access')  # readOnly, readWrite,  writeOnceReadOnly
                if access_type is None:
                    parameters.append((f'{object_name}{parameter_name}', f'any'))
                else:
                    parameters.append((f'{object_name}{parameter_name}', access_type))
                    # if access_type not in debug_access:
                    #     debug_access.append(access_type)

            if not obj.findall('.//parameter'):  # Check if object has no parameters
                parameters.append((object_name, f'any'))  # Append object name alone

        # for item in debug_access:
        #     print(item)

        return parameters
    except ET.ParseError:
        # Handle XML parsing errors
        return []


def update_listbox(parameters: List[Tuple[str, str]], case_ref: BooleanVar, access_ref: IntVar,
                   entry_ref: Entry, listbox_ref: Listbox) -> None:
    # Clear the listbox
    listbox_ref.delete(0, 'end')

    my_case = case_ref.get()
    my_access = access_ref.get()
    partial_string: str = entry_ref.get()

    # print("My Access: ", my_access)

    for item in parameters:
        # Check parameters read/write permissions against the filter
        if my_access == 1 and item[1] != "readOnly":
            continue  # Skip all items that are *not* read only, when I want to see read-only parameters

        if my_access == 2 and item[1] == "readOnly":
            continue  # Skip all items that are read only items, when I want to see read-write items

        target_string = item[0]
        if my_case == 0:
            partial_string = partial_string.lower()
            target_string = target_string.lower()

        if partial_string in target_string:
            listbox_ref.insert('end', item[0])


def copy_to_clipboard(listbox_ref: Listbox) -> None:
    """Copy selected listbox elements to the clipboard"""
    root.clipboard_clear()
    selected = listbox_ref.curselection()
    if selected:
        for i in selected:
            root.clipboard_append(listbox_ref.get(i) + '\n')


def click_on_file_open() -> None:
    """Select a TR-181 Data Model File"""
    file_name: str = filedialog.askopenfilename(filetypes=[('XML Files', '*.xml')])
    if file_name:
        try:
            # Update the file label
            file_label.config(text="Model Definition File: " + file_name)

            parameters: List[(str, str)] = read_tr181_file(file_name)

            # Enable widgets and populate the listbox
            entry.config(state='normal')
            listbox.config(state='normal')
            for parameter in parameters:
                listbox.insert('end', parameter[0])

            # Bind the function to the entry widget
            entry.bind('<KeyRelease>', lambda event: update_listbox(parameters, case_sensitive, param_access_type,
                                                                    entry, listbox))
            # Set focus on the entry box
            entry.focus_set()

        except FileNotFoundError:
            # Display an error message if the file is not found
            messagebox.showerror("Error", "File not found!")
        except ET.ParseError:
            # Display an error message if parsing fails
            messagebox.showerror("Error", "Invalid XML file!")
    else:
        pass


def generate_key_release_event(entry_ref: Entry) -> None:
    """Generate a Key Release Event for UI action"""
    entry_ref.event_generate('<KeyRelease>')


# Add an "About" menu item to the "Help" menu
def show_about_dialog():
    about_dialog = Toplevel(root)
    about_dialog.title("About")
    about_dialog.geometry("400x200")

    text_widget = Text(about_dialog, width=40, height=10, font=("Helvetica", 10))
    text_widget.pack(padx=20, pady=20)

    about_text = """TR-181 Parameter lookup
Version 1.1

Copyright 2024 - Hari Turlapati

Permission is hereby granted, free of charge, to use, copy, modify, and distribute this software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""

    text_widget.insert(INSERT, about_text)
    text_widget.config(state='disabled')  # make the text read-only


if __name__ == '__main__':
    # Create a GUI application
    root: Tk = Tk()
    root.geometry('1080x720')
    root.title("TR181 Parameter Lookup")
    root.resizable(True, True)  # Make the GUI resizable

    # Create a menu bar
    menubar: Menu = Menu(root)
    root.config(menu=menubar)

    # Create a 'File' menu
    file_menu: Menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file_menu)

    # Add 'Open' and 'Exit' commands to the 'File' menu
    file_menu.add_command(label='Open', command=click_on_file_open)
    file_menu.add_command(label='Exit', command=root.quit)

    # Create a "Help" menu
    help_menu: Menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=show_about_dialog)

    # Create labels
    file_label: Label = Label(root, text="Load the definition file to start...", anchor='w')
    param_label: Label = Label(root, text="Parameter to lookup: ", anchor='w')
    file_label.pack(fill='x')
    param_label.pack(fill='x')

    # Create entry widgets with clear button
    entry_frame: Frame = Frame(root)
    entry_frame.pack(anchor='w', fill='x')
    entry: Entry = Entry(entry_frame, state='disabled')
    entry.pack(anchor='w', side=LEFT, fill='both', expand=1)
    # Button to clear selection and restart
    entry_clear = Button(entry_frame, text="x",
                         command=lambda: [entry.delete(0, 'end'), entry.event_generate('<KeyRelease>')])
    entry_clear.pack(side=RIGHT)

    # Create listbox  (initially disabled)
    listbox_frame: Frame = Frame(root)
    listbox_frame.pack(anchor='w', fill='both', expand=1)
    scrollbar: Scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side='right', fill='y')
    listbox: Listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set, state='disabled', selectmode=MULTIPLE)
    listbox.pack(fill='both', expand=1)
    scrollbar.config(command=listbox.yview)

    # Define a clippy!!
    listbox.bind('<Button-3>', lambda e: popup_menu.tk_popup(e.x_root, e.y_root))
    popup_menu = Menu(root, tearoff=0)
    popup_menu.add_command(label='Copy', command=lambda: copy_to_clipboard(listbox))

    # Variable to store case-sensitive search state
    case_sensitive: BooleanVar = BooleanVar(value=False)  # Initially case-insensitive

    # Create checkbox for case-sensitive search
    case_sensitive_checkbox: Checkbutton = Checkbutton(root, text="Case sensitive",
                                                       variable=case_sensitive,
                                                       command=lambda: generate_key_release_event(entry),
                                                       borderwidth=1,
                                                       relief=RAISED)
    case_sensitive_checkbox.pack(anchor='w', side=LEFT)

    # Radio button to filter RO/RW parameters
    # Create a frame to hold the radio buttons
    rb_frame: Frame = Frame(root, borderwidth=1, relief=RAISED)
    rb_frame.pack(anchor='w', side=LEFT)
    # Create the radio buttons
    param_access_type: IntVar = IntVar()
    param_access_type.set(0)  # default value

    description_label: Label = Label(rb_frame, text="  Access:")
    description_label.pack(side=LEFT)

    r1: Radiobutton = Radiobutton(rb_frame, text="Any", variable=param_access_type, value=0,
                                  command=lambda: generate_key_release_event(entry))
    r1.pack(side=LEFT)

    r2: Radiobutton = Radiobutton(rb_frame, text="RO", variable=param_access_type, value=1,
                                  command=lambda: generate_key_release_event(entry))
    r2.pack(side=LEFT)

    r3: Radiobutton = Radiobutton(rb_frame, text="RW", variable=param_access_type, value=2,
                                  command=lambda: generate_key_release_event(entry))
    r3.pack(side=LEFT)

    # Button to clear selection and restart
    listbox_clear = Button(root, text="Clear listbox selection",
                           command=lambda: listbox.selection_clear(0, 'end'))
    listbox_clear.pack(side=RIGHT)

    # Start the GUI application
    root.mainloop()
