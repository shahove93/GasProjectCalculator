"""PyInstaller entry point for the GasProjectCalculator desktop application."""

import sys

from app.desktop_launcher import main

if __name__ == "__main__":
    sys.exit(main())
