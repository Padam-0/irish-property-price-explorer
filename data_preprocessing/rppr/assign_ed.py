"""
For each entry in the geocoded dataset assigns an electoral devision using a
point in polygon algorithm
"""

import numpy as np
import pandas as pd
import json
import matplotlib.path as mplPath
from tqdm import tqdm


def check_polygon(polygon, point):
    # Checks a specific polygon, returns True of the point is contained

    path = mplPath.Path(polygon)

    inside = path.contains_point(point)

    return inside


def find_ed(data, latitude, longitude):
    # For a specific point, loops through all polygons and checks each one.
    # Stops when a match is found and returns the electoral district name

    point = ([longitude, latitude])

    for feature in data['features']:

        polygon = np.array(feature['geometry']['coordinates'][0])
        if len(polygon) == 1:
            polygon = polygon[0]
            inside = check_polygon(polygon, point)
        elif len(polygon) <= 10:
            for i in range(len(polygon)):
                subpolygon = polygon[i]
                inside = check_polygon(subpolygon, point)
                if inside == 1:
                    break
        else:
            inside = check_polygon(polygon, point)

        if inside == 1:
            return feature['properties']['NAME_TAG']

    return None


def main():
    with open('eds.geojson') as f:
        data = json.load(f)

    df = pd.read_csv("geocoded_data.csv", encoding='latin1', index_col=0)
    tqdm.pandas(desc="Progress")

    df['ed'] = df.progress_apply(lambda row: find_ed(
        data, row['latitude'], row['longitude']), axis=1)

    df.to_csv("geocoded_data_with_ed.csv")


if __name__ == '__main__':
    main()
