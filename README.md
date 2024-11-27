# tylr.py - Convert Python Script to Windows Executable

This repository contains a Python script (`tylr.py`) and instructions on how to turn it into a standalone `.exe` file, which can be run on a Windows machine without needing to run the script via the terminal any time you want to start it.

## Steps to Download and Build the Executable

Follow these steps to download the script, install dependencies, build the `.exe` file, and run it:

---

### 1. Download or Clone the Repository

#### Option 1: Download the Repository as a ZIP file

1. Click the green **Code** button on the top right of the page.
2. Select **Download ZIP**.
3. Extract the contents of the ZIP file to a folder on your computer.

#### Option 2: Clone the Repository (if you have Git installed)

If you have Git installed, you can clone the repository using the following command in your terminal or Git Bash:

git clone https://github.com/your-username/your-repository.git

### Install Python
If you don't have Python installed, follow these steps:

Download Python from the official website: https://www.python.org/downloads/.

Install Python, and make sure to check the box that says "Add Python to PATH" during installation.

After installation, verify Python is installed by running the following command in Command Prompt or PowerShell:

python --version

You should see the Python version installed on your system.

### Install Required Dependencies
Before building the .exe, you need to install some Python libraries. These dependencies are required to run the script and build the executable.

Open Command Prompt or PowerShell on your computer.

Navigate to the folder where you downloaded or cloned the repository. For example, if you extracted the ZIP file to C:\Projects\tylr, use the following command to change the directory:

cd C:\Projects\tylr
Install the necessary Python libraries by running the following command:

pip install -r requirements.txt

This will install all the dependencies listed in the requirements.txt file. If you do not have a requirements.txt file, you will need to manually install the required libraries.

### Build the Executable
Once you have all the necessary dependencies installed, you can build the .exe file.

In Command Prompt or PowerShell, navigate to the folder where the tylr.py script is located (if you haven’t already).

Run the following command to build the .exe:

python -m PyInstaller --onefile --noconsole tylr.py

--onefile: This option bundles everything into a single .exe file.
--noconsole: This option ensures that the console window does not open when running the .exe (ideal for GUI applications).

This process may take a few minutes, depending on the size of the script and dependencies.

### Run the Executable
To run the .exe file:

Navigate to the dist folder.
Double-click on tylr.exe to run the script as a standalone application.
You should now be able to run the script without needing Python installed.