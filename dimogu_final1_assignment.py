# Camera Manager Tool for Maya
# Author: Danielle Imogu
# Date: 08.24.2025
# Description: Simple UI to create, delete, rename, lock, export, import, and manage cameras in Maya.

import os
import maya.cmds as cmds

IMG_PATH = os.path.join(os.path.dirname(__file__), "img")

# -------------------------
# Helper Functions
# -------------------------
def list_cameras():
    cameras = cmds.ls(type="camera")
    cmds.textScrollList("cameraList", edit=True, removeAll=True)
    cameras = [cmds.listRelatives(c, parent=True)[0] for c in cameras]
    for cam in cameras:
        cmds.textScrollList("cameraList", edit=True, append=cam)

def create_camera(*args):
    cmds.camera()
    list_cameras()

def delete_camera(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if selected:
        confirm = cmds.confirmDialog(
            title="Delete Camera?",
            message=f"Are you sure you want to delete camera: {selected[0]}?",
            button=["Yes", "No"],
            defaultButton="No",
            cancelButton="No",
            icon='warning'
        )
        if confirm == "Yes":
            try:
                cmds.delete(selected[0])
                list_cameras()
            except RuntimeError as e:
                cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def rename_camera(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if selected:
        result = cmds.promptDialog(
            title="Rename Camera",
            message="Enter new camera name:",
            button=["OK", "Cancel"],
            defaultButton="OK",
            cancelButton="Cancel",
            dismissString="Cancel"
        )
        if result == "OK":
            new_name = cmds.promptDialog(query=True, text=True)
            if cmds.objExists(new_name):
                cmds.confirmDialog(
                    title="Error",
                    message=f"A camera named '{new_name}' already exists.",
                    button=["OK"],
                    icon="critical"
                )
                return
            try:
                cmds.rename(selected[0], new_name)
                list_cameras()
            except RuntimeError as e:
                cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def toggle_lock_camera(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if not selected:
        cmds.warning("No camera selected.")
        return
    cam = selected[0]
    try:
        locked = cmds.getAttr(cam + ".translateX", lock=True)
        for attr in ["translate", "rotate", "scale"]:
            for axis in ["X", "Y", "Z"]:
                cmds.setAttr(f"{cam}.{attr}{axis}", lock=not locked)
        state = "locked" if not locked else "unlocked"
        cmds.inViewMessage(amg=f"Camera <hl>{cam}</hl> transforms {state}", pos="topCenter", fade=True)
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def export_cameras(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if not selected:
        cmds.warning("No cameras selected to export.")
        return
    file_path = cmds.fileDialog2(dialogStyle=2, fileMode=0, caption="Export Cameras", fileFilter="Maya ASCII (*.ma)")
    if not file_path:
        return
    file_path = file_path[0]
    try:
        cmds.select(selected, replace=True)
        cmds.file(file_path, force=True, options="v=0;", type="mayaAscii", exportSelected=True)
        cmds.inViewMessage(amg=f"Exported cameras: <hl>{', '.join(selected)}</hl>", pos="topCenter", fade=True)
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def import_cameras(*args):
    file_path = cmds.fileDialog2(dialogStyle=2, fileMode=1, caption="Import Cameras", fileFilter="Maya ASCII (*.ma)")
    if not file_path:
        return
    file_path = file_path[0]
    try:
        cmds.file(file_path, i=True, type="mayaAscii", ignoreVersion=True, mergeNamespacesOnClash=False)
        list_cameras()
        cmds.inViewMessage(amg=f"Imported cameras from <hl>{file_path}</hl>", pos="topCenter", fade=True)
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def set_renderable_camera(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if not selected:
        cmds.warning("No camera selected.")
        return
    cam = selected[0]
    all_cams = cmds.ls(type="camera")
    for cam_shape in all_cams:
        try:
            cmds.setAttr(cam_shape + ".renderable", 0)
        except Exception:
            pass
    try:
        cam_shape = cmds.listRelatives(cam, shapes=True, type="camera")[0]
        cmds.setAttr(cam_shape + ".renderable", 1)
        cmds.inViewMessage(amg=f"<hl>{cam}</hl> is now the renderable camera", pos="topCenter", fade=True)
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def duplicate_camera(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if not selected:
        cmds.warning("No camera selected.")
        return
    cam = selected[0]
    try:
        new_cam = cmds.duplicate(cam, renameChildren=True)[0]
        new_name = cmds.rename(new_cam, cam + "_copy#")
        list_cameras()
        cmds.inViewMessage(amg=f"Duplicated camera <hl>{cam}</hl> as <hl>{new_name}</hl>", pos="topCenter", fade=True)
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def show_camera_info(*args):
    selected = cmds.textScrollList("cameraList", query=True, selectItem=True)
    if not selected:
        cmds.warning("No camera selected.")
        return
    cam = selected[0]
    try:
        cam_shape = cmds.listRelatives(cam, shapes=True, type="camera")[0]
        focal_length = cmds.getAttr(cam_shape + ".focalLength")
        near_clip = cmds.getAttr(cam_shape + ".nearClipPlane")
        far_clip = cmds.getAttr(cam_shape + ".farClipPlane")
        renderable = cmds.getAttr(cam_shape + ".renderable")
        horizontal_ap = cmds.getAttr(cam_shape + ".horizontalFilmAperture")
        vertical_ap = cmds.getAttr(cam_shape + ".verticalFilmAperture")
        msg = (
            f"Camera: {cam}\n"
            f"Focal Length: {focal_length} mm\n"
            f"Near Clip: {near_clip}\n"
            f"Far Clip: {far_clip}\n"
            f"Renderable: {'Yes' if renderable else 'No'}\n"
            f"Film Aperture: {horizontal_ap} x {vertical_ap}"
        )
        cmds.confirmDialog(title="Camera Info", message=msg, button=["OK"], icon="information")
    except Exception as e:
        cmds.confirmDialog(title="Error", message=str(e), button=["OK"], icon="critical")

def add_camera_popup_menu(scroll_list_name="cameraList"):
    if cmds.popupMenu("camListMenu", exists=True):
        cmds.deleteUI("camListMenu")
    cmds.popupMenu("camListMenu", parent=scroll_list_name, button=3)
    cmds.menuItem(label="Set as Renderable", command=set_renderable_camera)
    cmds.menuItem(label="Duplicate Camera", command=duplicate_camera)
    cmds.menuItem(label="Show Camera Info", command=show_camera_info)

# -------------------------
# UI Function
# -------------------------
def cam_manager_ui():
    ui_title = 'cam_manager'
    if cmds.window(ui_title, exists=True):
        cmds.deleteUI(ui_title)
    window = cmds.window(ui_title, title='Camera Manager', widthHeight=(300, 900))
    main_col = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # Header
    cmds.frameLayout(label="Camera Manager", collapsable=False, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True)
    cmds.image(image=os.path.join(IMG_PATH, 'main_camera_image.jpeg'), height=100)
    cmds.setParent("..")

    # Camera List
    cmds.frameLayout(label="Cameras", collapsable=False, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True)
    cmds.textScrollList("cameraList", height=150, allowMultiSelection=True)
    add_camera_popup_menu("cameraList")
    cmds.setParent("..")

    # Buttons
    cmds.frameLayout(label="Camera Operations", collapsable=False, marginHeight=5)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
    cmds.button(label="Create New Camera", command=create_camera)
    cmds.button(label="Delete Camera", command=delete_camera)
    cmds.button(label="Rename Camera", command=rename_camera)
    cmds.button(label="Lock/Unlock Camera Transforms", command=toggle_lock_camera)
    cmds.button(label="Export Selected Cameras", command=export_cameras)
    cmds.button(label="Import Cameras", command=import_cameras)
    cmds.setParent("..")

    cmds.separator(style="in", height=10)
    cmds.text(label="Select a camera and use the right-click menu for more options.", align="center")
    cmds.showWindow(ui_title)
    list_cameras()

# -------------------------
# Shelf Button
# -------------------------
def add_shelf_button():
    shelf = "Custom"
    if cmds.shelfLayout(shelf, exists=True):
        cmds.shelfButton(
            parent=shelf,
            annotation="Camera Manager",
            label="CamMgr",
            image=os.path.join(IMG_PATH, "main_camera_image.jpg"),
            command="import camera_manager; camera_manager.cam_manager_ui()"
        )
        print("Camera Manager button added to shelf:", shelf)
