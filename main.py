"""An alternative entry point for pytest; mainly for PyInstaller"""

import sys

import pytest

if __name__ == "__main__":
    pytest.main(sys.argv[1:])
