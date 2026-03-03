def get_collection_of_flatfiles() -> pd.DataFrame:
   
    collected = pd.DataFrame()
    for parent in df_of_davailable_edis_in_daas.Name:
        tmp = get_table_of_available_flatfiles(edi_folder=parent, location= EDI_CONTAINER_LOCATION)
        tmp.insert(0, 'ParentDir', parent)

        collected = pd.concat([collected, tmp])

    return collected

df = get_collection_of_flatfiles()
df['KB_Size'] = df.ByteSize.apply(lambda x: convert_file_size(size=x, from_unit='B', to_unit='KB'))
df['MB_Size'] = df.ByteSize.apply(lambda x: convert_file_size(size=x, from_unit='B', to_unit='MB'))
