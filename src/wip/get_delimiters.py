def get_delimiters(edi_dirty_contents: str):
    
    # -------------  Get start of ISA (In case there is leading characters before the "ISA")
    isa_start_location = edi_dirty_contents.find('ISA')
    edi_clean_contents = edi_dirty_contents[isa_start_location:]

    # -------------  Get Element Seperator
    element_seperator = edi_clean_contents[3]

    # -------------  Get Segment Terminator
    # If edi sender truncated blank values then "Segment Terminator" will not be in the correct position
    segment_terminator = (edi_clean_contents[105] 
                          if edi_clean_contents[106:108] == 'GS' 
                          else edi_clean_contents[edi_clean_contents.find('GS' + element_seperator) -1])
    
    # -------------  Get ISA and GS elements
    isa_elements, gs_elements = [_.split(element_seperator) for _ in edi_clean_contents.split(segment_terminator, 2)[:2]]

    # -------------  Get Compount Seperator
    compound_seperator =isa_elements[16]

    # -------------  Get X12 Release
    x12_release = int(gs_elements[8])

    # -------------  Get 
    repetition_seperator = isa_elements[11] if x12_release < 4010 else None

    delimiters = {'element': element_seperator,
                  'segment': segment_terminator,
                  'compound': compound_seperator,
                  'repetition': repetition_seperator
    }
    return delimiters

delimiter: dict = get_delimiters(edi_dirty_contents)
delimiter
