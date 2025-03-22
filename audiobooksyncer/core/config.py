"""Configs which can be set using CLI options."""

import os

aeneas_processes = os.cpu_count()
"""
Number of processes for audio alignment.
"""

aeneas_dtw_margin = 120
"""
DWT margin for audio alignment.
"""
