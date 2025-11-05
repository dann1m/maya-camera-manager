# Camera Manager for Maya

A simple Python tool for managing cameras in Autodesk Maya.  
Easily create, delete, rename, lock/unlock, duplicate, export, and import cameras through a clean UI.


This tool was created as part of [Alexander Richter's Python for Maya course](https://alexanderrichtertd.com/).

---

## Features

- List all cameras in the scene
- Create new cameras
- Delete selected cameras with confirmation
- Rename selected cameras safely
- Lock/unlock camera transforms (translate, rotate, scale)
- Duplicate cameras
- Set a camera as the renderable camera
- Export/import cameras to/from `.ma` files
- Right-click menu with quick actions
- Shelf button for easy access

---

## Installation

1. **Download the files**  
   - Clone the GitHub repository or download the ZIP.

2. **Copy to your Maya scripts folder**  
   - Usually located at:  
     ```
     Documents/maya/scripts
     ```
   - Make sure the `img` folder with the icon is in the same folder as `camera_manager.py`.

3. **Add to shelf (optional)**  
   - Run the script in Maya:
     ```python
     import camera_manager
     camera_manager.add_shelf_button()
     ```
   - This will create a shelf button in the "Custom" shelf for one-click access.

---

## Usage

1. Run the Camera Manager UI in Maya:
   ```python
   import camera_manager
   camera_manager.cam_manager_ui()

2. Use the UI to manage cameras:

- Select a camera from the list.
- Use buttons for create, delete, rename, lock/unlock, export, import.
- Right-click a camera in the list for quick actions like:
  - "Set as Renderable"
  - "Duplicate Camera"
  - "Show Camera Info"

## Requirements

- Autodesk Maya (tested on 2022+)
- Python (built into Maya)
- PySide2 (comes with Maya)

## Notes

- Works with all camera types, including perspective and orthographic cameras.
- Always check the camera list after operations to see updates.
- Exported cameras are saved as `.ma` files and can be imported into other Maya scenes.

## License

You are free to use, modify, and share this tool.
