# app/ingest/readers.py
import os
from pathlib import Path
from typing import List

# Extensions we allow
ALLOWED_EXT = {
    ".txt", ".md", ".pdf", ".docx", ".csv", ".xlsx"
}

# Directories we exclude
EXCLUDED_DIRS = {
    "/System", "/Library", "/Applications", "/Volumes",
    ".git", "node_modules", "__pycache__", ".venv"
}

# Max file size in bytes (5 MB default)
MAX_FILE_SIZE = 5 * 1024 * 1024


def extract_text_by_ext(path: Path) -> str:
    # For now only safe read of txt/md
    if path.suffix.lower() in [".txt", ".md"]:
        try:
            return path.read_text(errors="ignore")
        except Exception:
            return ""
    return ""


def crawl_folder(root: Path) -> List[Path]:
    """
    Walk folder tree and return list of allowed files.
    Applies extension filters, size limits, and excludes certain directories.
    """
    files: List[Path] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]

        for fname in filenames:
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()

            if ext not in ALLOWED_EXT:
                continue

            try:
                if fpath.stat().st_size > MAX_FILE_SIZE:
                    continue
            except Exception:
                continue

            files.append(fpath)

    return sorted(files)