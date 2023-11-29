import carb

import omni.ext


from omni.services.core import main


# As most of the features of our API are implemented by the means of function handlers in the `/services` sub-folder,

# the main duty of our extension entrypoint is to register our Service's `@router` and dictate when its capability

# should be enabled or disabled under the guidance of the User or the dependency system.

from .services.capture import router



# Any class derived from `omni.ext.IExt` in the top level module (defined in the `python.module` section of the

# `extension.toml` file) will be instantiated when the extension is enabled, and its `on_startup(ext_id)` method

# will be called. When disabled or when the application is shut down, its `on_shutdown()` will be called.

class ViewportCaptureCoreExtension(omni.ext.IExt):

    """Sample extension illustrating registration of a service."""


    # `ext_id` is the unique identifier of the extension, containing its name and semantic version number. This

    # identifier can be used in conjunction with the Extension Manager to query for additional information, such

    # as the extension's location on the filesystem.

    def on_startup(self, ext_id: str) -> None:

        ext_name = ext_id.split("-")[0]

        carb.log_info("ViewportCaptureCoreExtension startup")


        # At this point, we register our Service's `router` under the prefix we gave our API using the settings system,

        # to facilitate its configuration and to ensure it is unique from all other extensions we may have enabled:

        url_prefix = carb.settings.get_settings().get_as_string(f"exts/{ext_name}/url_prefix")

        main.register_router(router=router, prefix=url_prefix, tags=["Viewport capture"],)


    def on_shutdown(self) -> None:

        carb.log_info("ViewportCaptureCoreExtension shutdown")


        # When disabling the extension or shutting down the instance of the Omniverse application, let's make sure we

        # also deregister our Service's `router` in order to avoid our API being erroneously advertised as present as

        # part of the OpenAPI specification despite our handler function no longer being available:

        main.deregister_router(router=router)