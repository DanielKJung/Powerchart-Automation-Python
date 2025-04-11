"""
PowerChart MCP Server

This MCP server implements an interface for automating interactions with PowerChart
via pre-defined coordinates for clicking and navigating the interface.
"""

import os
import subprocess
import platform
import time
import json
from typing import Any, Dict, List, Optional, Tuple, Literal
from pathlib import Path
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

# Create an MCP server
mcp = FastMCP(
    "PowerChart Automation", 
    description="Automates PowerChart EHR interactions using coordinate-based automation",
    dependencies=["pyautogui", "Pillow", "python-dotenv"]
)

# ===================================
# Models for PowerChart Navigation
# ===================================

class NavigationLocation(BaseModel):
    """Represents a clickable location in PowerChart UI"""
    x: int
    y: int
    name: str
    description: Optional[str] = None

class ScreenSection(BaseModel):
    """Screen section with capture coordinates"""
    left_x: int
    upper_y: int
    right_x: int
    lower_y: int
    name: str

# ===================================
# Load Coordinates from JSON
# ===================================

# This dictionary will hold all coordinates organized by section
COORDINATES = {}
SCREEN_SECTIONS = {}

def load_coordinates_json():
    """Load coordinates from the coordinates.json file"""
    possible_paths = [
        "coordinates.json",  # Current directory
        "../coordinates.json",  # Parent directory
        str(Path.home() / "coordinates.json"),  # Home directory
        str(Path(__file__).parent / "coordinates.json"),  # Script directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    
                    # Load coordinates
                    for section, items in data.items():
                        if section == "screen_sections":
                            # Handle screen sections specially
                            for name, section_data in items.items():
                                SCREEN_SECTIONS[name] = ScreenSection(
                                    left_x=section_data["left_x"],
                                    upper_y=section_data["upper_y"],
                                    right_x=section_data["right_x"],
                                    lower_y=section_data["lower_y"],
                                    name=section_data["name"]
                                )
                        else:
                            # Handle regular coordinate sections
                            if isinstance(items, dict):
                                # Section has subsections
                                COORDINATES[section] = {}
                                for subsection, coords in items.items():
                                    COORDINATES[section][subsection] = []
                                    for item in coords:
                                        COORDINATES[section][subsection].append(
                                            NavigationLocation(**item)
                                        )
                            else:
                                # Regular section with coordinates
                                COORDINATES[section] = []
                                for item in items:
                                    COORDINATES[section].append(
                                        NavigationLocation(**item)
                                    )
                    
                    print(f"Loaded coordinates from {path}")
                    return True
            except Exception as e:
                print(f"Error loading coordinates from {path}: {e}")
    
    print("Warning: coordinates.json file not found. Proceeding with empty coordinates.")
    return False

# Initialize coordinates
load_coordinates_json()

# ===================================
# Automation Helper Functions
# ===================================

def click_at_coordinates(x: int, y: int, clicks: int = 1, interval: float = 0.5):
    """Click at specific coordinates using platform-appropriate methods"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # Use cliclick if available
        if os.path.exists("/opt/homebrew/bin/cliclick"):
            cmd = ["/opt/homebrew/bin/cliclick", f"c:{x},{y}"]
            if clicks > 1:
                for _ in range(clicks):
                    subprocess.run(cmd)
                    time.sleep(interval)
            else:
                subprocess.run(cmd)
        else:
            # Fallback to pyautogui
            print("Starting powerchart_mcp.py...")
            import pyautogui
            print("Imported pyautogui")
            pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)
    else:
        # Use pyautogui for other platforms
        import pyautogui
        pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)
    
    # Wait a moment after clicking
    time.sleep(0.3)

def take_screenshot(section: str = None):
    """Take a screenshot of the specified section or full screen"""
    import pyautogui
    from PIL import Image
    import io
    
    if section and section in SCREEN_SECTIONS:
        section_info = SCREEN_SECTIONS[section]
        region = (
            section_info.left_x, 
            section_info.upper_y, 
            section_info.right_x - section_info.left_x, 
            section_info.lower_y - section_info.upper_y
        )
        screenshot = pyautogui.screenshot(region=region)
    else:
        screenshot = pyautogui.screenshot()
    
    # Convert to bytes for return
    buf = io.BytesIO()
    screenshot.save(buf, format='PNG')
    buf.seek(0)
    
    return buf.getvalue()

def find_location_by_name(section: str, name: str, subsection: str = None) -> Optional[NavigationLocation]:
    """Find a location by its name in the specified section"""
    if section in COORDINATES:
        section_coords = COORDINATES[section]
        
        if isinstance(section_coords, list):
            for loc in section_coords:
                if loc.name.lower() == name.lower():
                    return loc
        elif isinstance(section_coords, dict):
            if subsection and subsection in section_coords:
                # Search in specific subsection if provided
                for loc in section_coords[subsection]:
                    if loc.name.lower() == name.lower():
                        return loc
            else:
                # Search in all subsections
                for subsection_items in section_coords.values():
                    for loc in subsection_items:
                        if loc.name.lower() == name.lower():
                            return loc
    
    return None

# ===================================
# MCP Tools for PowerChart Automation
# ===================================

@mcp.tool()
def navigate_to(section: str, element: str, subsection: str = None) -> str:
    """
    Navigate to a specific element within a section of PowerChart.
    
    Args:
        section: The section of PowerChart where the element is located
        element: The name of the UI element to click
        subsection: Optional subsection within the section (e.g., "default" or "scrolled" for section_headers)
    
    Returns:
        Result message
    """
    location = find_location_by_name(section, element, subsection)
    
    if not location:
        if subsection:
            return f"Error: Could not find element '{element}' in section '{section}', subsection '{subsection}'"
        else:
            return f"Error: Could not find element '{element}' in section '{section}'"
    
    click_at_coordinates(location.x, location.y)
    if subsection:
        return f"Clicked on {element} (coordinates: {location.x}, {location.y}) in subsection {subsection}"
    else:
        return f"Clicked on {element} (coordinates: {location.x}, {location.y})"

@mcp.tool()
def double_click_element(section: str, element: str, subsection: str = None) -> str:
    """
    Double-click on a specific element within a section of PowerChart.
    
    Args:
        section: The section of PowerChart where the element is located
        element: The name of the UI element to double-click
    
    Returns:
        Result message
    """
    location = find_location_by_name(section, element, subsection)
    
    if not location:
        if subsection:
            return f"Error: Could not find element '{element}' in section '{section}', subsection '{subsection}'"
        else:
            return f"Error: Could not find element '{element}' in section '{section}'"
    
    click_at_coordinates(location.x, location.y, clicks=2, interval=0.1)
    if subsection:
        return f"Double-clicked on {element} (coordinates: {location.x}, {location.y}) in subsection {subsection}"
    else:
        return f"Double-clicked on {element} (coordinates: {location.x}, {location.y})"

@mcp.tool()
def scroll_section(section: str, direction: Literal["up", "down"], clicks: int = 1) -> str:
    """
    Scroll up or down within a section of PowerChart.
    
    Args:
        section: The section of PowerChart to scroll
        direction: Direction to scroll ("up" or "down")
        clicks: Number of scroll operations to perform
    
    Returns:
        Result message
    """
    # Find scroll coordinates for the section
    scroll_name = f"scroll {direction}"
    location = find_location_by_name(section, scroll_name)
    
    if not location:
        return f"Error: Could not find scroll {direction} element for section '{section}'"
    
    for _ in range(clicks):
        click_at_coordinates(location.x, location.y)
        time.sleep(0.2)  # Small delay between scrolls
    
    return f"Scrolled {direction} {clicks} times in section '{section}'"

@mcp.tool()
def capture_screen_section(section: str) -> bytes:
    """
    Capture a screenshot of a specific section of PowerChart.
    
    Args:
        section: The section of PowerChart to capture
    
    Returns:
        Screenshot image data
    """
    if section not in SCREEN_SECTIONS:
        return f"Error: Section '{section}' not defined for screenshots"
    
    screenshot_data = take_screenshot(section)
    return screenshot_data

@mcp.resource("coordinates://{section}")
def get_coordinates(section: str) -> str:
    """
    Get the available coordinates for a specific section.
    
    Args:
        section: Section name to get coordinates for
    
    Returns:
        Information about available coordinates
    """
    if section not in COORDINATES:
        return f"No coordinates available for section '{section}'"
    
    section_coords = COORDINATES[section]
    result = f"Available coordinates in section '{section}':\n\n"
    
    if isinstance(section_coords, list):
        for loc in section_coords:
            result += f"- {loc.name}: ({loc.x}, {loc.y})"
            if loc.description:
                result += f" - {loc.description}"
            result += "\n"
    elif isinstance(section_coords, dict):
        for subsection, locs in section_coords.items():
            result += f"Subsection '{subsection}':\n"
            for loc in locs:
                result += f"  - {loc.name}: ({loc.x}, {loc.y})"
                if loc.description:
                    result += f" - {loc.description}"
                result += "\n"
            result += "\n"
    
    return result

@mcp.resource("sections://list")
def list_sections() -> str:
    """
    List all available sections in PowerChart for navigation.
    
    Returns:
        List of available sections
    """
    result = "Available PowerChart sections:\n\n"
    
    for section in COORDINATES.keys():
        result += f"- {section}\n"
    
    result += "\nAvailable screenshot sections:\n\n"
    for section in SCREEN_SECTIONS.keys():
        result += f"- {section}\n"
    
    return result

@mcp.tool()
def click_patient_from_list(position: int) -> str:
    """
    Click on a patient at a specific position in the patient list.
    
    Args:
        position: Position of the patient in the list (1-based)
    
    Returns:
        Result message
    """
    # Find the appropriate patient coordinate based on position
    patient_name = f"Patient {position}"
    location = find_location_by_name("specific_patient_list", patient_name)
    
    if not location:
        return f"Error: Could not find patient at position {position}"
    
    double_click = click_at_coordinates(location.x, location.y, clicks=2, interval=0.1)
    return f"Double-clicked on patient at position {position} (coordinates: {location.x}, {location.y})"

@mcp.tool()
def perform_workflow(workflow_name: str) -> str:
    """
    Perform a predefined workflow in PowerChart.
    
    Args:
        workflow_name: Name of the workflow to perform
    
    Returns:
        Result of the workflow
    """
    workflows = {
        "open_patient_list": [
            {"action": "navigate_to", "params": {"section": "home", "element": "Patient List"}},
            {"action": "navigate_to", "params": {"section": "patient_lists", "element": "Pink A"}}
        ],
        "check_documentation": [
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Provider View"}},
            {"action": "navigate_to", "params": {"section": "documentation", "element": "Documentation"}},
            {"action": "capture_screen_section", "params": {"section": "inpatient_manage"}}
        ],
        "view_lab_results": [
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Provider View"}},
            {"action": "navigate_to", "params": {"section": "labs", "element": "Results Review"}},
            {"action": "navigate_to", "params": {"section": "labs", "element": "All Laboratory"}}
        ],
        "check_patient_details": [
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Provider View"}},
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Inpatient/Manage"}},
            {"action": "navigate_to", "params": {"section": "section_headers", "element": "Hospital Course", "subsection": "default"}},
            {"action": "capture_screen_section", "params": {"section": "inpatient_manage"}},
            {"action": "navigate_to", "params": {"section": "section_headers", "element": "Problem List", "subsection": "default"}},
            {"action": "capture_screen_section", "params": {"section": "inpatient_manage"}}
        ],
        "view_media_gallery": [
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Provider View"}},
            {"action": "navigate_to", "params": {"section": "specific_patient", "element": "Inpatient/Manage"}},
            {"action": "navigate_to", "params": {"section": "section_headers", "element": "Media Gallery", "subsection": "default"}},
            {"action": "capture_screen_section", "params": {"section": "media_gallery_folder"}}
        ]
    }
    
    if workflow_name not in workflows:
        return f"Error: Workflow '{workflow_name}' not defined"
    
    results = []
    for step in workflows[workflow_name]:
        action = step["action"]
        params = step["params"]
        
        if action == "navigate_to":
            # Check if subsection is specified
            subsection = params.pop("subsection", None)
            if subsection:
                # Find location in specific subsection
                location = find_location_by_name(params["section"], params["element"], subsection)
                if not location:
                    message = f"Error: Could not find element '{params['element']}' in section '{params['section']}', subsection '{subsection}'"
                    results.append(message)
                    continue
                
                # Click on the location
                click_at_coordinates(location.x, location.y)
                message = f"Clicked on {params['element']} (coordinates: {location.x}, {location.y}) in subsection {subsection}"
                results.append(message)
            else:
                # Use regular navigate_to function
                result = navigate_to(**params)
                results.append(result)
            
            time.sleep(1)  # Wait between navigation steps
        elif action == "capture_screen_section":
            section = params.get("section")
            if section in SCREEN_SECTIONS:
                result = f"Screen section '{section}' captured"
                capture_screen_section(**params)
                results.append(result)
            else:
                results.append(f"Error: Screen section '{section}' not found")
    
    return f"Workflow '{workflow_name}' completed. Steps performed:\n" + "\n".join(results)

# Start the server when run directly
if __name__ == "__main__":
    mcp.run()