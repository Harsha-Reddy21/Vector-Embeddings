import re
from typing import List, Dict, Any

def extract_timestamps(text: str) -> List[Dict[str, float]]:
    """
    Extract timestamps from text in the format [MM:SS] or [HH:MM:SS].
    
    Args:
        text: Text containing timestamps
        
    Returns:
        List of dictionaries with start and end times in seconds
    """
    # Pattern for [MM:SS] format
    pattern1 = r'\[(\d{1,2}):(\d{2})\]'
    # Pattern for [HH:MM:SS] format
    pattern2 = r'\[(\d{1,2}):(\d{2}):(\d{2})\]'
    # Pattern for timestamps like [12.34 → 45.67]
    pattern3 = r'\[(\d+\.\d+)\s*(?:→|-|to)\s*(\d+\.\d+)\]'
    
    timestamps = []
    
    # Find all [MM:SS] timestamps
    for match in re.finditer(pattern1, text):
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        time_seconds = minutes * 60 + seconds
        timestamps.append({"start": time_seconds, "end": time_seconds + 30})  # Assume 30 second segment
    
    # Find all [HH:MM:SS] timestamps
    for match in re.finditer(pattern2, text):
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        time_seconds = hours * 3600 + minutes * 60 + seconds
        timestamps.append({"start": time_seconds, "end": time_seconds + 30})  # Assume 30 second segment
    
    # Find all [start → end] timestamps
    for match in re.finditer(pattern3, text):
        start = float(match.group(1))
        end = float(match.group(2))
        timestamps.append({"start": start, "end": end})
    
    return timestamps


def format_timestamp(seconds: float) -> str:
    """
    Format seconds into MM:SS or HH:MM:SS string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}" 