import re
from typing import Dict, Optional

def identify_edi_filename_parts(filename: str) -> Dict[str, str]:
    """
    Parse an EDI filename into its component parts.
    
    Expected format:
        {Project}_{EDI}_{FileDate}_{FileTimestamp}_{UniqueID}_{FileDateRedundant}_{FileTimestampRedundant}.{FileExt}.{Status}
        
    Example:
        P3I_180M_20230930_184304000_0000002284_2023-09-30Z_184705.txt.complete
        
    Args:
        filename: The EDI filename to parse
        
    Returns:
        Dictionary with keys: Project, EDI, FileDate, FileTimestamp, UniqueID,
        FileDateRedundant, FileTimestampRedundant, FileExt, Status
        
    Raises:
        ValueError: If filename format is invalid
    """
    if not filename or not isinstance(filename, str):
        raise ValueError(f"Filename must be a non-empty string, got: {filename}")
    
    # Split on underscores only, handle extensions separately
    parts = filename.split('_')
    
    if len(parts) != 7:
        raise ValueError(
            f"Invalid filename format. Expected 7 underscore-separated parts, "
            f"got {len(parts)} in '{filename}'"
        )
    
    # Last part contains: {FileTimestampRedundant}.{FileExt}.{Status}
    # Example: 184705.txt.complete
    last_part = parts[6]
    last_parts = last_part.split('.')
    
    if len(last_parts) < 2:
        raise ValueError(
            f"Invalid filename format. Expected at least extension and status, "
            f"got '{last_part}'"
        )
    
    # Extract components
    file_timestamp_redundant = last_parts[0]
    
    # Handle optional .complete suffix
    if len(last_parts) == 3:
        # Format: timestamp.ext.status (e.g., 184705.txt.complete)
        file_ext = last_parts[1]
        status = last_parts[2]
    elif len(last_parts) == 2:
        # Format: timestamp.ext (e.g., 184705.txt)
        file_ext = last_parts[1]
        status = None
    else:
        # More than 3 parts - combine middle parts as extension
        file_ext = '.'.join(last_parts[1:-1])
        status = last_parts[-1]
    
    return {
        'Project': parts[0],
        'EDI': parts[1],
        'FileDate': parts[2],
        'FileTimestamp': parts[3],
        'UniqueID': parts[4],
        'FileDateRedundant': parts[5],
        'FileTimestampRedundant': file_timestamp_redundant,
        'FileExt': file_ext,
        'Status': status
    }


# Test cases
if __name__ == '__main__':
    # Test with .complete
    result1 = identify_edi_filename_parts(
        'P3I_180M_20230930_184304000_0000002284_2023-09-30Z_184705.txt.complete'
    )
    print(result1)
    # Expected: Status = 'complete'
    
    # Test without .complete
    result2 = identify_edi_filename_parts(
        'P3I_180M_20230930_184304000_0000002284_2023-09-30Z_184705.txt'
    )
    print(result2)
    # Expected: Status = None
