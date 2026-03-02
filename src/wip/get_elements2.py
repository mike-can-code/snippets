from typing import Dict, Optional

def get_delimiters(edi_contents: str) -> Dict[str, Optional[str]]:
    """
    Parses an EDI X12 string to extract its delimiter set, handling both
    standard and truncated ISA segments.

    Args:
        edi_contents: A string containing the EDI X12 data, which may have
                      leading garbage characters.

    Returns:
        A dictionary containing the extracted delimiters.

    Raises:
        ValueError: If the file is too malformed to determine delimiters.
    """
    # 1. Locate and validate the start of the ISA segment
    try:
        isa_start_index = edi_contents.index('ISA')
        edi_clean_contents = edi_contents[isa_start_index:]
    except ValueError:
        raise ValueError("Fatal: Could not find 'ISA' segment in the provided EDI content.")

    # 2. Extract Element Separator (using INDEXING, not slicing)
    if len(edi_clean_contents) < 4:
        raise ValueError("EDI content is too short to contain an element separator.")
    element_separator = edi_clean_contents[3]
    
    # 3. Determine Segment Terminator using the robust hybrid approach
    segment_terminator = None
    if len(edi_clean_contents) >= 106 and edi_clean_contents[106:108] == 'GS':
        segment_terminator = edi_clean_contents[105]  # Standard position
    
    if not segment_terminator:
        try:
            gs_marker = f'GS{element_separator}'
            gs_index = edi_clean_contents.index(gs_marker)
            segment_terminator = edi_clean_contents[gs_index - 1] # Fallback
        except ValueError:
            raise ValueError("Could not determine segment terminator: GS segment not found after truncated ISA.")

    # 4. Split the EDI into ISA and GS segments
    #    The '2' limit is crucial for performance and to avoid issues with other data
    segments = edi_clean_contents.split(segment_terminator, 2)
    
    if len(segments) < 2:
        raise ValueError("Fatal: Could not split EDI into ISA and GS segments.")
        
    isa_elements = segments[0].split(element_separator)
    gs_elements = segments[1].split(element_separator)

    # 5. Validate and extract remaining delimiters
    if len(isa_elements) < 17 or len(gs_elements) < 9:
        raise ValueError("Fatal: ISA or GS segment has an incorrect number of elements.")

    # ISA16 IS the compound separator
    compound_separator = isa_elements[16]
    
    # ISA11 is the repetition separator (check version from GS08)
    repetition_separator_char = isa_elements[11]
    x12_version_code = gs_elements[8]
    is_repetition_sep_used = int(x12_version_code) < 4010
    repetition_separator = repetition_separator_char if is_repetition_sep_used else None

    # 6. Assemble and return the final dictionary
    return {
        'element': element_separator,
        'segment': segment_terminator,
        'compound': compound_separator,
        'repetition': repetition_separator
    }

# --- Sample Usage ---
sample_edi = """
garbage text...
ISA*00*          *00*          *01*SENDERID       *01*RECEIVERID     *240301*1000*^*00501*000000001*0*T*:~GS*FA*SENDER*RECEIVER*240301*1000*1*X*005010~
"""

try:
    delimiters = get_delimiters(sample_edi)
    print("Successfully parsed delimiters:")
    print(delimiters)
except ValueError as e:
    print(f"Error parsing EDI: {e}")
