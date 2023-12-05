from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from omni.services.core import routers
from omni.services.renderer.core.utils import (
    capture_viewport
)
from omni.services.renderer.core.models import (
    Entities,
    Implants,
    RenderViews,
    RenderSettings
)


router = routers.ServiceAPIRouter()



# Let's define a model to handle the parsing of incoming requests.

#

# Using `pydantic` to handle data-parsing duties makes it less cumbersome for us to do express types, default values,

# minimum/maximum values, etc. while also taking care of documenting input and output properties of our service using

# the OpenAPI specification format.

class RenderRequestModel(BaseModel):

    """Model describing the request to capture a viewport as an image."""
    usd_path: str
    output_path: str
    entities: Entities
    implants: Implants
    render_views: RenderViews
    render_settings: RenderSettings

    
    # entities: Entities = Field(
    #     ..., # the ... is a placeholder for the default value
    #     title="Entities",
    #     description="Dictionary of entities to and their prim paths."
    # )

    # implants: Implants = Field(
    #     ..., # the ... is a placeholder for the default value
    #     title="Implants",
    #     description="List to apply to specific entities.",
    # )

    # render_views: RenderViews = Field(
    #     ..., # the ... is a placeholder for the default value
    #     title="Render Views",
    #     description="List of render views to capture as each implant is applied.",
    # )

    # render_settings: RenderSettings = Field(
    #     ..., # the ... is a placeholder for the default value
    #     title="Render Settings",
    #     description="Unsure what will be in this.",
    # )

    # usd_stage_path: str = Field(

    #     ...,

    #     title="Path of the USD stage for which to capture an image",

    #     description="Location where the USD stage to capture can be found.",

    # )

    # If required, add additional capture response options in subsequent iterations.

    # [...]


# We will also define a model to handle the delivery of responses back to clients.

#

# Just like the model used to handle incoming requests, the model to deliver responses will not only help define

# default values of response parameters, but also in documenting the values clients can expect using the OpenAPI

# specification format.

class RenderResponseModel(BaseModel):

    """Model describing the response to the request to capture a viewport as an image."""


    success: bool = Field(

        default=False,

        title="Capture status",

        description="Status of the capture of the given USD stage.",

    )

    captured_image_path: Optional[str] = Field(

        default=None,

        title="Captured image path",

        description="Path of the captured image, hosted on the current server.",

    )

    error_message: Optional[str] = Field(

        default=None,

        title="Error message",

        description="Optional error message in case the operation was not successful.",

    )



# Using the `@router` annotation, we'll tag our `capture` function handler to document the responses and path of the

# API, once again using the OpenAPI specification format.

@router.post(

    path="/capture",

    summary="Capture a given USD stage",

    description="Capture a given USD stage as an image.",

    response_model=RenderResponseModel,

)

async def capture(request: RenderRequestModel,) -> RenderResponseModel:
    # Unpack the request parameters into variables to pass to the `capture_viewport` function
    entities = Entities.load(request.entities)
    implants = Implants.load(request.implants)
    render_views = RenderViews.load(request.render_views)
    render_settings = RenderSettings.load(request.render_settings)

    success, captured_image_path, error_message = await capture_viewport( # await render_scene (
        usd_stage_path=request.usd_stage_path,
        # output_path=request.output_path,
        # entitites=entities,
        # implants=implants,
        # render_views=render_views,
        # render_settings=render_settings,       
    )

    return RenderResponseModel(

        success=success,

        captured_image_path=captured_image_path,

        error_message=error_message,

    )
