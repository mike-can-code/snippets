import pandas as pd

# -------------  Constants
EDI_CONTAINER_LOCATION = 's3://advana-data-zone/bronze/dla_daas/edi/'

# -------------  Get directory contents as dataframe
def get_dir_list(*, location: str) -> pd.DataFrame:
    '''
    Return Sample:

        |------------------------------------------------------|------------|----------|-------------------------------|
        | Path                                                 | Name       | ByteSize | ModificationTime              |
        |------------------------------------------------------|------------|----------|-------------------------------|
        | s3://advana-data-zone/bronze/dla_daas/edi/dteb_214a/ | dteb_214a/ |     0    | 2026-02-27T16:19:27.714+00:00 |
        | s3://advana-data-zone/bronze/dla_daas/edi/dteb_315a/ | dteb_315a/ |     0    | 2026-02-27T16:19:27.714+00:00 |    
    
    '''

    # %fs ls $location does not work
    # Use the format below instead
    dir_list: list = dbutils.fs.ls(location)

    dir_list_df = pd.DataFrame(dir_list, columns= ['Path', 'Name', 'ByteSize', 'ModificationTime'])
    dir_list_df['ModificationTime'] = pd.to_datetime(dir_list_df['ModificationTime'], unit='ms')
    dir_list_df = dir_list_df.sort_values(['Path'])

    return dir_list_df


# ------- Get available edi types by (number and alpha) as list
def get_list_of_available_edis(*, location) -> list:
    '''
    Return Sample:

        ['180M', '214A', '315A', '315B', '315N', '511M', '511R', '527R', '856A']

    '''

    dir_list_df: pd.DataFrame = get_dir_list(location=location)
    list_of_unique_edis: list = list(set(dir_list_df.Name.str.split('_').str[-1].str
            .replace('/', '')
            .replace('name}', '')
            .replace('tmp', '')
            .replace('failed', '')
            .replace('completed', '')
            .replace('archive', '')
            .replace('staging', '')
            .replace('backlog', '')
            .replace('tracking', '')
            .replace('december2025', '')
            .replace('856rtemp', '856r (temp)')
            .str.upper()
    ))

    list_of_unique_edis = sorted([_ for _ in list_of_unique_edis if _])   
    return list_of_unique_edis

# -------------  Get available edi flatfiles as dataframe
def get_table_of_available_flatfiles(*, edi_folder: str, location: str) -> pd.DataFrame:
    edi_folder = edi_folder if edi_folder[-1] == '/' else edi_folder + '/'
    location+= edi_folder

    print(edi_folder)
    return get_dir_list(location = location)

# -------------  Prepopulate variables
list_of_available_edis_in_daas: list = get_list_of_available_edis(location= EDI_CONTAINER_LOCATION)
df_of_davailable_edis_in_daas:  pd.DataFrame = get_dir_list(location= EDI_CONTAINER_LOCATION)

# -------------  Parse owner, EDI number and EDI alpaha
df_of_davailable_edis_in_daas['Owner'] =  ['DLA' if 'dedso' in _ else 'DTEB' if 'dteb' in _ else '' for _ in df_of_davailable_edis_in_daas.Name]
df_of_davailable_edis_in_daas['edi_nbr'] = [_.split('dteb_')[-1].split('dedso_')[-1].split('_')[0].replace('temp', '')[:-1][:3] 
                                             if _.split('dteb_')[-1].split('dedso_')[-1].split('_')[0].replace('temp', '')[:-1][:3].isdigit()
                                             else ''
                                             for _ in df_of_davailable_edis_in_daas.Name]
                                              
df_of_davailable_edis_in_daas['edi_alpha'] = [_.split('dteb_')[-1].split('dedso_')[-1].split('_')[0].replace('temp', '')[:-1][-1] .upper()
                                             if _.split('dteb_')[-1].split('dedso_')[-1].split('_')[0].replace('temp', '')[:-1][:3].isdigit()
                                             else ''
                                             for _ in df_of_davailable_edis_in_daas.Name]


# -------------  Display on screen
print(f'\nAVAILABLE EDIs: {list_of_available_edis_in_daas}\n')

print('TABLE OF FOLDERS CONTAINING EDIs:')
display(df_of_davailable_edis_in_daas)
