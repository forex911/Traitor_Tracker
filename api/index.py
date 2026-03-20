import os
import sys

# Append the root path so `app.py` and other modules can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
