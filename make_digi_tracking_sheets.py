""" using existing accession spreadsheet (with new IDs)
    create one CSV spreadsheet per box of negatives in the Klein collection, with the following fields:

        "Box Number", "Local Identifier", "Label", "ID", "Strip/Row Number", 
        "Image Number", "Digitized in 2017 pilot"

these sheets will be uploaded to Google Sheets and used by Digitization Services to support imaging
workflows
"""

import pandas as pd


def main():
    # fiddling with data types
    input_columns = [
        "Box Number", "Binder Number", "Label", "ID", "Section Number",
        "Strip/Row Number", "Image Number", "Local Identifier",
        "Legacy Unique ID", "Digitized in 2017 pilot", "Is negative",
        "Convention / Event", "Year", "City", "State", "Country",
        "Central Figure First name", "Central Figure Last name",
        "Notable Figure First name", "Notable Figure Last name", "Description",
        "Format \n(35mm)"
    ]
    dtype_dict = {col: str for col in input_columns}
    for i in ["Digitized in 2017 pilot", "Is negative"]:
        dtype_dict[i] = bool

    # read accession list file with new IDs
    accession_list = pd.read_csv(
        "MS381_JayKayKlein_AccessionLists - Photographic Material - New IDs.csv",
        dtype=dtype_dict)

    # populate new dataframe with rows representing negatives
    box_list_data = accession_list[accession_list["Is negative"] == True]

    # retain only select columns
    box_list_data = box_list_data[[
        "Box Number", "Local Identifier", "Label", "ID", "Strip/Row Number",
        "Image Number", "Digitized in 2017 pilot"
    ]]

    # rename "ID" column to "Film Roll ID"
    box_list_data.rename(columns={"ID": "Film Roll ID"}, inplace=True)

    # add value "ALREADY DIGITIZED" in "Local Identifier" column, for digitized items that do not have new local ID
    # per Mark request to remind students not to scan these / not attempt to fill in blanks
    box_list_data["Local Identifier"] = box_list_data[
        "Local Identifier"].fillna("ALREADY DIGITIZED")

    # write out one csv file per box, 1-11
    for i in range(1, 12):
        box_sheet = box_list_data[box_list_data["Box Number"] == str(
            i)].fillna("")
        box_sheet.to_csv(
            f"box_lists/ms381_box_{str(i).zfill(3)}_digi_list.csv",
            index=False)

if __name__ == '__main__':
    main()
