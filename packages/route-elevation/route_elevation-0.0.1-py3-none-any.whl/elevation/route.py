import os
from typing import Optional

import googlemaps
from googlemaps.directions import directions
from googlemaps.elevation import elevation_along_path


class Route:
    _client: googlemaps.Client
    _start: str
    _end: str
    _route: dict
    _elevations: list[dict]

    def __init__(self, start: str, end: str, *, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ["GOOGLE_MAPS_API_KEY"]
        if api_key is None:
            raise ValueError("A Google Maps API key is required.")
        self._client = googlemaps.Client(key=api_key)
        self._start = start
        self._end = end

        self._get_route()
        self._get_elevations()

    def __array__(self):
        import numpy as np

        return np.array(
            [
                [
                    point["distance"],
                    point["elevation"],
                ]
                for point in self._elevations
            ]
        )

    def _get_route(self):
        directions_result = directions(
            self._client,
            self._start,
            self._end,
            mode="driving",
        )
        self._route = directions_result[0]["legs"][0]

    def _get_elevations(self):
        ret = []
        distance = 0
        for step_index, step in enumerate(self._route["steps"]):
            step_polyline = step["polyline"]["points"]
            step_elevations = elevation_along_path(
                self._client,
                step_polyline,
                samples=512,
            )
            for elevation_index, elevation in enumerate(step_elevations):
                distance += step["distance"]["value"] / len(step_elevations)
                ret.append(
                    {
                        "location": elevation["location"],
                        "elevation": elevation["elevation"],
                        "distance": distance,
                    }
                )
        self._elevations = ret

    def plot(self):
        import matplotlib.pyplot as plt

        plt.plot(self.__array__()[:, 0], self.__array__()[:, 1])
        plt.show()

    def to_array(self):
        return self.__array__()
