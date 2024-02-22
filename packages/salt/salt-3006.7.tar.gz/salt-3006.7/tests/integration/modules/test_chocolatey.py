import pytest

import salt.utils.path
import salt.utils.platform
from tests.support.case import ModuleCase
from tests.support.sminion import create_sminion


@pytest.mark.skip_unless_on_windows
@pytest.mark.windows_whitelisted
@pytest.mark.destructive_test
@pytest.mark.slow_test
class ChocolateyModuleTest(ModuleCase):
    """
    Validate Chocolatey module
    """

    @classmethod
    def setUpClass(cls):
        """
        Ensure that Chocolatey is installed
        """
        if salt.utils.path.which("chocolatey.exe") is None:
            sminion = create_sminion()
            sminion.functions.chocolatey.bootstrap()

    def test_list_(self):
        ret = self.run_function("chocolatey.list", narrow="adobereader", exact=True)
        self.assertTrue("adobereader" in ret)

    def test_list_sources(self):
        ret = self.run_function("chocolatey.list_sources")
        self.assertTrue("chocolatey" in ret.keys())
