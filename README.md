# TR-181 Parameter Lookup Tool
This program provides a graphical user interface (GUI) to search for TR-181 parameters within a CWMP model definition file.

## Features
* Parse CWMP model definition file (download the latest file from: https://cwmp-data-models.broadband-forum.org/tr-181-2-17-0-cwmp-full.xml)
* Search for parameters by entering a partial string.
* Select & copy one or more matching parameters from the listbox.

## Requirements
* Python 3.x
* **tkinter** library (usually included by default in Python installations)

## Usage
1. Run the script: python tr181_parameter_lookup.py
2. Click **File -> Open** and select your XML model definition file.
3. Start typing parameter name in the search box, to populate matching parameters in the listbox
4. Optionally, enable **Case-sensitive Search** checkbox at left bottom 
5. Multiple items in the listbox can be selected and copied to clipboard. 
6. Selection of items can be cleared by the **Clear listbox selections** button


## Error Handling
The program displays error messages if the selected file cannot be found or if the XML parsing fails.