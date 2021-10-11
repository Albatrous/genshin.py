from __future__ import annotations

import json
from typing import Any, List, Tuple
from datetime import datetime

from pydantic import Field, validator

from .base import GenshinModel


class MapInfoDetails(GenshinModel):
    slices: List[List[str]]
    origin: Tuple[int, int]
    total_size: Tuple[int, int]
    padding: Tuple[int, int]

    @validator("slices", pre=True)
    def __flatten_slices(cls, v):
        return [[j["url"] for j in i] for i in v]


class MapInfo(GenshinModel):
    id: int
    name: str
    icon: str

    details: MapInfoDetails = Field(galias="detail")

    @validator("details", pre=True)
    def __parse_detail(cls, v):
        return json.loads(v)


class MapNode(GenshinModel):
    id: int
    name: str
    icon: str
    parent_id: int
    depth: int
    node_type: int
    jump_type: int
    jump_target_id: int
    display_priority: int
    children: List[MapNode]
    activity_page_label: int
    area_page_label: List[int]
    is_all_area: bool

    @validator("name")
    def __remove_style(cls, v):
        return v.replace("\xa0", " ")


class MapPoint(GenshinModel):
    id: int
    label_id: int
    x: float = Field(galias="x_pos")
    y: float = Field(galias="y_pos")
    display_state: int

    ctime: datetime
    author: str = Field(galias="author_name")

    @property
    def pos(self) -> Tuple[float, float]:
        return self.x, self.y


class MapLocation(GenshinModel):
    id: int
    name: str
    parent_id: int
    map_id: int

    lx: float = Field(galias="l_x")
    ly: float = Field(galias="l_y")
    rx: float = Field(galias="r_x")
    ry: float = Field(galias="r_y")

    children: List[MapLocation]


MapNode.update_forward_refs()
MapLocation.update_forward_refs()