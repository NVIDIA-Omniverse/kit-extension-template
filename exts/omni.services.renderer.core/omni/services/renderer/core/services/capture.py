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

# Define a model to handle the parsing of incoming requests.
class RenderRequestModel(BaseModel):
    """Model describing the request to capture a viewport as an image."""
    usd_path: str
    output_path: str
    entities: Entities
    implants: Implants
    render_views: RenderViews
    render_settings: RenderSettings


# Define a model to handle the delivery of responses back to clients.
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
