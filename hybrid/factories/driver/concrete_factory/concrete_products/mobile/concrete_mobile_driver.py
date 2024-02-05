from typing import Any

from hybrid.enums.file_paths import FilePaths
from hybrid.enums.mobile_os import MobileOs
from hybrid.enums.test_environments import TestEnvironments
from hybrid.enums.test_execution_mode import TestExecutionMode
from hybrid.factories.driver.abstract_factory.abstract_products.abstract_mobie.abstract_mobile import AbstractMobile
from hybrid.factories.driver.concrete_factory.concrete_products.mobile.concrete_android_driver import ConcreteAndroidDriver
from hybrid.factories.driver.concrete_factory.concrete_products.mobile.concrete_ios_driver import ConcreteIOSDriver
from hybrid.utilities.parser.yaml_parser_utils import YamlParser
from hybrid.utilities.ui.appium_core.appium_core_utils import CoreUtils


class ConcreteMobileDriver(AbstractMobile):
    """
    Concrete mobile browser factory produce a family of web browsers that belong to
    web variant. The factory guarantees that resulting web browsers are compatible.
    Note that signature of the concrete mobile browser factory's methods return an abstract
    web browser, while inside the method a concrete product is instantiated.
    """

    def __init__(
        self,
        *,
        os: MobileOs,
        test_execution_mode: TestExecutionMode,
        test_environment: TestEnvironments,
    ) -> None:
        """Concrete implementation of mobile driver instance creation

        Args:
            os (MobileOs): mobile os enum
            test_execution_mode (TestExecutionMode): test execution mode enum
            test_environment (TestEnvironments): test environments enum
        """
        self.testEnv = test_environment
        self.os = os
        self.testExecMode = test_execution_mode

    def get_mobile_driver(self, *, capabilities: dict[str, Any]):
        """Concrete implementation of fetching mobile driver

        Args:
            capabilities (dict[str, Any]): mobile capabilities

        Returns:
            tuple: (mobile driver instance, appium port)
        """
        common_config = YamlParser(FilePaths.COMMON)
        # launch appium service
        port = CoreUtils.launch_appium_service()
        # return requested mobile driver
        remote_url = (
            common_config.get_value(
                "appium",
                "appium_base_url_local"
                if self.testExecMode.value.__eq__(TestExecutionMode.LOCAL.value)
                else "appium_base_url_remote",
            ),
        )[0].replace("${port}", str(port))
        from urllib.parse import urlparse

        host = urlparse(remote_url).hostname
        CoreUtils.wait_for_appium_service_to_load(30, host, port)
        return (
            ConcreteAndroidDriver(remote_url).get_driver(capabilities=capabilities)
            if self.os.value.__eq__(MobileOs.ANDROID.value)
            else ConcreteIOSDriver(remote_url).get_driver(capabilities=capabilities)
        ), port
