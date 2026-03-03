import json

def parse_edi_with_multiple_groups(raw_edi_string: str) -> dict:
    """
    Parses a raw EDI string into a structured dictionary, correctly handling
    multiple functional groups (GS/GE) and the transaction sets within them.

    Args:
        raw_edi_string: The complete EDI data as a single string.

    Returns:
        A hierarchical dictionary representing the entire EDI file.
    """
    segments = raw_edi_string.strip().split('\\x15')

    # The top-level structure for the entire interchange
    edi_file = {
        "interchange_header": None,
        "functional_groups": [],  # This will be a list to hold multiple groups
        "interchange_trailer": None
    }

    current_functional_group = None
    current_transaction_set = None

    for segment_str in segments:
        if not segment_str:
            continue

        elements = [elem.strip() for elem in segment_str.split('*')]
        segment_id = elements[0]

        # --- Interchange Level ---
        if segment_id == 'ISA':
            edi_file["interchange_header"] = elements
        elif segment_id == 'IEA':
            edi_file["interchange_trailer"] = elements

        # --- Functional Group Level ---
        elif segment_id == 'GS':
            # A new functional group is starting.
            current_functional_group = {
                "header": elements,
                "transaction_sets": [],
                "trailer": None
            }
        elif segment_id == 'GE':
            # The current functional group is ending.
            if current_functional_group:
                current_functional_group["trailer"] = elements
                edi_file["functional_groups"].append(current_functional_group)
                current_functional_group = None # Reset
        
        # --- Transaction Set Level (within a functional group) ---
        elif segment_id == 'ST':
            # A new transaction set is starting.
            current_transaction_set = {"segments": {}}
            # Add the ST segment
            current_transaction_set["segments"][segment_id] = [elements[1:]]
        elif segment_id == 'SE':
            # The current transaction set is ending.
            if current_transaction_set and current_functional_group:
                current_transaction_set["segments"][segment_id] = [elements[1:]]
                current_functional_group["transaction_sets"].append(current_transaction_set)
                current_transaction_set = None # Reset
        
        # --- Default: Add segment to the current transaction set ---
        elif current_transaction_set:
            if segment_id not in current_transaction_set["segments"]:
                current_transaction_set["segments"][segment_id] = []
            current_transaction_set["segments"][segment_id].append(elements[1:])

    return edi_file



parsed_edi = parse_edi_with_multiple_groups(edi_data_with_multiple_groups)


