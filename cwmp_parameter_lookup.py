import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog, messagebox

# Create a GUI application
root = Tk()
root.geometry('1080x720')  # Make the GUI resizable
root.title("TR181 Parameter Lookup")

# Create a menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create labels
file_label = Label(root, text="Load the definition file to start...")
param_label = Label(root, text="Parameter to lookup: ")
file_label.pack(anchor='w')
param_label.pack(anchor='w')

# Create entry and listbox widgets (initially disabled)
entry = Entry(root, state='disabled')
entry.pack(anchor='w', fill=X)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root, yscrollcommand=scrollbar.set, state='disabled')
listbox.pack(fill=BOTH, expand=1)

scrollbar.config(command=listbox.yview)

# Variable to store case-sensitive search state
case_sensitive = BooleanVar(value=False)  # Initially case-insensitive


# Function to open a file
def open_file():
    file_name = filedialog.askopenfilename(filetypes=[('XML Files', '*.xml')])
    if file_name:
        try:
            # Update the file label
            file_label.config(text="Model Definition File: " + file_name)

            # Load and parse the XML file with error handling
            tree = ET.parse(file_name)
            xml_root = tree.getroot()

            # Get all parameters
            parameters = []
            for obj in xml_root.findall('.//object'):
                object_name = obj.get('name')
                if object_name is None:
                    continue  # Skip objects without a name attribute

                has_param = False

                for param in obj.findall('.//parameter'):
                    parameter_name = param.get('name')
                    if parameter_name is None:
                        continue  # Skip parameters without a name attribute
                    else:
                        has_param = True
                        parameters.append(f'{object_name}{parameter_name}')

                if not has_param:
                    # Append object name alone if there were no parameters
                    parameters.append(object_name)

            # Enable widgets and populate the listbox
            entry.config(state='normal')
            listbox.config(state='normal')
            for parameter in parameters:
                listbox.insert(END, parameter)

            # Function to update the listbox
            def update_listbox(event):
                # Clear the listbox
                listbox.delete(0, END)

                if case_sensitive.get():
                    partial_string = entry.get()
                    for item in parameters:
                        if partial_string in item:
                            listbox.insert(END, item)
                else:
                    partial_string = entry.get().lower()
                    for item in parameters:
                        if partial_string in item.lower():
                            listbox.insert(END, item)

            # Bind the function to the entry widget
            entry.bind('<KeyRelease>', update_listbox)

        except FileNotFoundError:
            # Display an error message if the file is not found
            messagebox.showerror("Error", "File not found!")
        except ET.ParseError:
            # Display an error message if parsing fails
            messagebox.showerror("Error", "Invalid XML file!")
    else:
        pass


# Create a 'File' menu
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)

# Add 'Open' and 'Exit' commands to the 'File' menu
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Exit', command=root.quit)

# Create checkbox for case-sensitive search
case_sensitive_checkbox = Checkbutton(root, text="Case-Sensitive Search", variable=case_sensitive)
case_sensitive_checkbox.pack(anchor='w')  # Or any other desired position
# Start the GUI application
root.mainloop()
