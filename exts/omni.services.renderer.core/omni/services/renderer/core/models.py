from typing import List
from pydantic.dataclasses import dataclass

@dataclass
class Entity:
    entity_id: int
    entity_type: str
    prim_path: str

@dataclass
class Implant:
    entity_id: int
    prop_type: str
    dataset_path: str
    dataset_key: str


@dataclass
class RenderView:
    camera_id: str
    entity_id: int
    visibility: str

@dataclass
class Entities:
    entities: List[Entity]

@dataclass
class Implants:
    implants: List[Implant]

@dataclass
class RenderViews:
    views: List[RenderView]

@dataclass
class RenderSettings:
    img_w: int
    img_h: int
    transparency: bool
    color_mode: str
    samples: int