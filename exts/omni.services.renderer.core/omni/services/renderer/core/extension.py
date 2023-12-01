import os


from fastapi.staticfiles import StaticFiles


import carb


import omni.ext

from omni.services.core import main


# As most of the features of our API are implemented by the means of function handlers in the `/services` sub-folder,

# the main duty of our extension entrypoint is to register our Service's `@router` and dictate when its capability

# should be enabled or disabled under the guidance of the User or the dependency system.

from .services.capture import router


# For convenience, let's also reuse the utility methods we already created to handle and format the storage location of

# the captured images so they can be accessed by clients using the server, once API responses are issued from our

# Service:

from .utils import get_captured_image_directory, get_captured_image_path



# Any class derived from `omni.ext.IExt` in the top level module (defined in the `python.module` section of the

# `extension.toml` file) will be instantiated when the extension is enabled, and its `on_startup(ext_id)` method

# will be called. When disabled or when the application is shut down, its `on_shutdown()` will be called.

class ViewportCaptureExtension(omni.ext.IExt):

    """Sample extension illustrating registration of a service."""


    # `ext_id` is the unique identifier of the extension, containing its name and semantic version number. This

    # identifier can be used in conjunction with the Extension Manager to query for additional information, such

    # as the extension's location on the filesystem.

    def on_startup(self, ext_id: str) -> None:

        ext_name = ext_id.split("-")[0]


        # At this point, we register our Service's `router` under the prefix we gave our API using the settings system,

        # to facilitate its configuration and to ensure it is unique from all other extensions we may have enabled:

        url_prefix = carb.settings.get_settings().get_as_string(f"exts/{ext_name}/url_prefix")
        print("url_prefix: ", url_prefix)

        main.register_router(router=router, prefix=url_prefix, tags=["Render Image"],)


        # Proceed to create a temporary directory in the Omniverse application file hierarchy where captured stage

        # images will be stored, until the application is shut down:

        captured_stage_images_directory = get_captured_image_directory()

        if not os.path.exists(captured_stage_images_directory):

            os.makedirs(captured_stage_images_directory)


        # Register this location as a mount, so its content is served by the web server bundled with the Omniverse

        # application instance, thus making the captured image available on the network:

        main.register_mount(

            path=get_captured_image_path(),

            app=StaticFiles(directory=captured_stage_images_directory, html=True),

            name="captured-stage-images",

        )


    def on_shutdown(self) -> None:

        # When disabling the extension or shutting down the instance of the Omniverse application, let's make sure we

        # also deregister our Service's `router` in order to avoid our API being erroneously advertised as present as

        # part of the OpenAPI specification despite our handler function no longer being available:

        main.deregister_router(router=router)

        main.deregister_mount(path=get_captured_image_path())