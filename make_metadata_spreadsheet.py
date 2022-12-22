import pandas as pd


def main():

    # read input files
    mapping = pd.read_csv("Klein metadata mapping - Mapping.csv").fillna(0)
    fixed_values = pd.read_csv("Klein metadata mapping - Fixed values.csv")
    accession_list = pd.read_csv(
        "MS381_JayKayKlein_AccessionLists - Photographic Material - New IDs - Sheet1.csv",
        dtype=str).fillna("")
    template = pd.read_csv("Nuxeo Spreadsheet Template - Template.csv")

    # select a single box
    box = 1
    box_accession_list = accession_list[accession_list["Box Number"] == str(1)]
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
            elif mapping["Accession List Field"][i] == "Place":
                metadata[mapping["Nuxeo Spreadsheet Field"][i]] = 

    # fill fixed values
    for i in fixed_values.index:
        metadata[fixed_values["Nuxeo Spreadsheet Field"]
                 [i]] = fixed_values["Value"][i]

    metadata.to_csv("test.csv", index=False)


def place_to_lc_style(dataframe):
    """ takes place names as represented in accession sheet
        and attempts to convert them to library of congress headings style
        for example: "Los Angeles", "CA", "USA" --> "Los Angeles (Calif.)"

    credit = https://gist.github.com/rogerallen/1583593
    https://github.com/cmharlow/geonames-reconcile/blob/master/lc_parse.py

    UNFINISHED

    """
    lc_name = None 

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
        "WY": "Wyo."
    }

    if city and state:
        if country == "USA":
            lc_name = f"{city} ({state_dict[state]})"

    return lc_name


if __name__ == '__main__':
    main()
