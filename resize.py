# powerchart_resize.py
import subprocess
import platform
import time
import os
from pathlib import Path

def resize_citrix_viewer():
    """
    Resizes the Citrix Viewer window to a predefined size
    
    Returns:
        None
    """
    print("Resizing Citrix Viewer...")
    
    system = platform.system()
    if system != "Darwin":  # Not macOS
        print("Resize is currently only supported on macOS")
        return
    
    # Create a debug log file
    subprocess.run('echo "Starting Citrix resize operation at $(date)" > /tmp/citrix-debug.log', 
                  shell=True, check=False)
    
    # AppleScript for resizing
    apple_script = '''
    tell application "Citrix Viewer" to activate
    tell application "System Events"
        tell process "Citrix Viewer"
            set frontWindow to first window
            set {x, y} to position of frontWindow
            set {width, height} to size of frontWindow
            set clickX to (x + width - 60)
            set clickY to (y + 15)
            do shell script "/opt/homebrew/bin/cliclick c:" & clickX & "," & clickY
        end tell
    end tell
    '''
    
    try:
        print("Executing AppleScript...")
        result = subprocess.run(['osascript', '-e', apple_script], 
                              capture_output=True, text=True, check=True)
        
        if result.stderr:
            print(f"Error executing AppleScript: {result.stderr}")
            return
        
        print(f"AppleScript result: {result.stdout}")
        print("Check /tmp/citrix-debug.log for detailed execution log")
        
        # Read and display the debug log
        try:
            log_result = subprocess.run(['cat', '/tmp/citrix-debug.log'], 
                                       capture_output=True, text=True, check=True)
            print(f"Debug log:\n{log_result.stdout}")
        except subprocess.CalledProcessError as err:
            print(f"Failed to read debug log: {err}")
        
    except subprocess.CalledProcessError as error:
        print(f"Failed to resize Citrix Viewer: {error}")
        
        # Try to get the debug log even in case of failure
        try:
            log_result = subprocess.run(['cat', '/tmp/citrix-debug.log'], 
                                       capture_output=True, text=True, check=True)
            print(f"Debug log after error:\n{log_result.stdout}")
        except subprocess.CalledProcessError as err:
            print(f"Failed to read debug log: {err}")

if __name__ == "__main__":
    resize_citrix_viewer()
    print("Resize operation complete.")