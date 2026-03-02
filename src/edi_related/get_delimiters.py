from typing import Dict, Optional

def get_delimiters(edi_dirty_contents: str) -> Dict[str, Optional[str]]:

    # -------------  Get start of ISA (In case there is leading characters before the "ISA")
    try:
        isa_start_index = edi_contents.index('ISA')
        edi_clean_contents = edi_contents[isa_start_index:]
    except ValueError:
        raise ValueError("Fatal: Could not find 'ISA' segment in the provided EDI content.")

    # -------------  Get Element Separator 
    # Element Separator is in position 4 (python is zero based so we use 3)
    element_separator = edi_clean_contents[3]


    # -------------  Get Segment Terminator
    gs_location = f'GS{element_separator}'
    gs_location = edi_clean_contents.index(gs_location)
    segment_terminator = (edi_clean_contents[105] 
                         if gs_index == 106
                         else edi_clean_contents.split(element_separator, 17)[16][1])

    # -------------  Get clean ISA and GS elements
    isa_line, gs_line = [_.strip() for _ in edi_clean_contents.split(segment_seperator, 2)[:2]]
    isa_elements = isa_line.split(element_separator)
    gs_elements = gs_line.split(element_separator)

   # -------------  Get Compount Seperator
    compound_seperator = isa_elements[16]
    
   # -------------  Get X12 Release
    x12_release = int(gs_elements[8])


    # -------------  Get Repetition Seperator
    repetition_seperator = isa_elements[11] if x12_release > 4010 else None

    # -------------  Create the delimiter dictionary
    delimiters = {'element': element_separator,
                  'segment': segment_terminator,
                  'compound': compound_seperator,
                  'repetition': repetition_seperator
    }
    
    return delimiters
