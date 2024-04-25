import xml.etree.ElementTree as ET
from tkinter import BooleanVar, Button, Checkbutton, Entry, Frame, Label, Listbox, Menu, Scrollbar, Tk
from tkinter import LEFT, RIGHT, MULTIPLE
from tkinter import filedialog, messagebox
from typing import List


def read_tr181_file(file_name: str) -> List[str]:
    """Retrieve all "parameter" elements under each "object" element within the "model" element
    Generate a List of "object-name"."parameter-name" strings in the model"""
    try:
        # Load and parse the XML file
        tree = ET.parse(file_name)
        xml_root = tree.getroot()

        # Get all parameters
        parameters: List[str] = []
        for obj in xml_root.findall('.//object'):
            object_name: str = obj.get('name')
            if object_name is None:
                continue  # Skip objects without a name attribute

            for param in obj.findall('.//parameter'):
                parameter_name: str = param.get('name')
                if parameter_name is None:
                    continue  # Skip parameters without a name attribute
                parameters.append(f'{object_name}{parameter_name}')

            if not obj.findall('.//parameter'):  # Check if object has no parameters
                parameters.append(object_name)  # Append object name alone

        return parameters
    except ET.ParseError:
        # Handle XML parsing errors
        return []


def update_listbox(parameters: List[str], case_ref: BooleanVar, entry_ref: Entry, listbox_ref: Listbox) -> None:
    # Clear the listbox
    listbox_ref.delete(0, 'end')

    if case_ref.get():
        partial_string: str = entry_ref.get()
        for item in parameters:
            if partial_string in item:
                listbox_ref.insert('end', item)
    else:
        partial_string: str = entry_ref.get().lower()
        for item in parameters:
            if partial_string in item.lower():
                listbox_ref.insert('end', item)


def copy_to_clipboard(listbox_ref: Listbox) -> None:
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

            parameters: List[str] = read_tr181_file(file_name)

            # Enable widgets and populate the listbox
            entry.config(state='normal')
            listbox.config(state='normal')
            for parameter in parameters:
                listbox.insert('end', parameter)

            # Bind the function to the entry widget
            entry.bind('<KeyRelease>', lambda event: update_listbox(parameters, case_sensitive, entry, listbox))

        except FileNotFoundError:
            # Display an error message if the file is not found
            messagebox.showerror("Error", "File not found!")
        except ET.ParseError:
            # Display an error message if parsing fails
            messagebox.showerror("Error", "Invalid XML file!")
    else:
        pass


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
    case_sensitive_checkbox: Checkbutton = Checkbutton(root, text="Case-Sensitive Search", variable=case_sensitive)
    case_sensitive_checkbox.pack(anchor='w', side=LEFT)
    # Button to clear selection and restart
    listbox_clear = Button(root, text="Clear selection", command=lambda: listbox.selection_clear(0, 'end'))
    listbox_clear.pack(side=RIGHT)

    # Start the GUI application
    root.mainloop()
