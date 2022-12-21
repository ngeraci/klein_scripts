""" creates new "Local Identifier" column for Jay Kay Klein photographs accession CSV,
    writes out updated CSV to new file for use in digitization project
    new ID format:
        * "curivsc" = SCUA prefix
        * MS381 = collection number
        * object number: numbered continuously & sequentially
          using the row number (index + 1), zero-padded to six digits
        * component number: 1, zero-padded to four digits
          (hard-coded as 1 because these images are all simple,
          not complex/multi-page digital objects)
    renames old ID column from "Unique ID" to "Legacy Unique ID"
    input filename: "MS381_JayKayKlein_AccessionLists - Photographic Material.csv"
    new spreadsheet filename: "MS381_JayKayKlein_AccessionLists - Photographic Material - New IDs.csv"
        (downloaded from "Photographic Material" tab of
        https://docs.google.com/spreadsheets/d/1akxRbbcHRfqHdqgWvHgkMQwdVYMMRgQO8YFgxEilooE/edit#gid=916881284)
"""

import pandas as pd


def main():

    # read accession list file
    accession_list = pd.read_csv(
        "MS381_JayKayKlein_AccessionLists - Photographic Material.csv",
        dtype="str").fillna("")

    # rename column containing old ID
    accession_list.rename(columns={"Unique ID": "Legacy Unique ID"},
                          inplace=True)

    # items with these labels are already digitized
    pilot_series = [
        "PittCon 60", "ChiCon 62", "DisCon 63", "Tricon 66", "Nycon III",
        "BayCon 68", "St Louis Con 69", "Noreascon 71"
    ]

    # add True/False column "Digitized in 2017 pilot" - populate True if item is in one of the listed labels
    digitized = accession_list["Label"].isin(pilot_series)
    accession_list.insert(8, "Digitized in 2017 pilot", digitized)

    # add True/False column "Negative" to indicate whether a row represents a negative
    negatives = accession_list["Format \n(35mm)"].str.startswith("negatives")
    accession_list.insert(9, "Is negative", negatives)

    # populate new "Local Identifier" column
    ## "curivsc" = SCUA prefix
    ## MS381 = collection number
    ## str(counter).zfill(6) = object number: numbered sequentially, skipping those already 
    ## digitized, zero-padded to six digits
    ## str(1).zfill(4) = object component number: 1, zero-padded to four digits 
    ## (hard-coded as 1 because these images are all simple,
    ### not complex/multi-page digital objects)

    # build list of new IDs. Items already digitized or that are not negatives,
    # do not get a new ID and instead get the value "None"
    counter = 1
    new_id_column = []
    for i in accession_list.index:
        if accession_list["Digitized in 2017 pilot"][
                i] == False and accession_list["Is negative"][i] == True:
            new_id_column.append(
                f"curivsc_ms381_{str(counter).zfill(6)}_{str(1).zfill(4)}")
            counter += 1
        else:
            new_id_column.append(None)

    # insert new values immediately to the left of "Legacy Unique ID"
    accession_list.insert(7, "Local Identifier", new_id_column)
    accession_list
    # write out to new CSV file
    accession_list.to_csv(
        "MS381_JayKayKlein_AccessionLists - Photographic Material - New IDs.csv",
        index=False)

if __name__ == '__main__':
    main()
