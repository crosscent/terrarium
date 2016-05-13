"""update.py

Before running the script, please head to plants.usda.gov to get the newest
plant checklist and replace /data/plants/usda_plant_checklist.csv with the
newest file content.
"""

import csv
import requests

def ETL():
    """Parses the dictionary into a suitable format
    """
    pass

def unique_family(data):
    """A list of unique families in the USDA data provided
    
    Iterates through the DictReader for the family names, and returns a list of
    names

    Args:
        A DictReader instance of the usda plant checklist

    Returns:
        A list of strings containing all the unique family names in the list
    """
    unique_family = []
    for line in data:
        if line["Family"] not in unique_family:
            unique_family.append(line["Family"])
    return unique_family

def group_by_family(data):
    """Group all species by their family name

    Iterates through the DictReader, and puts each species under their
    respective family in a dictionary

    Args:
        A DictReader instance of the usda plant checklist

    Returns:
        A dict`ioanry with ``family`` as keys, and a list of
        ``scientific name`` as their values
    """
    family = {}
    for line in data:
        if line["Family"] not in family:
            family[line["Family"]] = []
        family[line["Family"]].append(line["Scientific Name with Author"])
    return family

def update():
    """Parses the USDA plant list provided by USDA
    """
    csv_file = open('data/plants/usda_plant_checklist.csv')
    reader = csv.reader(csv_file)
    header = reader.next()
    data = list(csv.DictReader(csv_file, header))
