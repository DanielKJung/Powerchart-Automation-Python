# powerchart_quit.py
import os
import subprocess
import platform
import tempfile
import time
from pathlib import Path

def quit_powerchart():
    """
    Quits the PowerChart application via Citrix Viewer using the direct method:
    Citrix Viewer menu -> "Sign Out and Quit Citrix Viewer"
    
    Returns:
        True if PowerChart was successfully quit, False otherwise
    """
    print("Starting PowerChart direct quit sequence...")
    
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            # Check if Citrix Viewer is running before attempting to quit
            try:
                result = subprocess.run("pgrep -f 'Citrix Viewer' || echo 'not_running'", 
                                      shell=True, capture_output=True, text=True, check=False)
                if result.stdout.strip() == "not_running":
                    print("Citrix Viewer is not running. No action needed.")
                    return True  # Return success since there's nothing to quit
            except Exception as check_err:
                print(f"Error checking if Citrix Viewer is running: {check_err}")
                # Continue anyway as the main script will handle errors
            
            # Create debug log file
            with tempfile.NamedTemporaryFile(suffix='_citrix_quit_debug.log', delete=False) as temp_file:
                temp_log_path = temp_file.name
            
            with open(temp_log_path, 'w') as f:
                f.write(f"Quit attempt started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print('Using direct "Sign Out and Quit" method on macOS...')
            
            apple_script = f'''
            tell application "Citrix Viewer"
              activate
              delay 0.5
              
              tell application "System Events"
                tell process "Citrix Viewer"
                  -- Log all menu bar items for debugging
                  set menuBarItems to name of every menu bar item of menu bar 1
                  do shell script "echo 'Menu bar items: " & menuBarItems & "' >> '{temp_log_path}'"
                  
                  -- Click on the Citrix Viewer menu (typically the second menu item)
                  click menu bar item 2 of menu bar 1
                  delay 0.3
                  
                  -- Log all menu items in the Citrix Viewer menu
                  set menuItems to name of every menu item of menu 1 of menu bar item 2 of menu bar 1
                  do shell script "echo 'Citrix Viewer menu items: " & menuItems & "' >> '{temp_log_path}'"
                  
                  -- Try to click on "Sign Out and Quit Citrix Viewer" directly
                  try
                    click menu item "Sign Out and Quit Citrix Viewer" of menu 1 of menu bar item 2 of menu bar 1
                    do shell script "echo 'Successfully clicked on Sign Out and Quit menu item' >> '{temp_log_path}'"
                  on error errMsg
                    do shell script "echo 'Error: " & errMsg & "' >> '{temp_log_path}'"
                    -- Fallback to the old method in case the menu item doesn't exist
                    click menu item "Quit Citrix Viewer..." of menu 1 of menu bar item 2 of menu bar 1
                    delay 1
                    click button "Sign Out" of window 1
                  end try
                end tell
              end tell
            end tell
            '''
            
            # Save script to temp file
            with tempfile.NamedTemporaryFile(suffix='.scpt', delete=False) as temp_file:
                temp_script_path = temp_file.name
            
            with open(temp_script_path, 'w') as f:
                f.write(apple_script)
            
            try:
                # Run the script
                subprocess.run(['osascript', temp_script_path], check=True)
                print("PowerChart direct quit attempt completed")
                
                # Display debug log
                try:
                    with open(temp_log_path, 'r') as f:
                        log_content = f.read()
                    print(f"Debug log:\n{log_content}")
                except Exception as log_err:
                    print(f"Error reading debug log: {log_err}")
                
                # Clean up
                os.unlink(temp_script_path)
                
                return True
            
            except subprocess.CalledProcessError as err:
                print(f"Error executing AppleScript: {err}")
                
                # Display debug log even on error
                try:
                    with open(temp_log_path, 'r') as f:
                        log_content = f.read()
                    print(f"Debug log after error:\n{log_content}")
                except Exception as log_err:
                    print(f"Error reading debug log: {log_err}")
                
                return False
        
        elif system == "Windows":  # Windows
            print("PowerChart quit for Windows not yet implemented")
            return False
        
        else:
            print(f"Platform {system} is not supported.")
            return False
    
    except Exception as err:
        print(f"Error in quit_powerchart: {err}")
        return False

if __name__ == "__main__":
    success = quit_powerchart()
    print(f"PowerChart quit {'successful' if success else 'failed'}")
    exit(0 if success else 1)