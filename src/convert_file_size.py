def convert_file_size(*, size: int, from_unit: str, to_unit: str) -> float:
    """
    Converts a file size from one unit to another.

    Args:
        size: The numerical size of the file size.
        from_unit: The starting unit ('B', 'KB', 'MB', 'GB', 'TB').
        to_unit: The target unit to convert to ('B', 'KB', 'MB', 'GB', 'TB').

    Returns:
        The converted file size.
    """
    # Dictionary to convert any unit to bytes
    to_bytes_map = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
    }

    # Standardize units to uppercase
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    # Check for valid units
    if from_unit not in to_bytes_map or to_unit not in to_bytes_map:
        valid_units = list(to_bytes_map.keys())
        raise ValueError(f"Invalid unit. Please use one of: {valid_units}")
    
    # Convert the original size to bytes
    size_in_bytes = size * to_bytes_map[from_unit]

    # Convert from bytes to the target unit
    converted_size = size_in_bytes / to_bytes_map[to_unit]

    return converted_size
