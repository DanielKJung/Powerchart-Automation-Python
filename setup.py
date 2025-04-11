from setuptools import setup, find_packages

setup(
    name="powerchart-mcp",
    version="0.1.0",
    description="MCP server for PowerChart automation using coordinates",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.2.0",
        "pyautogui>=0.9.54",
        "Pillow>=10.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "powerchart-mcp=powerchart_mcp:mcp.run",
        ],
    },
    python_requires=">=3.10",
)