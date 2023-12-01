from typing import Optional
from pydantic import BaseModel, Field
from omni.services.core import routers
from omni.services.renderer.core.utils import (
    capture_viewport
)


router = routers.ServiceAPIRouter()


class RenderModel(BaseModel):

    """Model describing the request to render an image."""


    usd_stage_path: str = Field(

        ...,

        title="Path of the USD stage for which to capture an image",

        description="Location where the USD stage to capture can be found.",

    )

    implants_path: str = Field(
        ...,
        title="Path of the implants file",
        description="Location where the implants file can be found.",
    )  


class RendererResponseModel(BaseModel):

    """Model describing the response to the request to capture a viewport as an image."""


    success: bool = Field(

        default=False,

        title="Capture status",

        description="Status of the capture of the given USD stage.",

    )

    captured_image_path: [str] = Field(

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

    response_model=RendererResponseModel,

)

async def capture(request: RenderModel,) -> RendererResponseModel:

    success, captured_image_path, error_message = await capture_viewport(usd_stage_path=request.usd_stage_path)

    return RendererResponseModel(

        success=success,

        captured_image_path=captured_image_path,

        error_message=error_message,

    )
