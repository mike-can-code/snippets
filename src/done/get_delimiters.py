from typing import Dict, Optional, List

def get_delimiters(dirty_txt: str) -> Dict[str, Optional[str]]:

    #-----------Remove everything before "ISA"
    try:
        isa_start_location: int = dirty_txt.index('ISA')
        clean_txt: str = dirty_txt[isa_start_location:]
    except ValueError:
        raise ValueError("Fatal: Could not find 'ISA' segment in the provided EDI content.")

    #-----------Get Element Separator
    # Element Separator is in position 4 (python is zero based so we use 3)
    element_separator: str = clean_txt[3]

    #-----------Get Segment Terminator
    # Find where GS segment starts to determine ISA length
    gs_identifier: str = f'GS{element_separator}'

    try:
        gs_location: int = clean_txt.index(gs_identifier)
    except ValueError:
        raise ValueError("Fatal: Could not find 'GS' segment after ISA.")

    # If GS starts at position 106, ISA is standard length (106 chars) with terminator at position 105
    # Otherwise, ISA is truncated/variable length, so find terminator after ISA16
    segment_terminator: str = (clean_txt[105] 
                              if gs_location == 106
                              else clean_txt.split(element_separator, 17)[16][1])
        
    #-----------Get X12 Release
    # Get ISA and GS segments
    first_2segments: List[str] = clean_txt.split(segment_terminator, 2)
        
    # Validate we have both ISA and GS segments
    if len(first_2segments) < 2 or not first_2segments[1].strip():
        raise ValueError("Fatal: Could not find 'GS' segment after ISA. EDI may be truncated or incomplete.")

    isa_line: str = first_2segments[0].strip()  # First segment should be ISA
    gs_line: str = first_2segments[1].strip()   # Second segment should be GS

    # Validate GS segment format
    if not gs_line.startswith('GS'):
        raise ValueError(f"Fatal: Expected 'GS' segment but found '{gs_line[:10]}...'")    
    
    # Split segments into individual elements
    # This helps us get the X12 Release
    isa_elements: List[str] = isa_line.split(element_separator)
    gs_elements: List[str] = gs_line.split(element_separator)

    # Validate EDI X12 standard requirements
    if len(isa_elements) != 17:  # ISA + 16 data elements
        raise ValueError(f"Fatal: ISA segment must have exactly 16 data elements, found {len(isa_elements) - 1}.")

    if len(gs_elements) < 9:  # GS + at least 8 data elements
        raise ValueError(f"Fatal: GS segment must have at least 8 data elements, found {len(gs_elements) - 1}.")

    # Determine X12 version from both ISA and GS segments
    x12_release_isa: int = int(isa_elements[12])  # ISA12 contains version
    x12_release_gs: int = int(gs_elements[8])     # GS08 contains version
    
    # Normalize ISA version to match GS format (e.g., 401 -> 4010)
    if x12_release_isa < 10000:
        x12_release_isa = x12_release_isa * 10
    
    # Validate versions match
    if x12_release_isa != x12_release_gs:
        raise ValueError(
            f"Fatal: X12 version mismatch detected. "
            f"ISA12 indicates version {x12_release_isa}, "
            f"but GS08 indicates version {x12_release_gs}. "
            f"EDI document may be malformed or corrupted."
        )
    
    #-----------Get Component Separator
    # Extract Component Separator (also called Compound Separator)
    compound_separator: str = isa_elements[16]
    
    #-----------Get Repetition Separator
    repetition_separator: Optional[str] = isa_elements[11] if x12_release_isa > 4010 else None
    
    
    #-----------Create return dictionary
    delimiters: Dict[str, Optional[str]] = {
        'element': element_separator,
        'segment': segment_terminator,
        'compound': compound_separator,
        'repetition': repetition_separator
    }
    
    return delimiters
