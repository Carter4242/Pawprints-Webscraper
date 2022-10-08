"""
PAWPRINTS-WEBSCRAPER

This module formats the raw results string first into a json, and then into a list of every petition.

Author: Carter4242
https://github.com/Carter4242
"""


from datetime import datetime, date
from dataclasses import dataclass
import json


@dataclass
class Petition:
    """
    id: int - unique id for petition, matches url
    signatures: int - number of signatures petition received
    response: bool - wether or not petition has a response - marked as true if there is any response
    updates: bool - wether or not petition has updates
    charged: bool - wether or not the petition has been charged to be dealt with by someone
    timestamp: date - the day M/D/Y the petition was created
    expires: date - the day M/D/Y the petition expired
    title: str - the title of the petition
    author: str - the author of the petition
    # tags: str - the tags of the petition (NOT CURRENTLY RECORDED)
    """
    id: int
    signatures: int
    response: bool
    updates: bool
    charged: bool
    timestamp: date
    expires: date
    title: str
    author: str
    # tags: str


def formatPetitions(result: str) -> list:
    """
    Formats the result of the all command. First into a json. Then into a list.

    :param result: the unformatted all string
    :type result: str
    :return: the formatted completed petition list
    :rtype: list
    """

    print("\nRemoving start and end formatting")
    # Cuts the starting '{"petitions": [' and the ending mapping section.
    result = result[14:result.find(', \"map\": {')]

    print("Loading json")
    data = json.loads(result)  # Loads the result into a list of dictionaries
    print ("Length of data: " + str(len(data)))

    print("\nLoading Petitions List")
    petitions = []
    for i in data:
        # Converts the received dates that look like "October 08, 2022" into datetime.date(2022, 10, 8)
        made = datetime.date(datetime.strptime(i['timestamp'],'%B %d, %Y'))
        expired = datetime.date(datetime.strptime(i['expires'],'%B %d, %Y'))
        updated = False  # Default, changed if it has been
        responded = bool(i['response'])  # Default, changed to true if there is an update, but no response.
        if i['updates'] != []:
            updated = True
            responded = True  # If the petition has received an update, than there has a been a response of some kind.
        petitions.append(Petition(
            id=int(i['id']),  # str -> int
            signatures=int(i['signatures']),  # str -> int
            response=responded,  # str -> bool (above)
            updates=updated,  # str -> bool (above)
            charged=bool(i['in_progress']),  # str -> bool
            timestamp= made,  # str -> datetime.date (above)
            expires= expired,  # str -> datetime.date (above)
            title=i["title"],  # str
            author=i['author'],  # str
            # tags=i['tags'],  # str
            ))

    print("Finished Loading Petitions List")
    print("Length of petitions: " + str(len(petitions)))  # This better match the length of data.

    return petitions
