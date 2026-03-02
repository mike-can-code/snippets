import re

def identify_edi_filename_parts(filename: str) -> dict:
    filename_parts = re.split('[_.]', filename)

    filename_parts_names = [
        'Project', 
        'EDI',
        'FileDate', 
        'FileTimestamp', 
        'UniqueID', 
        'FileDateRedundant', 
        'FileTimestampRedundant', 
        'FileExt', 
        'Status'
    ]
    
    if len(filename_parts) != len(filename_parts_names):
        print(f"Warning: Filename produced {len(filename_parts)} parts, but expected {len(filename_parts_names)}.")
        # You might want to handle this more robustly, but for now we'll zip the shortest
        
    return dict(zip(filename_parts_names, filename_parts))
