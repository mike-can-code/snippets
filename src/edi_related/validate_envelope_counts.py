def validate_envelope_counts():
    isa_marker = clean_contents[:4]
    gs_marker = delimiter['segment'] + 'GS' + delimiter['element']
    st_marker = delimiter['segment'] + 'ST' + delimiter['element']
    se_marker = delimiter['segment'] + 'SE' + delimiter['element']
    ge_marker = delimiter['segment'] + 'GE' + delimiter['element']
    iea_marker = delimiter['segment'] + 'IEA' + delimiter['element']

    # If these are not equal generate an error
    clean_contents.count(isa_marker) == clean_contents.count(iea_marker)
    clean_contents.count(gs_marker) == clean_contents.count(ge_marker)
    clean_contents.count(st_marker) == clean_contents.count(se_marker)
