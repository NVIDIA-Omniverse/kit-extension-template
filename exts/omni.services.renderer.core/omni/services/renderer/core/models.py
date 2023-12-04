from pydantic import dataclasses


@dataclasses.dataclass
class Entity:
        entity_id: str
        prim_path: str

@dataclasses.dataclass
class Implant:
    name: str
    usd_path: str
    prop_type: str
    transforms: list

@dataclasses.dataclass
class RenderView:
    camera_path: str
    entity_id: str
    visibility: str

@dataclasses.dataclass
class RenderSetting:
    resolution: (int, int)

class Payload_Base:
    @classmethod
    def load(self):
        raise NotImplementedError

class Entities(Payload_Base):

    @classmethod
    def load(self, entities):
        """
        Description:
        Load a list of entities from a JSON file.
        Args:
        entities (dict): List of entities to load.
        Returns:
        list[Entity]: List of entities loaded from the JSON file.
        """
        return [
            Entity(entity_id, prim_path) 
            for entity_id, prim_path 
            in entities.items()
        ]

class Implants(Payload_Base):
    
    @classmethod
    def load(self, implants):
        return [
            Implant(name, usd_path, prop_type, transforms)
            for name, usd_path, prop_type, transforms
            in implants
        ]

class RenderViews(Payload_Base):
    def __init__(self, camera_path, entity_id, visibility):
        self.camera_path = camera_path
        self.entity_id = entity_id
        self.visibility = visibility
    
    @classmethod
    def load(self, render_views):
        return [
            RenderView(camera_path, entity_id, visibility)
            for camera_path, entity_id, visibility
            in render_views
        ]

class RenderSettings(Payload_Base):
     def __init__(self, resolution) -> None:
          self.resolution = resolution
     
     @classmethod
     def load(self, render_settings):
        return [
            RenderSetting(resolution)
            for resolution
            in render_settings
        ]