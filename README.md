# TR-181 Parameter Lookup Tool
This program provides a graphical user interface (GUI) to search for TR-181 parameters within a CWMP model definition file.

## Features
* Load a CWMP model definition file (download the latest file from: https://cwmp-data-models.broadband-forum.org/tr-181-2-17-0-cwmp-full.xml)
* Search for parameters by entering a partial string.
* Display matching parameters in a listbox.

## Requirements
* Python 3.x
* tkinter library (usually included by default in Python installations)

## Usage
1. Run the script: python tr181_parameter_lookup.py
2. Click **File -> Open** and select your XML model definition file.
3. Enter a partial parameter name in the search bar.
4. Matching parameters will be displayed in the listbox as you type.
5. Optionally, enable Case-sensitive Search checkbox


## Error Handling
The program displays error messages if the selected file cannot be found or if the XML parsing fails.