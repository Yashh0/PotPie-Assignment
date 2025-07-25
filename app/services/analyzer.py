# app/services/analyzer.py

import re
from typing import List, Dict


def split_diff_by_file(diff: str) -> List[Dict[str, str]]:
    """
    Splits a GitHub diff into individual file diffs.
    """
    file_diffs = []
    pattern = re.compile(r'diff --git a/(.*?) b/(.*?)\n(.*?)\n(?=diff --git|\Z)', re.DOTALL)

    for match in pattern.finditer(diff):
        filename = match.group(2)
        file_diff = match.group(3).strip()
        if file_diff:
            file_diffs.append({"filename": filename, "diff": file_diff})

    return file_diffs
