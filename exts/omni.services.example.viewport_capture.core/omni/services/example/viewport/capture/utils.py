import asyncio
import os
import shutil
from typing import Optional, Tuple
import carb.settings
import carb.tokens
import omni.kit.actions.core
import omni.kit.app
import omni.usd



# Let's include a small utility method to facilitate obtaining the name of the extension our code is bundled with.

# While we could certainly store and share the `ext_id` provided to the `on_startup()` method of our Extension, this

# alternative method of obtaining the name of our extension can also make our code more portable across projects, as it

# may allow you to keep your code changes located closer together and not have to spread them up to the main entrypoint

# of your extension.

def get_extension_name() -> str:

    """

    Return the name of the Extension where the module is defined.


    Args:

        None


    Returns:

        str: The name of the Extension where the module is defined.


    """

    extension_manager = omni.kit.app.get_app().get_extension_manager()

    extension_id = extension_manager.get_extension_id_by_module(__name__)

    extension_name = extension_id.split("-")[0]

    return extension_name



# Building on the utility method just above, this helper method helps us retrieve the path where captured images are

# served from the web server, so they can be presented to clients over the network.

def get_captured_image_path() -> str:

    """

    Return the path where the captured images can be retrieved from the server, in the `/{url_prefix}/{capture_path}`

    format.


    Args:

        None


    Returns:

        str: The path where the captured images can be retrieved from the server.


    """

    extension_name = get_extension_name()

    settings = carb.settings.get_settings()

    url_prefix = settings.get_as_string(f"exts/{extension_name}/url_prefix")

    capture_path = settings.get_as_string(f"exts/{extension_name}/capture_path")


    captured_images_path = f"{url_prefix}{capture_path}"

    return captured_images_path



# In a similar fashion to the utility method above, this helper method helps us retrieve the path on disk where the

# captured images are stored on the server. This makes it possible to map this storage location known to the server to a

# publicly-accessible location on the server, from which clients will be able to fetch the captured images once their

# web-friendly names have been communicated to clients through our Service's response.

def get_captured_image_directory() -> str:

    """

    Return the location on disk where the captured images will be stored, and from which they will be served by the web

    server after being mounted. In order to avoid growing the size of this static folder indefinitely, images will be

    stored under the `${temp}` folder of the Omniverse application folder, which is emptied when the application is shut

    down.


    Args:

        None


    Returns:

        str: The location on disk where the captured images will be stored.


    """

    extension_name = _get_extension_name()

    capture_directory_name = carb.settings.get_settings().get_as_string(f"exts/{extension_name}/capture_directory")

    temp_kit_directory = carb.tokens.get_tokens_interface().resolve("${temp}")

    captured_stage_images_directory = os.path.join(temp_kit_directory, capture_directory_name)

    return captured_stage_images_directory



# This is the main utility method of our collection so far. This small helper builds on the existing capability of the

# "Edit > Capture Screenshot" feature already available in the menu to capture an image from the Omniverse application

# currently running. Upon completion, the captured image is moved to the storage location that is mapped to a

# web-accessible path so that clients are able to retrieve the screenshot once they are informed of the image's unique

# name when our Service issues its response.

async def capture_viewport(usd_stage_path: str) -> Tuple[bool, Optional[str], Optional[str]]:

    """

    Capture the viewport, by executing the action already registered in the "Edit > Capture Screenshot" menu.


    Args:

        usd_stage_path (str): Path of the USD stage to open in the application's viewport.


    Returns:

        Tuple[bool, Optional[str], Optional[str]]: A tuple containing a flag indicating the success of the operation,

            the path of the captured image on the web server, along with an optional error message in case of error.


    """

    success: bool = omni.usd.get_context().open_stage(usd_stage_path)

    captured_image_path: Optional[str] = None

    error_message: Optional[str] = None


    if success:

        event = asyncio.Event()


        menu_action_success: bool = False

        capture_screenshot_filepath: Optional[str] = None

        def callback(success: bool, captured_image_path: str) -> None:

            nonlocal menu_action_success, capture_screenshot_filepath

            menu_action_success = success

            capture_screenshot_filepath = captured_image_path


            event.set()


        omni.kit.actions.core.execute_action("omni.kit.menu.edit", "capture_screenshot", callback)

        await event.wait()

        await asyncio.sleep(delay=1.0)


        if menu_action_success:

            # Move the screenshot to the location from where it can be served over the network:

            destination_filename = os.path.basename(capture_screenshot_filepath)

            destination_filepath = os.path.join(get_captured_image_directory(), destination_filename)

            shutil.move(src=capture_screenshot_filepath, dst=destination_filepath)


            # Record the final location of the captured image, along with the status of the operation:

            captured_image_path = os.path.join(get_captured_image_path(), destination_filename)

            success = menu_action_success

    else:

        error_message = f"Unable to open stage \"{usd_stage_path}\"."


    return (success, captured_image_path, error_message)
