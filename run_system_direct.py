#!/usr/bin/env python3
"""Direct system runner without virtual environment issues"""

import subprocess
import sys

# Run with system Python directly
subprocess.run(['/usr/bin/python3', 'run_orion_system.py'])