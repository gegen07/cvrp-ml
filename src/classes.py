import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Union

from dacite import from_dict
import pandas as pd
import geopandas as gpd
import h3


class JSONDataclassMixin:
    """Mixin for adding JSON file capabilities to Python dataclasses."""

    @classmethod
    def from_file(cls, path: Union[Path, str]) -> "JSONDataclassMixin":
        """Load dataclass instance from provided file path."""

        with open(path) as f:
            data = json.load(f)

        return from_dict(cls, data)

    def to_file(self, path: Union[Path, str]) -> None:
        """Save dataclass instance to provided file path."""

        with open(path, "w") as f:
            json.dump(asdict(self), f)

        return


@dataclass(unsafe_hash=True)
class Point:
    """Point in earth. Assumes a geodesical projection."""

    lng: float
    """Longitude (x axis)."""

    lat: float
    """Latitude (y axis)."""


@dataclass(unsafe_hash=True)
class Delivery:
    """A delivery request."""

    id: str
    """Unique id."""

    point: Point
    """Delivery location."""

    size: int
    """Size it occupies in the vehicle (considered 1-D for simplicity)."""

@dataclass
class CVRPSeries(JSONDataclassMixin):
    name: str
    """Unique name of this instance."""

    region: str
    """Region name."""

    origin: Point
    """Location of the origin hub."""

    vehicle_capacity: int
    """Maximum sum of sizes per vehicle allowed in the solution."""

    deliveries: List[Delivery]
    """List of deliveries to be solved."""

    def to_gdf(self) -> gpd.GeoDataFrame:
        """Converts the deliveries to a GeoDataFrame."""

        df = pd.json_normalize([asdict(d) for d in self.deliveries],max_level=1)
        df.columns = ["id", "size", "lat", "long",]
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lat, df.long))
        gdf.crs = "EPSG:4326"


        gdf["h3_boundary"] = gdf.apply(lambda x: h3.geo_to_h3(x["long"], x["lat"], 6), axis=1)
        gdf["h3_center"] = gdf.apply(lambda x: h3.h3_to_geo(x["h3_boundary"]), axis=1)

        return gdf


@dataclass
class CVRPInstance(JSONDataclassMixin):
    name: str
    """Unique name of this instance."""

    region: str
    """Region name."""

    origin: Point
    """Location of the origin hub."""

    vehicle_capacity: int
    """Maximum sum of sizes per vehicle allowed in the solution."""

    deliveries: List[Delivery]
    """List of deliveries to be solved."""


@dataclass
class CVRPSolutionVehicle:

    origin: Point
    """Location of the origin hub."""

    deliveries: List[Delivery]
    """Ordered list of deliveries from the vehicle."""

    @property
    def circuit(self) -> List[Point]:
        return (
            [self.origin] + [d.point for d in self.deliveries] + [self.origin]
        )

    @property
    def occupation(self) -> int:
        return sum([d.size for d in self.deliveries])


@dataclass
class CVRPSolution(JSONDataclassMixin):
    name: str
    vehicles: List[CVRPSolutionVehicle]

    @property
    def deliveries(self):
        return [d for v in self.vehicles for d in v.deliveries]