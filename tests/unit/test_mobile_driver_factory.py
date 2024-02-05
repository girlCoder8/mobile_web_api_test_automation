from pytest import mark

from tests.fixtures.conftest import mobile_driver  # type: ignore
from hybrid.enums.appium_automation_name import AppiumAutomationName
from hybrid.enums.browser_make import MobileWebBrowserMake
from hybrid.enums.mobile_app_type import MobileAppType
from hybrid.enums.mobile_device_environment_type import MobileDeviceEnvironmentType
from hybrid.enums.mobile_os import MobileOs


@mark.skip(reason="require infrastructure to support to run this test case and is resource intensive")
@mark.unit_test
@mark.parametrize(
    "mobile_driver",
    [
        {
            "arg_mobile_os": MobileOs.ANDROID,
            "arg_mobile_app_type": MobileAppType.WEB,
            "arg_mobile_device_environment_type": MobileDeviceEnvironmentType.PHYSICAL,
            "arg_automation_name": AppiumAutomationName.UIAUTOMATOR2,
            "arg_mobile_web_browser": MobileWebBrowserMake.CHROME,
        }
    ],
    indirect=True,
)
def test_mobile_driver_factory(mobile_driver):
    mobile_driver.get("https://www.google.com")
    title = mobile_driver.title
    assert isinstance(title, str) and title.lower().__eq__("google")
