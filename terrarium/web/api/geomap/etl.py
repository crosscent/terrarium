def nominatim_to_place(data):
    """ETL for Nominatim data to PlaceSerializer

    This function extracts all the required variables for PlaceSerializer from
    data returned from Nominatim

    Args:
        data - Data from Nominatim

    Return:
        A dictionary in the proper PlaceSerializer format
    """
    display_name = data.get('display_name', None)
    place_id = data.get('place_id', None)
    osm_id = data.get('osm_id', None)
    osm_type_dict = {'node': 1,
                     'way': 2,
                     'relation': 3}
    if data.get('osm_type', None) and data['osm_type'] in osm_type_dict:
        osm_type = osm_type_dict[data['osm_type']]
    else:
         osm_type = 0

    if 'polygonpoints' in data:
        polygons = [{'polygon': {'type': 'MultiPolygon', 'coordinates': [[data.get('polygonpoints', None)]]}}]
        # make sure that the coordinates provided by Nominatim are floats and
        # not strings
        coordinates = polygons[0]['polygon']['coordinates'][0][0]
        for i in xrange(len(coordinates)):
            coordinates[i][0] = float(coordinates[i][0])
            coordinates[i][1] = float(coordinates[i][1])
            
    else:
        polygons = []

    return {'display_name': display_name,
            'place_id': place_id, 
            'osm_id': osm_id,
            'osm_type': osm_type,
            'polygons': polygons
            }
