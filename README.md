# Movie Library Desktop Application

A complete desktop application to manage your movie collection, allowing you to track movies you have watched and those you want to watch. This project has been converted into an installable software with an MSI setup.

## Features

- Add, edit, and delete movies in your library.
- Categorize movies as watched or want to watch.
- Analyze and visualize your movie data.
- User-friendly graphical interface.

## Files Overview

- **New_edit.py**  
  The main application script that launches the GUI for managing the movie library. This script contains the full functionality of adding, editing, and viewing movies along with saving data to CSV files.

- **msi_setup.py**  
  The setup script used to build an MSI installer for Windows. It packages the application into an executable and creates an easy-to-use Windows installer, enabling simple installation on any compatible system.

## Installation and Usage

### Prerequisites

- Python 3.8 or higher installed on your system.
- Required Python packages installed via:

  ```bash
  pip install -r requirements.txt

Running the Application
To launch the application directly without installation, run:

```bash
python New_edit.py
```

Creating the MSI Installer
To create a Windows installer package (MSI file), run:

```bash
python msi_setup.py
```
This will generate an MSI installer in the build folder. Use this installer to install the Movie Library application on Windows systems easily.

---
### Requirements
The project depends on the following Python packages:

```bash
requests
pillow
tabulate
ttkthemes
```
---
## Project Structure

```bash
movie-Library/
│
├── New_edit.py         # Main GUI application script
├── msi_setup.py        # MSI build and setup script
├── requirements.txt    # Required Python packages
├── movie_results.csv   # Data file for movie entries
├── watched_movies.csv  # Data file for watched movies
├── want_to_watch_movies.csv  # Data file for movies planned to watch
├── analyze.csv         # Data file for movie analysis
├── cinema5.jpg         # Background or UI image asset
└── header.jpg          # Header image asset

```
---
### Notes

- The application saves data in CSV files located in the project directory.
- Ensure that all dependencies are installed before running or packaging.
- The MSI installer is built using cx_Freeze and WiX Toolset. Make sure you have WiX installed and properly configured for MSI creation.
---
### Support
For any issues or feature requests, please open an issue on the GitHub repository.
---
## Author

This Movie Library application was developed by *Navid TK.*, combining my passion for movies and programming.  
If you have any questions, suggestions, or want to collaborate, feel free to reach out!

---

Thanks for checking out my project!
