# powerchart_login.py
import os
import time
import subprocess
import platform
import tempfile
from pathlib import Path
from dotenv import load_dotenv

def wait_for_apps(app_names):
    """
    Waits for specified applications to be running
    
    Args:
        app_names: List of application names to wait for
    
    Returns:
        True when all apps are running
    """
    print(f"Waiting for applications to be running: {', '.join(app_names)}")
    
    def is_app_running(app_name):
        """Check if an app is running on the current platform"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                script = f'tell application "System Events" to count processes whose name is "{app_name}"'
                result = subprocess.run(['osascript', '-e', script], 
                                        capture_output=True, text=True, check=True)
                return int(result.stdout.strip()) > 0
            
            elif system == "Windows":  # Windows
                result = subprocess.run(f'tasklist /FI "IMAGENAME eq {app_name}.exe" /NH', 
                                      shell=True, capture_output=True, text=True, check=False)
                return 'No tasks' not in result.stdout
            
            else:
                print(f"Platform {system} is not supported for app detection.")
                return False
                
        except Exception as error:
            print(f"Error checking if {app_name} is running: {error}")
            return False
    
    def check_apps():
        """Check status of all apps"""
        statuses = []
        for app in app_names:
            running = is_app_running(app)
            print(f"{app}: {'Running' if running else 'Not running'}")
            statuses.append({"app": app, "running": running})
        
        # Return True only if all apps are running
        return all(status["running"] for status in statuses)
    
    # Poll until all apps are running
    all_running = check_apps()
    attempts = 1
    max_attempts = 40  # 40 seconds with 1-second intervals
    
    while not all_running and attempts < max_attempts:
        print(f"Attempt {attempts}/{max_attempts}: Not all apps running yet. Checking again in 1 second...")
        time.sleep(1)  # Wait 1 second
        all_running = check_apps()
        attempts += 1
    
    if not all_running:
        raise Exception(f"Timed out waiting for applications to launch: {', '.join(app_names)}")
    
    print("All required applications are now running!")
    return True

def login_to_powerchart():
    """
    Handles the PowerChart login process after Citrix Viewer and security app are open
    Uses credentials from environment variables
    
    Returns:
        True when login is complete successfully, False otherwise
    """
    print("Starting PowerChart login sequence...")
    
    # Load environment variables if available
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        print(".env file found, loading environment variables")
        load_dotenv()
    else:
        print(f".env file not found at: {env_path}")
        print(f"Working directory: {os.getcwd()}")
    
    try:
        # Get credentials from environment variables
        username = os.environ.get("CERNER_USERNAME")
        password = os.environ.get("CERNER_PASSWORD")
        
        # Verify credentials are available
        if not username or not password:
            raise Exception("Credentials not found. Please set CERNER_USERNAME and CERNER_PASSWORD environment variables.")
        
        print("Credentials check: Username and password found")
        
        # Wait for Citrix Viewer and Citrix Husk (which runs the Cerner Security app)
        apps_to_wait_for = ['Citrix Viewer', 'Citrix   Husk']
        print(f"Waiting for applications: {', '.join(apps_to_wait_for)}")
        
        wait_for_apps(apps_to_wait_for)
        print("Required applications detected as running")
        
        # Add a 8-second delay for margins as requested
        print("Adding 8-second delay for margins...")
        time.sleep(8)
        
        system = platform.system()
        if system == "Darwin":  # macOS
            # macOS approach using AppleScript
            print("Executing login sequence on macOS...")
            
            apple_script = f'''
            tell application "System Events"
              -- Focus on the Citrix   Husk process that runs the Cerner Security application
              tell process "Citrix   Husk"
                set frontmost to true
                delay 1
                
                -- Type username (assuming we're already in the username field)
                keystroke "{username}"
                delay 0.2
                
                -- Press tab to move to password field
                key code 48 -- Tab key
                delay 0.2
                
                -- Type password
                keystroke "{password}"
                delay 0.2
                
                -- Press return to submit
                key code 36 -- Return key
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
                print("Login sequence executed successfully")
                
                # Clean up
                os.unlink(temp_script_path)
                
                return True
            
            except subprocess.CalledProcessError as err:
                print(f"Error executing AppleScript for login: {err}")
                return False
            
        elif system == "Windows":  # Windows
            # Windows approach - basic implementation
            print("Executing login sequence on Windows...")
            
            # The following PowerShell script attempts to automate similar actions on Windows
            powershell_script = f'''
            # Find and focus the Citrix   Husk window that runs the Cerner security app
            $securityApp = Get-Process | Where-Object {{ $_.ProcessName -eq "Citrix   Husk" -or $_.MainWindowTitle -match "Cerner Server Security" }}
            if ($securityApp) {{
              [void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
              [System.Windows.Forms.SendKeys]::SendWait('{username}')
              Start-Sleep -Milliseconds 500
              [System.Windows.Forms.SendKeys]::SendWait('{{TAB}}')
              Start-Sleep -Milliseconds 500
              [System.Windows.Forms.SendKeys]::SendWait('{password}')
              Start-Sleep -Milliseconds 500
              [System.Windows.Forms.SendKeys]::SendWait('{{ENTER}}')
              Write-Output "Login sequence executed"
              exit 0
            }} else {{
              Write-Error "Could not find Cerner Server Security window"
              exit 1
            }}
            '''
            
            # Save script to temp file
            with tempfile.NamedTemporaryFile(suffix='.ps1', delete=False) as temp_file:
                temp_script_path = temp_file.name
            
            with open(temp_script_path, 'w') as f:
                f.write(powershell_script)
            
            try:
                # Run the script
                subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', temp_script_path], check=True)
                print("Login sequence executed successfully")
                
                # Clean up
                os.unlink(temp_script_path)
                
                return True
            
            except subprocess.CalledProcessError as err:
                print(f"Error executing PowerShell script for login: {err}")
                return False
        
        else:
            print(f"Platform {system} is not supported for automated login.")
            return False
    
    except Exception as err:
        print(f"Error in login_to_powerchart: {err}")
        return False

if __name__ == "__main__":
    success = login_to_powerchart()
    print(f"PowerChart login {'successful' if success else 'failed'}")
    exit(0 if success else 1)