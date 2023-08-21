import sys
from cx_Freeze import setup, Executable
from cx_Freeze import bdist_msi

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this for a GUI application on Windows

executables = [Executable("New_edit.py", base=base, icon="output-onlinepngtools.ico", target_name="Movie Search.exe")]

# Add the image files to be included in the setup directory
image_files = ["header.jpg", "cinema5.jpg"]

setup(
    name="MovieSearchApp",
    version="1.0",
    description="A Movie Search and Database Management App",
    executables=executables,
    data_files=[("", image_files)],  # Include the image files in the setup directory
    options={
        "bdist_msi": {
            "add_to_path": False,  # Set to True if you want to add the app to the system PATH
        }
    },
)
