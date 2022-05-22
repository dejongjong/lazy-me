import black
import os
from pathlib import Path

PKG_ROOT = Path(__file__).parents[1]
FILES_TO_BLACKEN = [
    PKG_ROOT / "test.py"
]

for file_path in FILES_TO_BLACKEN:
    with f as f:  
        blackened = black.format_file_contents(
            src_contents=f.read(),
            fast=True,
            mode=black.Mode()
        )
        f.write(blackened)
    
