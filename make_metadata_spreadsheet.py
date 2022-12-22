""" prototype script showing one method for creating a descriptive metadata spreadsheet
    (matching the Nuxeo spreadsheet template format) for one box of the Klein collection.
    written December 2022 by Noah Geraci

    requires input files downloaded as CSV:
    * Accession list:
        https://docs.google.com/spreadsheets/d/1AT3mwyDwuFbH75yt_DeoGW4drYQfBGnypgT-OcJNcuI/edit#gid=352824156
    * Mapping:
        https://docs.google.com/spreadsheets/d/1-HLaT33pqwvomism1FELssIlWGJAycZzTBvXg11Op8Q/edit#gid=0
        (download "Mapping" and "Fixed values" tabs as separate CSVs)
    * Nuxeo spreadsheet template
        https://docs.google.com/spreadsheets/d/1-HLaT33pqwvomism1FELssIlWGJAycZzTBvXg11Op8Q/edit#gid=0

    This script ignores the "Fields for review" tab of the mapping spreadsheet -- fields such as personal names,
    which will need to be reviewed and verified to add to the metadata, are not included here.

"""

import pandas as pd


def main():

    # read input files
    mapping = pd.read_csv("Klein metadata mapping - Mapping.csv").fillna(0)
    fixed_values = pd.read_csv("Klein metadata mapping - Fixed values.csv")
    accession_list = pd.read_csv(
        "MS381_JayKayKlein_AccessionLists - Photographic Material - New IDs - Sheet1.csv",
        dtype=str).fillna("")
    template = pd.read_csv("Nuxeo Spreadsheet Template - Template.csv")

    # select a box
    # could run this for multiple boxes using a for loop
    box = 1
    box_accession_list = accession_list[accession_list["Box Number"] == str(box)]
    # drop rows that don't have local IDs -- no local ID == already digitized
    box_accession_list = box_accession_list[
        box_accession_list["Local Identifier"] != ""]

    # create empty dataframe with same columns as Nuxeo spreadsheet template
    metadata = pd.DataFrame(columns=template.columns)

    # add mapped values to new dataframe
    for i in mapping.index:
        # bring over unmodified values directly
        if not mapping["Modification"][i]:
            metadata[mapping["Nuxeo Spreadsheet Field"]
                     [i]] = box_accession_list[mapping["Accession List Field"]
                                               [i]]
        else:
            # box number
            if mapping["Accession List Field"][i] == "Box Number":
                metadata[mapping["Nuxeo Spreadsheet Field"]
                         [i]] = box_accession_list[
                             mapping["Accession List Field"][i]].apply(
                                 lambda x: f"Box {x}")

            # place
            elif mapping["Accession List Field"][i] == "City; State; Country":
                metadata["Place 1 Name"] = place_to_lc_style(
                    box_accession_list)

    # fill fixed values
    for i in fixed_values.index:
        metadata[fixed_values["Nuxeo Spreadsheet Field"]
                 [i]] = fixed_values["Value"][i]

    metadata.to_csv("ms381_box_001_metadata_test.csv", index=False)


def place_to_lc_style(dataframe):
    """ clunky attempt to take place names as represented in accession sheet
        and convert them to library of congress headings style
        for example: "Los Angeles", "CA", "USA" --> "Los Angeles (Calif.)"

        if there is no state, or state not found in state dict, simply
        concatenate values in city, state, and country field separated by
        comma and space

        takes pandas dataframe with "City", "State", and "Country" columns,
        returns list of place names

    credit to https://gist.github.com/rogerallen/1583593
    https://github.com/cmharlow/geonames-reconcile/blob/master/lc_parse.py

    """
    state_dict = {
        "AL": "Ala.",
        "AK": "Alaska",
        "AZ": "Ariz.",
        "AR": "Ark.",
        "CA": "Calif.",
        "CO": "Colo.",
        "CT": "Conn.",
        "DE": "Del.",
        "DC": "D.C.",
        "FL": "Fla.",
        "GA": "Ga.",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Ill.",
        "IN": "Ind.",
        "IA": "Iowa",
        "KS": "Kan.",
        "KY": "Ky.",
        "LA": "La.",
        "ME": "Me.",
        "MD": "Md.",
        "MA": "Mass.",
        "MI": "Mich.",
        "MN": "Minn.",
        "MS": "Miss.",
        "MO": "Mo.",
        "MT": "Mont.",
        "NE": "Neb.",
        "NV": "Nev.",
        "NH": "N.H.",
        "NJ": "N.J.",
        "NM": "N.M.",
        "NY": "N.Y.",
        "NC": "N.C.",
        "ND": "N.D.",
        "OH": "Ohio",
        "OK": "Okla.",
        "OR": "Or.",
        "PA": "Pa.",
        "RI": "R.I.",
        "SC": "S.C.",
        "SD": "S.D.",
        "TN": "Tenn.",
        "TX": "Tex.",
        "UT": "Utah",
        "VT": "Vt.",
        "VA": "Va.",
        "WA": "Wash.",
        "WV": "W. Va.",
        "WI": "Wis.",
        "WY": "Wyo.",
        "ON": "Ont.",
        "QC": "Québec",
        "VIC": "Vic.",
        "NSW": "N.S.W."
    }

    lc_name_list = []

    for i in dataframe.index:
        lc_name = None
        if dataframe["City"][i] and dataframe["State"][i]:
            if state_dict.get(dataframe["State"][i]):
                lc_name = f"{dataframe['City'][i]} ({state_dict[dataframe['State'][i]]})"

        if not lc_name:
            names = [
                dataframe[x][i] for x in ["City", "State", "Country"]
                if dataframe[x][i] != ""
            ]
            lc_name = ", ".join(names)
            if lc_name == "USA":
                lc_name = "United States"
        lc_name_list.append(lc_name)

    return lc_name_list


if __name__ == '__main__':
    main()
