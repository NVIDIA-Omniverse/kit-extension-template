import carb.settings


import omni.kit.test


# Let's import the components for which we intend to provide unit tests from their module paths:

from omni.services.renderer.core.utils import (

    get_captured_image_directory,

    get_captured_image_path,

    get_extension_name,

)



# Unit tests for Omniverse Extensions follow the standard patterns and best practices of the Python community, and

# already well-defined around the `unittest` module.

#

# In case this is your first experience writing unit tests, just know that having a test class derived from

# `omni.kit.test.AsyncTestCase` declared on the root of module will make it auto-discoverable by the test framework,

# and the methods prefixed with the `test_*` keyword will be automatically executed.

class TestUtils(omni.kit.test.AsyncTestCase):

    """Unit tests for the `utils` module."""


    def _get_setting(self, setting_key: str) -> str:

        """

        Utility method to return extension settings.


        Args:

            setting_key (str): Key of the setting to retrieve.


        Returns:

            str: The value of the setting with the given key.


        """

        settings = carb.settings.get_settings()

        return settings.get_as_string(f"exts/omni.services.renderer.core/{setting_key}")


    def test_extension_name_matches_default_extension_name(self) -> None:

        """Ensure the method to obtain the extension's name matches the actual extension name."""

        self.assertEqual(get_extension_name(), "omni.services.renderer.core")


    def test_captured_image_directory_ends_with_configured_setting_value(self) -> None:

        """Ensure the resolved directory where captures are stored ends with the configured setting value."""

        capture_directory_name = self._get_setting("capture_directory")


        self.assertTrue(

            get_captured_image_directory().endswith(capture_directory_name),

            "Expected the path to the capture directory to end with the name of the directory provided as setting.",

        )


    def test_captured_image_path_starts_with_api_url_prefix(self) -> None:

        """Ensure the web-friendly capture path contains the API URL components."""

        url_prefix = self._get_setting("url_prefix")

        capture_path = self._get_setting("capture_path")


        self.assertTrue(

            get_captured_image_path().startswith(url_prefix),

            "Expected the web-friendly capture path to contain the API URL prefix.",

        )

        self.assertTrue(

            get_captured_image_path().endswith(capture_path),

            "Expected the web-friendly capture path to contain the API storage path.",

        )