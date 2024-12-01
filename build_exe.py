import os
import sys
import subprocess
from importlib.metadata import distributions

def install_requirements():
    """Install required packages if they're not already installed"""
    required = {'python-dotenv', 'requests', 'pyinstaller'}
    installed = {dist.metadata['Name'].lower() for dist in distributions()}
    missing = required - installed

    if missing:
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

def build_exe():
    """Build the executable using PyInstaller"""
    subprocess.check_call([
        'pyinstaller',
        '--name=OneSignal Mailer by xioBrain',
        '--windowed',
        '--onefile',
        '--icon=app_icon.ico',
        '--add-data=settings.json;.',
        'gui.py'
    ])

def main():
    print("Installing requirements...")
    install_requirements()
    
    print("Building executable...")
    build_exe()
    
    print("\nBuild complete! You can find the executable in the 'dist' folder.")
    print("You can now run 'OneSignal Mailer by xioBrain.exe' by double-clicking it.")

if __name__ == '__main__':
    main()
