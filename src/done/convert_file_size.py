from typing import Union

def convert_file_size(*, size: Union[int, float], from_unit: str, to_unit: str) -> float:
    """
    Converts a file size from one unit to another using binary (base-1024) conversion.
    
    Valid units: B, KB, MB, GB, TB
    """
    to_bytes_map = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
    }

    if size < 0:
        raise ValueError(f"Size must be non-negative, got: {size}")

    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    if from_unit not in to_bytes_map or to_unit not in to_bytes_map:
        raise ValueError(f"Invalid unit. Valid units are: {', '.join(to_bytes_map.keys())}")
    
    # Direct conversion: size * (from_factor / to_factor)
    return size * to_bytes_map[from_unit] / to_bytes_map[to_unit]
