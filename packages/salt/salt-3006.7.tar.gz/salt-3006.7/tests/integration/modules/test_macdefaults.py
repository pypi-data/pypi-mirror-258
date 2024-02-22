"""
Validate the mac-defaults module
"""
import pytest

from tests.support.case import ModuleCase

DEFAULT_DOMAIN = "com.apple.AppleMultitouchMouse"
DEFAULT_KEY = "MouseHorizontalScroll"
DEFAULT_VALUE = "0"


@pytest.mark.destructive_test
@pytest.mark.skip_if_not_root
@pytest.mark.skip_unless_on_darwin
class MacDefaultsModuleTest(ModuleCase):
    """
    Integration tests for the mac_default module
    """

    def test_macdefaults_write_read(self):
        """
        Tests that writes and reads macdefaults
        """
        write_domain = self.run_function(
            "macdefaults.write", [DEFAULT_DOMAIN, DEFAULT_KEY, DEFAULT_VALUE]
        )
        self.assertTrue(write_domain)

        read_domain = self.run_function(
            "macdefaults.read", [DEFAULT_DOMAIN, DEFAULT_KEY]
        )
        self.assertTrue(read_domain)
        self.assertEqual(read_domain, DEFAULT_VALUE)
