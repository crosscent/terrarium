"""itis.py

Before running the script, please head to itis.gov and get the newest plant
checklist in sqlite format and replace /data/plants/itis_plant_cheklist.sqlite
with the newest content.
"""

import sqlite3

from terrarium.plants.models import Plant
from terrarium.plants.models import Taxonomy

def ETL_taxonomy(row):
    """
    ETL on each row extracted from SQLite3 for ``plants.Taxonomy``
    """

    model_dict = {'name': row[1],
                  'level': row[0]}
    
    taxonomy, created = Taxonomy.objects.get_or_create(**model_dict)
    return taxonomy

def ETL_plant(row, parent_id=None):
    """
    ETL on each row extracted from SQLite3 for ``plants.Plant``
    """

    # Assuming that each of the complete names are unique, and that parents do
    # not come after child

    # simply set this to a table could speed the process up, but not all users
    # have the same Taxonomy id. Perhaps caching it using another function and
    # calling that variable could work.
    taxonomy = Taxonomy.objects.get(level=row[1])

    if row[2] == 'accepted' or row[2] == 'valid':
        accepted = True
    else:
        accepted = False

    if row[6] == 'accepted' or row[6] == 'valid':
        parent_accepted = True
    else:
        parent_accepted = False
    parent = None
    if row[4]:
        try:
            parent = Plant.objects.get(scientific_name=row[4],
                                       taxonomy__level=row[5],
                                       accepted=parent_accepted)
        except Plant.DoesNotExist:
            pass

    model_dict = {"scientific_name": row[0],
                  "taxonomy": taxonomy,
                  "accepted": accepted,
                  "unaccepted_reason": row[3],
                  "parent": parent}
    plant, created = Plant.objects.get_or_create(**model_dict)
    return plant

def update():
    """
    Use the complete listing provided in the .sqlite file
    """
    conn = sqlite3.connect("data/plants/itis_plant_checklist.sqlite")
    c = conn.cursor()

    # iterate through taxonomic_units and parse it
    # kingdom_id == 3 is where all the plant data is
    for row in c.execute("""SELECT rank_id, rank_name
                             FROM taxon_unit_types
                             WHERE kingdom_id=3"""):
        print ETL_taxonomy(row)

    for row in c.execute("""SELECT s.complete_name, s.rank_id,
                                   s.name_usage, s.unaccept_reason,
                                   p.complete_name, p.rank_id,
                                   p.name_usage
                                FROM taxonomic_units s
                                    LEFT JOIN taxonomic_units p
                                        ON s.parent_tsn = p.tsn
                                WHERE s.kingdom_id=3
                                ORDER BY s.tsn ASC"""):
        print ETL_plant(row)
