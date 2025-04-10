# another way to determine WHEN the drag (& hold) should be let go:
# 1. use a pixel color code monitor. without warning, it's 1772, 1064.
# with warning, it's 1728, 1064.

#ALSO! Some documents in documents are NOT freeform texts, they're images.
# Need a way to distinguish that.


import subprocess
import time
import platform

def run_cliclick_command(command):
    """Run a cliclick command and return the result"""
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/cliclick"] + command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing cliclick command: {e}")
        print(f"Error output: {e.stderr}")
        return None

def activate_citrix_viewer():
    """Activate Citrix Viewer before performing actions"""
    system = platform.system()
    if system == "Darwin":  # macOS
        print("Activating Citrix Viewer...")
        try:
            # Use AppleScript to bring Citrix Viewer to the front
            activate_script = '''
            tell application "Citrix Viewer"
                activate
                delay 0.2
            end tell
            '''
            subprocess.run(['osascript', '-e', activate_script], check=True)
            print("Citrix Viewer activated successfully")
            return True
        except subprocess.CalledProcessError as err:
            print(f"Error activating Citrix Viewer: {err}")
            return False
    else:
        print(f"Platform {system} is not supported for this function.")
        return False

def click_hold_drag_wait_release(
    start_x, start_y,
    end_x, end_y,
    drag_duration=2.0,
    hold_duration=3.0
):
    """
    Perform a click-hold-drag-wait-release sequence using cliclick.
    
    Args:
        start_x, start_y: Starting coordinates
        end_x, end_y: Ending coordinates
        drag_duration: Time in seconds to drag from start to end
        hold_duration: Time in seconds to hold at the end position before releasing
    """
    # First activate Citrix Viewer
    if not activate_citrix_viewer():
        print("Failed to activate Citrix Viewer. Aborting the sequence.")
        return False
    
    # Wait a moment after activation
    time.sleep(1)
    
    print(f"Starting sequence at coordinates: ({start_x}, {start_y})")
    
    # Move to start position
    run_cliclick_command(f"m:{start_x},{start_y}")
    time.sleep(0.5)  # Give a moment for the cursor to arrive
    
    # Click and hold at start position
    print("Clicking and holding...")
    run_cliclick_command(f"dd:{start_x},{start_y}")
    time.sleep(0.5)  # Short delay after initial click
    
    # Calculate intermediate points for smooth dragging
    steps = max(int(drag_duration * 10), 10)  # At least 10 steps for smooth dragging
    step_delay = drag_duration / steps
    
    print(f"Dragging to ({end_x}, {end_y}) over {drag_duration} seconds...")
    for i in range(1, steps + 1):
        # Calculate intermediate position
        progress = i / steps
        current_x = int(start_x + (end_x - start_x) * progress)
        current_y = int(start_y + (end_y - start_y) * progress)
        
        # Move to intermediate position while still holding
        run_cliclick_command(f"m:{current_x},{current_y}")
        time.sleep(step_delay)
    
    # Hold at final position
    print(f"Holding at ({end_x}, {end_y}) for {hold_duration} seconds...")
    time.sleep(hold_duration)
    
    # Release at final position
    print("Releasing mouse button...")
    run_cliclick_command(f"du:{end_x},{end_y}")
    
    print("Sequence completed")
    return True

if __name__ == "__main__":
    # Starting coordinates
    START_X = 586
    START_Y = 410
    
    # Ending coordinates
    END_X = 1090
    END_Y = 1163
    
    # Execute the sequence
    print("Starting click-hold-drag-wait-release sequence...")
    result = click_hold_drag_wait_release(
        START_X, START_Y,
        END_X, END_Y,
        drag_duration=0,
        hold_duration=5.0
    )
    print(f"Test {'completed successfully' if result else 'failed'}")