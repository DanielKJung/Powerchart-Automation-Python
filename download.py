# powerchart_download.py
import os
import time
from datetime import datetime
import subprocess
from pathlib import Path
import platform
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def download_powerchart_ica(
    username=None, 
    password=None, 
    download_path=None, 
    headless=True
):
    """
    Downloads and opens the PowerChart ICA file from Cerner
    
    Args:
        username: Optional username (falls back to env variable)
        password: Optional password (falls back to env variable)
        download_path: Optional custom download path
        headless: Whether to run browser in headless mode (default: True)
    
    Returns:
        Path to the downloaded file
    """
    print("Starting PowerChart download script...")
    
    # Load environment variables if available
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        print(".env file found, loading environment variables")
        load_dotenv()
    else:
        print(f".env file not found at: {env_path}")
        print(f"Working directory: {os.getcwd()}")
    
    try:
        # Get credentials from parameters or environment variables
        user_creds = username or os.environ.get("CERNER_USERNAME")
        pass_creds = password or os.environ.get("CERNER_PASSWORD")
        
        print(f"Credentials check: {'Username found' if user_creds else 'Username NOT found'}")
        
        # Verify credentials are available
        if not user_creds or not pass_creds:
            raise Exception("Credentials not found. Please provide credentials or set CERNER_USERNAME and CERNER_PASSWORD environment variables.")

        # Define download path
        downloads_path = download_path or os.environ.get("DOWNLOAD_PATH") or os.path.join(str(Path.home()), "Downloads")
        
        print(f"Download path: {downloads_path}")
        
        # Generate filename with timestamp to avoid conflicts
        timestamp = datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file_path = os.path.join(downloads_path, f"PowerChart-{timestamp}.ica")
        
        print(f"Target file path: {file_path}")
        print("Launching browser...")

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=headless)
            print("Browser launched successfully")
            
            downloaded_path = ""
            
            try:
                # Create new context and page
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
                print("Browser page created")

                # Navigate to login page
                base_url = os.environ.get("CERNER_BASE_URL", "https://trummo.cernerworks.com/Citrix/ProdWeb/")
                print(f"Navigating to Cerner login page at {base_url}...")
                page.goto(base_url)
                print("Login page loaded")

                # Fill in credentials
                print("Filling in credentials...")
                page.get_by_role("textbox", name="User name:").fill(user_creds)
                page.get_by_role("textbox", name="User name:").press("Tab")
                page.get_by_role("textbox", name="Password:").fill(pass_creds)

                # Log in
                print("Logging in...")
                page.get_by_role("link", name="Log On").click()
                print("Login submitted")

                # Wait for download to be triggered by button click
                print("Waiting for PowerChart link to appear...")
                page.wait_for_selector('a:has-text("Powerchart P275 TRUM_MO")')
                
                # Set up download handler
                print("Setting up download handler...")
                with page.expect_download() as download_info:
                    # Click the PowerChart app link
                    print("Clicking PowerChart link...")
                    page.get_by_role("link", name="Powerchart P275 TRUM_MO Powerchart P275 TRUM_MO").click()
                    print("PowerChart link clicked")
                
                # Wait for the download to complete
                print("Waiting for download to start...")
                download = download_info.value
                print("Download started, waiting for completion...")
                
                # Save the file
                download.save_as(file_path)
                downloaded_path = file_path
                
                print(f"Download completed successfully to: {file_path}")
                
            except Exception as err:
                print(f"Error during browser automation: {err}")
                raise err
            finally:
                # Close the browser
                print("Closing browser...")
                browser.close()
                print("Browser closed")

        # Open the file if download was successful
        if downloaded_path:
            print("Attempting to open ICA file...")
            open_ica_file(downloaded_path)
        
        return downloaded_path
    
    except Exception as error:
        print(f"Error in download_powerchart_ica function: {error}")
        raise error

def open_ica_file(file_path):
    """
    Opens an ICA file with the system's default application
    
    Args:
        file_path: Path to the ICA file
    """
    print("Opening ICA file with system default application")
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print('Detected macOS, using "open" command')
        try:
            subprocess.run(["open", file_path], check=True)
            print("ICA file opened successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open ICA file: {e}")
    
    elif system == "Windows":  # Windows
        print('Detected Windows, using "start" command')
        try:
            # Windows-specific function to open a file with its associated application
            os.startfile(file_path)
            print("ICA file opened successfully")
        except Exception as e:
            print(f"Failed to open ICA file: {e}")
    
    else:  # Linux or other OS
        print(f"Detected other OS ({system}). ICA file downloaded to: {file_path}. Please open it manually.")

if __name__ == "__main__":
    try:
        file_path = download_powerchart_ica()
        print("Script completed successfully")
        print(f"ICA file path: {file_path}")
    except Exception as err:
        print(f"Script failed with error: {err}")
        exit(1)